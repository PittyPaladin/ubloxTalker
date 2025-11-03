import serial
import copy
import threading
from collections import deque
import time
import struct
import logging
import re
import sys
from dataclasses import dataclass, field, fields, MISSING
from typing import List, Dict, Any

from ubloxDefines import *
from ubloxCfgIface import UBX_REMAINS_DEFAULT_CFG, UBX_COMPLETE_ICD_DEFAULT_CFG

##############
### Logger ###
##############
def setup_logger(name, level=logging.DEBUG, log_to_file=False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is reused
    if not logger.handlers:
        formatter = logging.Formatter("[%(levelname)s] [%(name)s] %(message)s")

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional file handler
        if log_to_file:
            file_handler = logging.FileHandler("gnss_driver.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

# Instantiate logger
logger = setup_logger("GNSSDriver")

#################
### Constants ###
#################
BUFFER_SIZE = 1024
FIFO_QUEUE_SIZE = 512

#############
### Utils ###
#############
def popN(dq, n):
    """Pop n bytes from the left of deque and return them as a bytes object."""
    popable_bytes = min(len(dq), n)
    return bytes(dq.popleft() for _ in range(popable_bytes))

def buffer2Ascii(intArr):
    return bytes(intArr).decode('ascii', errors='ignore')

# Get the time difference between current minus past timestamp
def time_diff_from(pastTimeStamp):
    return time.monotonic() - pastTimeStamp

#########################
### GNSS Driver class ###
#########################
class GNSSDriver:
    @dataclass
    class PendingCmds:
        bPendingDrvStop_: bool = False
        bPendingMonVer_: bool = False
        bPendingLogInfo_: bool = False
        bPendingMonGnss_: bool = False
        bPendingMonComms_: bool = False
        bPendingMonRf_: bool = False
        bPendingAck_: bool = False
        bPendingPVT_: bool = False
        bPendingReset_: bool = False

        def reset(self):
            default_dc_reset(self)

    @dataclass
    class IBIT:
        subMode_: IBITSubMode = IBITSubMode.SubModeClearAll
        startTs_: float = 0.0
        bSentMemClear_: bool = False

        def reset(self):
            default_dc_reset(self)

    @dataclass
    class CBIT:
        subMode_: CBITSubMode = CBITSubMode.SubModeBITRun
        startTs_: float = 0.0

        def reset(self):
            default_dc_reset(self)

    @dataclass
    class BIT:
        subMode_: CBITSubMode = BITSubMode.SubModeCheckCommsErrs
        startTs_: float = 0.0
        bSentMonComms_: bool = False
        bSentMonRf_: bool = False
        requested_mon_rf_: bool = False
        requested_comms_: bool = False

        def reset(self):
            default_dc_reset(self)

    @dataclass
    class PBIT:
        subMode_: PBITSubMode = PBITSubMode.SubModeRst
        currentMemLayer_: CfgMemLayer = CfgMemLayer.eLayerRAM
        startTs_: float = 0.0
        tries_: int = 0
        requestedVer_: bool = False
        requestedConstellations_: bool = False

        def reset(self, keepNumAttempts=False):
            for f in fields(self):
                if keepNumAttempts and f.name == "tries_":
                    continue
                if f.default is not MISSING:
                    setattr(self, f.name, f.default)
                elif f.default_factory is not MISSING:
                    setattr(self, f.name, f.default_factory())
                else:
                    setattr(self, f.name, None)

    @dataclass
    class Operational:
        startTs_: float = 0.0
        lastPVTReqTs_: float = 0.0
        cbit_period_: float = CBIT_PERIOD # [sec]

        def reset(self):
            default_dc_reset(self)

    @dataclass
    class CfgCtrlData:
        subMode_: CfgCtrlSubmode = CfgCtrlSubmode.SubModeValget
        sentValget_: bool = False
        keyIdsToValset_: List[int] = field(default_factory=list)
        bMoreValgetNeeded_: bool = False
        sentValset_: bool = False
        valget_items_cntr: int = 0
        success_: bool = False
        rxValgetItemsRing_: Dict[str, Any] = field(default_factory=dict)
        currentMemLayer_: CfgMemLayer = CfgMemLayer.eLayerRAM

        def reset(self):
            default_dc_reset(self)

    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.running = False
        self.lock = threading.Lock()
        self.read_thread = None

        # Driver's Finite State Machine (FSM) mode
        self.driverMode_ = GnssDriverMode.NoMode

        self.rxRing_ = deque(maxlen=BUFFER_SIZE)  # Circular buffer for RX
        self.ringBytesToRead_ = 1
        self.msgBuffer_ = bytearray(BUFFER_SIZE)
        self.msgIdx_ = 0 # working index of the msg buffer
        self.parserState_ = MsgParserState.eParserNone

        # Pending message responses
        self.cmds = self.PendingCmds()

        # [RX Internal Data]
        self.bFlashAttached_ = False
        self.rx_version_ = ("unk", "unk")
        self.constellations_up_ = 0
        self.jamming_state = False
        self.ant_status_ = 0
        self.ant_pwr_ = 0
        # Analytics
        self.cksumErrors = 0
        self.wcet_ = 0.0

        # [CFG Handler] Used by BIT and CBIT
        self.cfgr = self.CfgCtrlData()
        # Application-specific config only with cfg items that differ from RX defaults
        self.ascfg_ = copy.deepcopy(APP_SPECIFIC_CFG)
        # Default config of the Ublox receiver according to ICD
        self.defcfg_ = copy.deepcopy(UBX_REMAINS_DEFAULT_CFG)

        # [BIT] mode variables
        self.bit = self.BIT()

        # [PBIT] mode variables
        self.pbit = self.PBIT()

        # [IBIT] mode variables
        self.ibit = self.IBIT()

        # [CBIT] mode variables
        self.cbit = self.CBIT()

        # [Operational] mode variables
        self.opmode = self.Operational()


    # Public member functions
    # ---------------------------------------------
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.debug(f"Connected to {self.port} at {self.baudrate} baud.")
            self.running = True
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
        except serial.SerialException as e:
            logger.error(f"Connection failed: {e}")
            self.ser = None

    def disconnect(self):
        self.running = False
        if self.read_thread:
            self.read_thread.join(timeout=1)
        if self.is_connected():
            self.ser.close()
            logger.info("Serial connection closed.")

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def _read_loop(self):
        """Simulates interrupt-driven reception: producer that writes to RX buffer."""
        while self.running and self.is_connected():
            try:
                if self.ser.in_waiting:
                    with self.lock:
                        # Note: calling list to store bytes as ints one by one
                        self.rxRing_.extend( list(self.ser.readline()) )
            except Exception as e:
                break

    def Initialize(self):
        self.connect()

    def launch_ibit(self):
        # Regardless of current state, reset all data from all states and
        # transition immediately to IBIT
        self.reset_all_internal_data()
        self.driverMode_ = GnssDriverMode.IBIT

    def reset_all_internal_data(self):
        self.bit.reset()
        self.cfgr.reset()
        self.ibit.reset()
        self.cbit.reset()
        self.opmode.reset()
        self.cmds.reset()
        self.reset_ascfg_knowledge()
        self.reset_defcfg_knowledge()

    def Run(self):
        runStartTs = time.monotonic()

        # Early exit if not running
        if not self.running:
            return

        # Handle priority commands
        self.handle_priority_cmd()

        # Handle current mode actions
        self.handle_mode()

        # Read bytes in ring and process messages
        self.read_rx_ring()

        # Compute Run() execution time and store Worst Case Execution Time (wcet)
        runExecTime = time_diff_from(runStartTs)
        if runExecTime > self.wcet_:
            self.wcet_ = runExecTime


    # Private member functions
    # ---------------------------------------------
    def handle_priority_cmd(self):
        # Handle top priority commands
        pass # TODO: add as needed

    def handle_mode(self):
        if self.driverMode_ == GnssDriverMode.NoMode:
            # Transition to first mode
            self.driverMode_ = GnssDriverMode.PBIT
        elif self.driverMode_ == GnssDriverMode.PBIT:
            self.runPBIT()
        elif self.driverMode_ == GnssDriverMode.CBIT:
            self.runCBIT()
        elif self.driverMode_ == GnssDriverMode.IBIT:
            self.runIBIT()
        elif self.driverMode_ == GnssDriverMode.Operational:
            self.runOperational()
        elif self.driverMode_ == GnssDriverMode.Failure:
            pass # TODO


    #################################### [START] > PBIT member functions < [START] #####################################
    def runPBIT(self):
        # Restart PBIT first for a clean run, but increment number of PBIT attempts
        if self.pbit.startTs_ == 0.0:
            self.pbit.reset(keepNumAttempts=True)
            self.pbit.tries_ += 1
            self.pbit.startTs_ = time.monotonic()
            logger.info(f"PBIT: Launching NOW")

        # Reset to rebuild RAM cfg
        # --------------------------------------------------
        # Request UBX-CFG-RST for a controlled SW reset to recover default config
        # to RAM (either coming from flash storage if available, or from HW defaults)
        # Reset is called once only, when PBIT starts up at submode none
        if self.pbit.subMode_ == PBITSubMode.SubModeRst:
            # BBR not meant to store cfg items, only used (if present) for nav data storage.
            # This will trigger a rebuild of RAM configuration settings from all the lower layers.
            self.req_bbr_erase_and_reload_cfg()

            # SW rst gives no response and starts straight away, so change mode now
            self.pbit.subMode_ = PBITSubMode.SubModeReqVer

        # Request RX version
        # --------------------------------------------------
        # Request UBX-MON-VER and check receiver version (also request UBX-LOG_INFO
        # to see if flash memory is attached)
        elif self.pbit.subMode_ == PBITSubMode.SubModeReqVer:
            # Perform request
            if not self.pbit.requestedVer_:
                self.req_mon_ver()
                self.req_flash_mem()
                self.pbit.requestedVer_ = True
            # Request was sent, and...
            else:
                rx_version_ok = True # TODO
                # reponse arrived, and version number is OK
                if not self.cmds.bPendingMonVer_ and rx_version_ok and not self.cmds.bPendingLogInfo_:
                    self.pbit.subMode_ = PBITSubMode.SubModeReqConstellations
                # reponse arrived, and version number is NOT OK -> go to fail mode
                elif not self.cmds.bPendingMonVer_ and not rx_version_ok:
                    self.pbit.subMode_ = PBITSubMode.SubModeFailure

        # Request enabled constellations
        # --------------------------------------------------
        # Request UBX-MON-GNSS to check the minimum main constellations are supported
        elif self.pbit.subMode_ == PBITSubMode.SubModeReqConstellations:
            # Perform request
            if not self.pbit.requestedConstellations_:
                self.req_supported_constellations()
                self.pbit.requestedConstellations_ = True
            # Request was sent, and...
            else:
                constellations_ok = self.constellations_up_ & UBX_MON_GNSS_GPS_BIT_MASK # at least
                # response arrived and is OK
                if not self.cmds.bPendingMonGnss_ and constellations_ok:
                    self.pbit.subMode_ = PBITSubMode.SubModeASCfgHandler
                # response arrived and is NOT OK -> go to fail mode
                elif not self.cmds.bPendingMonGnss_ and not constellations_ok:
                    self.pbit.subMode_ = PBITSubMode.SubModeFailure

        # Run BIT
        # --------------------------------------------------
        elif self.pbit.subMode_ == PBITSubMode.SubModeBITRun:
            self.runBIT()
            if self.bit.subMode_ == BITSubMode.SubModeSuccess:
                self.pbit.subMode_ = PBITSubMode.SubModeASCfgHandler
            elif self.bit.subMode_ == BITSubMode.SubModeFailure:
                logger.critical(f"PBIT > BIT failed!")
                self.pbit.subMode_ = PBITSubMode.SubModeFailure

        # Apply config
        # --------------------------------------------------
        # After the SW, reset RAM layer was rebuilt from defaults and flash. Now,
        # application-specific config (ascfg) items are input into the receiver.
        elif self.pbit.subMode_ == PBITSubMode.SubModeASCfgHandler:
            self.cfg_ctrl(self.ascfg_)

        # Failed submode, do nothing
        # --------------------------------------------------
        elif self.pbit.subMode_ == PBITSubMode.SubModeFailure:
            pass # check transition will handle it from here

        else:
            logger.error(f"Unknown PBIT submode: {self.pbit.subMode_}")

        # Check if conditions meets for transition to another state
        self.check_transition_from_PBIT()

    def check_transition_from_PBIT(self):
        transition = False
        if self.pbit.subMode_ == PBITSubMode.SubModeFailure:
            logger.critical(f"PBIT: Failed. Going to Fail mode!")
            self.driverMode_ = GnssDriverMode.Failure
            transition = True
        elif self.pbit.subMode_ == PBITSubMode.SubModeASCfgHandler and self.cfgr.success_:
            logger.info(f"PBIT > SUCCESS! Transitioning to Operational Mode")
            self.driverMode_ = GnssDriverMode.Operational
            transition = True
        else:
            # BIT timed out?
            if time_diff_from(self.pbit.startTs_) > BIT_TIMEOUT:
                if self.pbit.tries_ >= BIT_MAX_TRIES:
                    # Go to fail mode
                    logger.critical(f"PBIT > timed out. No more retries. Going to Fail mode!")
                    self.driverMode_ = GnssDriverMode.Failure
                    transition = True
                else:
                    # Try again BIT procedure
                    logger.warning(f"PBIT > timed out, restarting BIT procedure")
                    self.pbit.reset(keepNumAttempts=True)

        if transition:
            self.cleanup_PBIT()

        return transition

    def cleanup_PBIT(self):
        self.pbit.reset()
        self.cfgr.reset()
    ###################################### [END] > PBIT member functions < [END] #######################################


    #################################### [START] > BIT member functions < [START] #####################################
    def runBIT(self):
        # Check comms
        # --------------------------------------------------
        if self.bit.subMode_ == BITSubMode.SubModeCheckCommsErrs:
            if not self.bit.requested_comms_:
                self.req_mon_comms()
                self.bit.requested_comms_ = True
            # Request was sent and...
            else:
                # response arrived and comms are OK
                if not self.cmds.bPendingMonComms_ and not (self.txErrors_mem_ or self.txErrors_alloc_):
                    self.bit.subMode_ = BITSubMode.SubModeCheckDyns
                # response arrived and comms are NOK
                if not self.cmds.bPendingMonComms_ and (self.txErrors_mem_ or self.txErrors_alloc_):
                    self.bit.subMode_ = BITSubMode.SubModeFailure

        # Check coherent RX dynamics
        # --------------------------------------------------
        elif self.bit.subMode_ == BITSubMode.SubModeCheckDyns:
            if self.rx_dynamics_ok():
                self.bit.subMode_ = BITSubMode.SubModeItfState
            else:
                self.bit.subMode_ = BITSubMode.SubModeFailure

        # Check interference state
        # --------------------------------------------------
        elif self.bit.subMode_ == BITSubMode.SubModeItfState:
            if not self.bit.requested_mon_rf_:
                self.req_mon_rf()
                self.bit.requested_mon_rf_ = True
            else:
                if not self.cmds.bPendingMonRf_:
                    self.bit.subMode_ = BITSubMode.SubModeCheckAnt
                    if self.jamming_state == JAMMING_STATE_CRITICAL:
                        # Raise jamming warning
                        logger.warning(f"BIT > RX jammed!")

        # Check antenna status
        # --------------------------------------------------
        elif self.bit.subMode_ == BITSubMode.SubModeCheckAnt:
            # Use same UBX-MON-RF received at last submode
            # if (self.ant_status_ == ANT_STATUS_OK) and (self.ant_pwr_ == ANT_PWR_ON):
            if True: # FIXME
                self.bit.subMode_ = BITSubMode.SubModeSuccess
            else:
                self.bit.subMode_ = BITSubMode.SubModeFailure
    ###################################### [END] > BIT member functions < [END] #######################################


    def cfg_ctrl(self, cfgdb):
        # Get values of application-specific configuration items
        # ----------------------------------------------------------------------
        if self.cfgr.subMode_ == CfgCtrlSubmode.SubModeValget:
            # [Prepare VALGET] with ascfg to see its values
            if not self.cfgr.sentValget_:
                # Construct a UBX-CFG-VALGET message asking for the values of the following application-specific
                # configuration items. Thay may already be set as desired in RAM if they were stored in flash memory
                # in a previous BIT.
                valget_msg = [0xB5, 0x62, 0x06, 0x8B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
                valget_fmt = '<BB8B'
                valget_len = 4 # version, layer and position make up the 4 bytes
                self.cfgr.valget_items_cntr = 0
                self.cfgr.bMoreValgetNeeded_ = False
                keys_cntr = 0
                for keyId in cfgdb:
                    keys_cntr += 1
                    if self.cfgr.valget_items_cntr+1 > MAX_VALGET_REQ_ITEMS: # mind max query limit
                        self.cfgr.bMoreValgetNeeded_ = True
                        break
                    # Skip those cfg items whose value is already the desired one
                    if cfgdb[keyId]["actualVal"] == cfgdb[keyId]["expectedVal"]:
                        continue

                    valget_msg.append(keyId)
                    valget_fmt += 'I'
                    valget_len += 4
                    self.cfgr.valget_items_cntr += 1

                valget_msg[UBX_MSG_PAYLOAD_LEN_POS : UBX_PAYLOAD_POS] = valget_len.to_bytes(2, byteorder='little', signed=False) # add total payload length
                valget_msg = struct.pack(valget_fmt, *valget_msg) # array of ints to bytes

                if self.cfgr.valget_items_cntr == 0:
                    logger.debug(f"CFG CTRL > VALGET not needed, all cfg values set!")
                    self.cfgr.success_ = True
                else:
                    # Add CRC and send the CFG-VALGET command
                    crc = struct.pack('<BB', *self.computeUbxCRC(valget_msg[2:]))
                    valget_msg = bytearray(valget_msg + crc)
                    self.send_command(valget_msg)
                    logger.debug(f"CFG CTRL > Sending VALGET for {keys_cntr}/{len(cfgdb)} cfg items")

                    self.cfgr.sentValget_ = True

            # [VALGET requested] awaiting response
            else:
                # [VALGET received] ring has data from the request
                if len(self.cfgr.rxValgetItemsRing_) >= self.cfgr.valget_items_cntr:
                    self.cfgr.sentValget_ = False
                    for keyId in list(self.cfgr.rxValgetItemsRing_):
                        # Store values in config and check if value is as expected. If not, put the
                        # key into a "keys to VALSET" list.
                        if keyId in cfgdb:
                            cfgdb[keyId]["actualVal"] = self.cfgr.rxValgetItemsRing_.pop(keyId)
                            if cfgdb[keyId]["actualVal"] != cfgdb[keyId]["expectedVal"]:
                                self.cfgr.keyIdsToValset_.append(keyId)
                            else:
                                if keyId in self.cfgr.keyIdsToValset_:
                                    self.cfgr.keyIdsToValset_.remove(keyId)

                    # If all cfg values set, BIT success. If not, go to VALSET them.
                    bAllCfgValuesSet = (len(self.cfgr.keyIdsToValset_) == 0)
                    if bAllCfgValuesSet:
                        if not self.cfgr.bMoreValgetNeeded_:
                            logger.debug(f"CFG CTRL > All cfg values set!")
                            self.cfgr.success_ = True
                    else:
                        self.cfgr.subMode_ = CfgCtrlSubmode.SubModeValset

        # Set values of application-specific configuration items
        # ----------------------------------------------------------------------
        elif self.cfgr.subMode_ == CfgCtrlSubmode.SubModeValset:
            layer = self.cfgr.currentMemLayer_.value
            # [Prepare VALSET] with application-specific configuration values
            if not self.cfgr.sentValset_:
                valset_msg = [0xB5, 0x62, 0x06, 0x8a, 0x00, 0x00, 0x00, 2**layer, 0x00, 0x00]
                #                 Header,class,   ID,     length, vers,    layer,  reserved0
                valset_fmt = '<BB8B'
                valset_len = 4 # version, layer and reserved0 make up the 4 bytes
                cfg_items_cntr = 0
                # Iterate for all cfg items
                for keyId in self.cfgr.keyIdsToValset_:
                    # Keep in mind only 64 cfg items can be queried
                    if cfg_items_cntr >= MAX_VALSET_REQ_ITEMS:
                        break

                    # Some messages cannot be set on some layers...
                    if self.skip_cfg_item(keyId, self.cfgr.currentMemLayer_):
                        cfgdb[keyId]["actualVal"] = cfgdb[keyId]["expectedVal"]
                        continue

                    # Skip those cfg items that already have the desired value
                    if cfgdb[keyId]["actualVal"] == cfgdb[keyId]["expectedVal"]:
                        continue

                    # Add keyId to message
                    valset_msg.append(keyId)
                    valset_fmt += 'I'
                    valset_len += 4

                    # Add corresponding value
                    keyValue = cfgdb[keyId]["expectedVal"]
                    valset_msg.append(keyValue)
                    vlen, vfmt = self.getKeyLenAndFmt(cfgdb[keyId]["type"])
                    valset_fmt += vfmt
                    valset_len += vlen

                    cfg_items_cntr += 1

                # Add total payload length
                valset_msg[UBX_MSG_PAYLOAD_LEN_POS : UBX_PAYLOAD_POS] = valset_len.to_bytes(2, byteorder='little', signed=False)
                # Array of ints to bytes message
                valset_msg = struct.pack(valset_fmt, *valset_msg)

                if cfg_items_cntr == 0:
                    logger.debug(f"CFG CTRL > VALSET not needed, all cfg values set!")
                    self.cfgr.subMode_ = CfgCtrlSubmode.SubModeValget
                else:
                    # Add CRC and send the CFG-VALSET command
                    crc = struct.pack('<BB', *self.computeUbxCRC(valset_msg[2:]))
                    valset_msg = bytearray(valset_msg + crc)
                    # print("Valset send:", [hex(x) for x in valset_msg])
                    self.send_command(valset_msg)
                    self.cmds.bPendingAck_ = True
                    self.cfgr.sentValset_ = True
                    logger.debug(f"CFG CTRL > Sending CFG-VALSET command for {cfg_items_cntr} cfg items for {layer=}")

            # [VALSET sent] awaiting ACK
            else:
                # ACK arrived and no more cfg items pending sending
                if not self.cmds.bPendingAck_:
                    self.cfgr.sentValset_ = False

                    # Go to set cfg for next layer
                    self.cfgr.currentMemLayer_ = CfgMemLayer(self.cfgr.currentMemLayer_ + 1)

                    # Skip BBR layer since it was fully erased at the beginning of PBIT, we want flash
                    if self.cfgr.currentMemLayer_ == CfgMemLayer.eLayerBBR:
                        if not self.bFlashAttached_:
                            self.cfgr.subMode_ = CfgCtrlSubmode.SubModeValget
                        else:
                            self.cfgr.currentMemLayer_ = CfgMemLayer(self.cfgr.currentMemLayer_ + 1)
                    # Last memory layer done
                    elif self.cfgr.currentMemLayer_ >= CfgMemLayer.eLayerEnumSize:
                        # Go send another VALGET to check the values you sent are properly set
                        self.cfgr.subMode_ = CfgCtrlSubmode.SubModeValget

    def skip_cfg_item(self, keyId, mem_layer):
        skip = False
        if mem_layer == CfgMemLayer.eLayerRAM:
            if keyId == 0x10510003:
                skip = True
        return skip

    #################################### [START] > CBIT member functions < [START] #####################################
    def runCBIT(self):
        if self.cbit.startTs_ == 0.0:
            # Restart variables for a clean run
            self.cleanup_CBIT()
            self.cbit.startTs_ = time.monotonic()
            logger.info("CBIT > Launching NOW")

        # Run BIT
        # --------------------------------------------------
        if self.cbit.subMode_ == CBITSubMode.SubModeBITRun:
            self.runBIT()
            if self.bit.subMode_ == BITSubMode.SubModeSuccess:
                self.cbit.subMode_ = CBITSubMode.SubModeDefCfgChecker
            elif self.bit.subMode_ == BITSubMode.SubModeFailure:
                logger.critical(f"PBIT > BIT failed!")
                self.cbit.subMode_ = CBITSubMode.SubModeFailure

        # Check that config not set in BIT remains at ICD default values
        # --------------------------------------------------
        elif self.cbit.subMode_ == CBITSubMode.SubModeDefCfgChecker:
            self.cfg_ctrl(self.defcfg_)

        else:
            logger.error(f"Unknown CBIT submode: {self.cbit.subMode_}")
            self.cbit.subMode_ = CBITSubMode.SubModeFailure

        # Check if transition from this state to another needs to be performed
        self.check_transition_from_CBIT()

    def check_transition_from_CBIT(self):
        transition = False
        if self.cbit.subMode_ == CBITSubMode.SubModeFailure:
            logger.critical(f"CBIT > Failed. Transitioning to Failure mode")
            self.driverMode_ = GnssDriverMode.Failure
            transition = True
        elif self.cbit.subMode_ == CBITSubMode.SubModeDefCfgChecker:
            if self.cfgr.success_:
                logger.info(f"CBIT > SUCCESS! Transitioning to Operational Mode")
                self.driverMode_ = GnssDriverMode.Operational
                self.reset_defcfg_knowledge()
                transition = True
            elif time_diff_from(self.cbit.startTs_) > CBIT_STAY_TIME:
                logger.info(f"CBIT > Transitioning to Operational Mode, pending complete defcfg check")
                self.driverMode_ = GnssDriverMode.Operational
                transition = True
            # TODO: a stuck CBIT defcfg checker that never ends can't be detected
        else: # Check CBIT timeout
            if time_diff_from(self.cbit.startTs_) > CBIT_TIMEOUT:
                # Go to fail mode
                logger.critical(f"CBIT > Timed out! Transitioning to Failure mode")
                self.driverMode_ = GnssDriverMode.Failure
                self.reset_defcfg_knowledge()
                transition = True

        # Reset dataclasses before actual mode transition
        if transition:
            self.cleanup_CBIT()

        return transition

    def rx_dynamics_ok(self):
        return True # TODO

    def cleanup_CBIT(self):
        self.cbit.reset()
        self.cfgr.reset()

    def reset_defcfg_knowledge(self):
        self.defcfg_ = copy.deepcopy(UBX_REMAINS_DEFAULT_CFG)
    ####################################### [END] > CBIT member functions < [END] ######################################


    #################################### [START] > IBIT member functions < [START] #####################################
    def runIBIT(self):
        if self.ibit.startTs_ == 0.0:
            # Restart IBIT related variables for a clean run
            self.cleanup_IBIT()
            # Restart IBIT-related variables since they were changed at last BIT run
            self.ibit.startTs_ = time.monotonic()
            logger.info("IBIT > Launching NOW")

        # Clear memory
        # --------------------------------------------------
        if self.ibit.subMode_ == IBITSubMode.SubModeClearAll:
            # Perform request
            if not self.ibit.bSentMemClear_:
                # Delete all cfg in flash and BBR (send the command regardless
                # if flash or even BBR presence is verified)
                self.req_clear_all()
                self.ibit.bSentMemClear_ = True
                logger.debug("IBIT > Clearing all cfg in flash and BBR")
            # Request was sent, and ACK arrived
            else:
                if not self.cmds.bPendingAck_:
                    # Transition to RST submode
                    self.ibit.subMode_ = IBITSubMode.SubModeRst
                    # Reset your current knowledge of RX cfg
                    self.reset_ascfg_knowledge()

        # Send reset command to rebuild config RAM layer
        # --------------------------------------------------
        elif self.ibit.subMode_ == IBITSubMode.SubModeRst:
            # Call UBX reset command, Rx does not acknowledge the command so time it
            if not self.cmds.bPendingReset_:
                self.req_ubx_cfg_rst()
                logger.debug("IBIT > Sending RST")
            else:
                if time_diff_from(self.ibit.startTs_) > IBIT_WAIT_AFTER_RST:
                    self.ibit.subMode_ = IBITSubMode.SubModeBITRun
                    self.cmds.bPendingReset_ = False # toggle it back
                    self.connect() # restart pyserial connection

        # Run BIT
        # --------------------------------------------------
        elif self.ibit.subMode_ == IBITSubMode.SubModeBITRun:
            self.runBIT()
            if self.bit.subMode_ == BITSubMode.SubModeSuccess:
                self.ibit.subMode_ = IBITSubMode.SubmodeSetASCfg
            elif self.bit.subMode_ == BITSubMode.SubModeFailure:
                logger.critical(f"IBIT > BIT failed!")
                self.ibit.subMode_ = IBITSubMode.SubModeFailure

        elif self.ibit.subMode_ == IBITSubMode.SubmodeSetASCfg:
            self.cfg_ctrl(self.ascfg_)

        self.check_transition_from_IBIT()

    def check_transition_from_IBIT(self):
        transition = False
        if self.ibit.subMode_ == IBITSubMode.SubModeFailure:
            logger.critical(f"IBIT > FAILED. Going to Fail Mode!")
            self.driverMode_ = GnssDriverMode.Failure
            transition = True
        elif self.ibit.subMode_ == IBITSubMode.SubmodeSetASCfg and self.cfgr.success_:
            logger.info(f"IBIT > SUCCESS. Going to Operational Mode!")
            self.driverMode_ = GnssDriverMode.Operational
            transition = True
        else:
            # IBIT timed out before reaching BIT launch
            if time_diff_from(self.ibit.startTs_) > IBIT_TIMEOUT:
                logger.critical(f"IBIT > Timed out at submode {self.ibit.subMode_.name}. Going to Fail mode!")
                self.driverMode_ = GnssDriverMode.Failure
                transition = True

        if transition:
            self.cleanup_IBIT()

    def cleanup_IBIT(self):
        self.bit.reset()
        self.cfgr.reset()
        self.ibit.reset()

    def reset_ascfg_knowledge(self):
        self.ascfg_ = copy.deepcopy(APP_SPECIFIC_CFG)
    ###################################### [END] > IBIT member functions < [END] #######################################


    ################################# [START] > OPERATIONAL member functions < [START] #################################
    def runOperational(self):
        if self.opmode.startTs_ == 0.0:
            # Restart BIT and IBIT related variables for a clean run
            self.opmode.reset()
            self.opmode.startTs_ = time.monotonic()
            logger.info("Operational Mode > Launching NOW")

        # Assert PVT cadence is coherent with config
        pvt_period = get_cfg_by_name(self.ascfg_, "CFG-PM-POSUPDATEPERIOD")["actualVal"] * MS_TO_SEC
        if time_diff_from(self.opmode.lastPVTReqTs_) > 5:
            self.req_ubx_nav_pvt()
            print("Pidiendo NAV PVT")
            self.opmode.lastPVTReqTs_ = time.monotonic()

        self.check_transition_from_operational()

    def check_transition_from_operational(self):
        transition = False

        # Regularly run a CBIT to check all is OK
        if self.opmode.cbit_period_ <= 0.0:
            logger.warning("CBIT switching period is <=0.0, so CBIT will never be performed. Not recommended.")
        elif time_diff_from(self.opmode.startTs_) > self.opmode.cbit_period_:
            self.driverMode_ = GnssDriverMode.CBIT
            transition = True

        if transition:
            self.opmode.reset()

        return transition
    ################################### [END] > OPERATIONAL member functions < [END] ###################################

    def read_rx_ring(self):
        with self.lock:
            # Read until emptying the ring
            ringLen = len(self.rxRing_)
            for _ in range(ringLen):
                # Read a certain number of bytes from the RX ring into a <class 'bytes'>
                msg = popN(self.rxRing_, self.ringBytesToRead_)
                bytesRead = len(msg)
                # Update bytes to read subtracting the ones read just now
                self.ringBytesToRead_ -= bytesRead

                # Store them into a temporary buffer
                self.msgBuffer_[self.msgIdx_ : self.msgIdx_ + bytesRead] = msg
                self.msgIdx_+= bytesRead

                # All bytes that needed to be read from the ring have been read
                if self.ringBytesToRead_ == 0:
                    if self.parserState_ == MsgParserState.eParserNone:
                        self.parseNone()
                    elif self.parserState_ == MsgParserState.eParserUBX_SyncChar2:
                        self.parseUbxSyncChar2()
                    elif self.parserState_ == MsgParserState.eParserNMEA:
                        self.parseNmea()
                    elif self.parserState_ == MsgParserState.eParserUBX_PayloadLen:
                        self.parseUbxPayloadLen()
                    elif self.parserState_ == MsgParserState.eParserUBX_Payload:
                        self.parseUbxPayload()
                    else:
                        logger.critical("[FAIL] Wrong parser state")

    def send_command(self, command):
        """Send a command string or bytes to the GNSS module."""
        if not self.is_connected():
            logger.critical("Can't send command, you are not connected!")
            return
        try:
            if isinstance(command, str):
                command_bytes = command.encode('ascii') + b'\r\n'
            else:
                command_bytes = command
            self.ser.write(command_bytes)
            # print(f"Sent: {[hex(x) for x in command]}")
        except Exception as e:
            logger.critical(f"send_command exception: {e}")

    def req_bbr_erase_and_reload_cfg(self):
        msg = struct.pack('>H19B', 0xB562, 0x06, 0x09, 0x0D, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x01, 0x19, 0x98)
        self.send_command(msg)

    def req_controlled_sw_rst(self):
        # Request the reset sending the command
        # msg = struct.pack('>H9B', 0xB562, 0x06, 0x04, 0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0F, 0x66) # Hotstart
        msg = struct.pack('>H10B', 0xB562, 0x06, 0x04, 0x04, 0x00, 0xFF, 0xB9, 0x01, 0x00, 0xC7, 0x8D) # Coldstart
        self.send_command(msg)

    def req_mon_ver(self):
        msg = struct.pack('>HBBHBB', 0xB562, 0x0A, 0x04, 0x0000, 0x0E, 0x34)
        self.send_command(msg)
        self.cmds.bPendingMonVer_ = True

    def req_mon_comms(self):
        msg = struct.pack('>H6B', 0xB562, 0x0A, 0x36, 0x00, 0x00, 0x40, 0xCA)
        self.send_command(msg)
        self.cmds.bPendingMonComms_ = True

    def req_mon_rf(self):
        msg = struct.pack('>H6B', 0xB562, 0x0A, 0x38, 0x00, 0x00, 0x42, 0xD0)
        self.send_command(msg)
        self.cmds.bPendingMonRf_ = True

    def req_flash_mem(self):
        msg = struct.pack('>HBBHBB', 0xB562, 0x21, 0x08, 0x0000, 0x29, 0x9C)
        self.send_command(msg)
        self.cmds.bPendingLogInfo_ = True

    def req_supported_constellations(self):
        msg = struct.pack('>HBBHBB', 0xB562, 0x0A, 0x28, 0x0000, 0x32, 0xA0)
        self.send_command(msg)
        self.cmds.bPendingMonGnss_ = True

    def req_ubx_nav_pvt(self):
        msg = struct.pack('>H6B', 0xB562, 0x01, 0x07, 0x00, 0x00, 0x08, 0x19)
        print([hex(x) for x in msg])
        self.send_command(msg)
        self.cmds.bPendingPVT_ = True

    def req_clear_all(self):
        # valdel_msg = struct.pack('>H14B', 0xB562, 0x06, 0x8C, 0x08, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x0F, 0xAE, 0xD3)
        #                                 Header, Class & ID,     Length, vers, lyrs,  reserved0,                   keys,        CRC
        msg = struct.pack('21B', 0xB5, 0x62, 0x06, 0x09, 0x0D, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x17, 0x2F, 0xAE)
        self.send_command(msg)
        self.cmds.bPendingAck_ = True

    def req_ubx_cfg_rst(self):
        navBbrMask = 0xFFFF # Cold start
        resetMode =  0x00 # Hardware reset (watchdog) immediately
        reserved0 = 0x00
        msg = struct.pack('>HBBHHBBBB', 0xB562, 0x06, 0x04, 0x0400, navBbrMask, resetMode, reserved0, 0x0C, 0x5D)
        self.send_command(msg)
        self.cmds.bPendingReset_ = True

    # ---------------------------------
    # Parsing functions ---------------
    # ---------------------------------
    def parseNone(self):
        if self.msgBuffer_[0] == UBX_PREAMBLE_SYNC_CHAR_1:
            self.parserState_ = MsgParserState.eParserUBX_SyncChar2
        elif self.msgBuffer_[0] == ord(NMEA_START_CHAR):
            self.parserState_ = MsgParserState.eParserNMEA
        else:
            # parser state remains the same, return buffer index to start
            self.msgIdx_ = 0

        # In any case, keep reading bytes one by one
        self.ringBytesToRead_ = 1

    def parseUbxSyncChar2(self):
        if self.msgBuffer_[1] == UBX_PREAMBLE_SYNC_CHAR_2:
            self.parserState_ = MsgParserState.eParserUBX_PayloadLen
            self.ringBytesToRead_ = 4 # Class, ID and payload Length are the following 4 bytes
        else: # false alarm, UBX sync char 1 was fortuitous
            self.parserState_ = MsgParserState.eParserNone
            self.ringBytesToRead_ = 1

    def parseUbxPayloadLen(self):
        # Check msg class and ID are recognized and defined in the ICD
        bRecognizedUbxMsg = self.validUbxClassAndID(self.msgBuffer_[UBX_MSG_CLASS_POS], self.msgBuffer_[UBX_MSG_ID_POS])

        if not bRecognizedUbxMsg:
            self.parserState_ = MsgParserState.eParserNone
            self.msgIdx_ = 0
            self.ringBytesToRead_ = 1
        else:
            self.parserState_ = MsgParserState.eParserUBX_Payload
            payloadLen = int.from_bytes(self.msgBuffer_[UBX_MSG_PAYLOAD_LEN_POS:UBX_PAYLOAD_POS],
                                        byteorder='little')
            self.ringBytesToRead_ = payloadLen + UBX_CHECKSUM_LEN

    def parseUbxPayload(self):
        # First compute that checksums match
        msgForCRC = bytes(self.msgBuffer_[UBX_MSG_CLASS_POS:self.msgIdx_ - 2])
        ck_a, ck_b = self.computeUbxCRC(msgForCRC)

        if ck_a == self.msgBuffer_[self.msgIdx_ - 2] and ck_b == self.msgBuffer_[self.msgIdx_ - 1]:
            if UBX_ACK_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseAckClassMsg()
            elif UBX_INF_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseInfClassMsg()
            elif UBX_CFG_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseCfgClassMsg()
            elif UBX_LOG_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseLogClassMsg()
            elif UBX_MGA_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseMgaClassMsg()
            elif UBX_MON_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseMonClassMsg()
            elif UBX_NAV_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseNavClassMsg()
            elif UBX_RXM_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseRxmClassMsg()
            elif UBX_SEC_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseSecClassMsg()
            elif UBX_TIM_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseTimClassMsg()
            elif UBX_UPD_CLASS == self.msgBuffer_[UBX_MSG_CLASS_POS]:
                self.parseUpdClassMsg()
        else:
            self.cksumErrors += 1
            logger.error(f"Non-matching CRCs for UBX message {[hex(x) for x in msgForCRC]}")

        # Either if message was successfully parsed or not CRC failed, go back to
        # none state to handle new messages coming from the RX ring
        self.parserState_ = MsgParserState.eParserNone
        self.msgIdx_ = 0
        self.ringBytesToRead_ = 1

    def parseAckClassMsg(self):
        clsID = struct.unpack('B', self.msgBuffer_[UBX_ACK_CLSID_POS : UBX_ACK_MSGID_POS])[0]
        msgID = struct.unpack('B', self.msgBuffer_[UBX_ACK_MSGID_POS : UBX_ACK_MSGID_POS + 1])[0]
        if self.msgBuffer_[UBX_MSG_ID_POS] == UBX_ACK_ACK_ID:
            logger.debug(f"ACK for {hex(clsID)} {hex(msgID)}")
            self.cmds.bPendingAck_ = False
        elif self.msgBuffer_[UBX_MSG_ID_POS] == UBX_ACK_NAK_ID:
            logger.debug(f"NACK for {hex(clsID)} {hex(msgID)}")

    def parseInfClassMsg(self):
        pass # TODO: implement

    def parseCfgClassMsg(self):
        if self.msgBuffer_[UBX_MSG_ID_POS] == UBX_CFG_VALGET_ID:
            self.parse_cfg_valget()

    def parse_cfg_valget(self):
        payloadLen = struct.unpack('<H', self.msgBuffer_[UBX_MSG_PAYLOAD_LEN_POS : UBX_PAYLOAD_POS])[0]
        version = struct.unpack('B', self.msgBuffer_[UBX_CFG_VALGET_VERSION_POS : UBX_CFG_VALGET_LAYER_POS])[0]
        layer = struct.unpack('B', self.msgBuffer_[UBX_CFG_VALGET_LAYER_POS : UBX_CFG_VALGET_POSITION_POS])[0]
        position = struct.unpack('<H', self.msgBuffer_[UBX_CFG_VALGET_POSITION_POS : UBX_CFG_VALGET_FIRST_KEYID_POS])[0]

        bParsingKeyId = True # starts by parsing key ID
        msgIdx = UBX_CFG_VALGET_FIRST_KEYID_POS
        payloadByteIdx = 4 # [bytes] since version, layer and position have already been parsed
        while True:
            if bParsingKeyId:
                keyId = struct.unpack('<I', self.msgBuffer_[msgIdx : msgIdx + UBX_CFG_KEYID_LEN])[0]
                # If Key ID is unknown, alert of error and break
                if not keyId in UBX_COMPLETE_ICD_DEFAULT_CFG:
                    logger.error(f"CFG-VALGET received has an unknown Key ID of {hex(keyId)}! Ignoring it...")

                # Increment index and bytes of payload parsed
                msgIdx += UBX_CFG_KEYID_LEN
                payloadByteIdx += UBX_CFG_KEYID_LEN
                # Next follows a key value
                bParsingKeyId = False

            else: # it's key value
                # Get the type of the value that corresponds to the key ID
                keyValue, valueLen = self.parseCfgValgetValue(self.msgBuffer_, msgIdx, UBX_COMPLETE_ICD_DEFAULT_CFG[keyId]["type"])
                logger.debug(f"VALGET parser says: KeyId {hex(keyId)} = {keyValue}")

                # Store key Id/Value pair to rx VALGET dict
                self.cfgr.rxValgetItemsRing_[keyId] = keyValue

                # Increment index and bytes of payload parsed
                msgIdx += valueLen
                payloadByteIdx += valueLen
                # Next follows a key ID
                bParsingKeyId = True

            # Stop parsing Key ID/Values pairs when payload length is reached
            if payloadByteIdx >= payloadLen:
                break

        logger.debug(f"CFG-VALGET parsed: {payloadLen=}, {version=}, {layer=}, {position=}")

    def parseCfgValgetValue(self, msgBuff, currIdx, keyValueType):
        val_len, val_fmt = self.getKeyLenAndFmt(keyValueType)
        keyValue = struct.unpack(val_fmt, msgBuff[currIdx : currIdx + val_len])[0]
        if keyValueType == "L": # transform to boolean instead of int
            keyValue = False if keyValue == 0 else True
        return keyValue, val_len

    def getKeyLenAndFmt(self, keyValueType):
        # L: single-bit boolean (true = 1, false = 0), stored as U1
        if keyValueType == "L":
            val_len = 1
            val_fmt = 'B'
        # Unsigned little-endian 8-bit widths
        elif keyValueType == "U1" or keyValueType == "E1" or keyValueType == "X1":
            val_len = 1
            val_fmt = 'B'
        # Unsigned little-endian 16-bit widths
        elif keyValueType == "U2" or keyValueType == "E2" or keyValueType == "X2":
            val_len = 2
            val_fmt = 'H'
        # Unsigned little-endian 32-bit widths
        elif keyValueType == "U4" or keyValueType == "E4" or keyValueType == "X4":
            val_len = 4
            val_fmt = 'I'
        # Unsigned little-endian 64-bit widths
        elif keyValueType == "U8" or keyValueType == "E8" or keyValueType == "X8":
            val_len = 8
            val_fmt = 'Q'
        # IEEE 754 single (32-bit) and double (64-bit) precision floats
        elif keyValueType == "R4":
            val_len = 4
            val_fmt = 'f'
        elif keyValueType == "R8":
            val_len = 8
            val_fmt = 'd'
        # I1, I2, I4, I8: signed little-endian, two's complement integers of 8-, 16-, 32- and 64-bit widths
        elif keyValueType == "I1":
            val_len = 1
            val_fmt = 'b'
        elif keyValueType == "I2":
            val_len = 2
            val_fmt = 'h'
        elif keyValueType == "I4":
            val_len = 4
            val_fmt = 'i'
        elif keyValueType == "I8":
            val_len = 8
            val_fmt = 'q'
        else:
            val_len = None
            val_fmt = None

        return val_len, val_fmt

    def parseLogClassMsg(self):
        if self.msgBuffer_[UBX_MSG_ID_POS] == UBX_LOG_INFO_ID:
            flash_size = int.from_bytes(self.msgBuffer_[UBX_LOG_INFO_FILESTORE_CAPACITY_POS : UBX_LOG_INFO_RESERVED1],
                                        byteorder='little')
            if  flash_size >= MIN_FILESTORE_CAPACITY:
                self.bFlashAttached_ = True
                logger.info(f"Flash device detected with {flash_size} bytes")
            else:
                # Explicitly lower it in case from PBIT to PBIT (between successive wake-ups)
                # flash gets somehow filled
                self.bFlashAttached_ = False
                logger.info("Flash device NOT detected")
            self.cmds.bPendingLogInfo_ = False

    def parseMgaClassMsg(self):
        pass # TODO: implement

    def parseMonClassMsg(self):
        if self.msgBuffer_[UBX_MSG_ID_POS] == UBX_MON_COMMS_ID:
            self.parseMonComms()
        elif self.msgBuffer_[UBX_MSG_ID_POS] == UBX_MON_VER_ID:
            self.parseMonVer()
        elif self.msgBuffer_[UBX_MSG_ID_POS] == UBX_MON_GNSS_ID:
            self.parseMonGnss()
        elif self.msgBuffer_[UBX_MSG_ID_POS] == UBX_MON_RF_ID:
            self.parseMonRf()

    def parseMonComms(self):
        txErrors = struct.unpack('<B', self.msgBuffer_[UBX_MON_COMMS_TXERRORS_POS : UBX_MON_COMMS_RESERVED0_POS])[0]
        self.txErrors_mem_ = txErrors & 0b0001
        self.txErrors_alloc_ = txErrors & 0b0010
        self.cmds.bPendingMonComms_ = False

    def parseMonVer(self):
        # Parse SW and HW version fields
        swVersion = buffer2Ascii(self.msgBuffer_[UBX_MON_VER_SW_VERSION_POS : UBX_MON_VER_HW_VERSION_POS])
        hwVersion = buffer2Ascii(self.msgBuffer_[UBX_MON_VER_HW_VERSION_POS : UBX_MON_VER_EXTENSION_POS])

        # Get whole extension Ascii field
        payload_len = struct.unpack('<H', self.msgBuffer_[UBX_MSG_PAYLOAD_LEN_POS : UBX_PAYLOAD_POS])[0]
        payload_len_excl_sw_hw = payload_len - (UBX_MON_VER_SW_VERSION_LEN + UBX_MON_VER_HW_VERSION_LEN)
        extension_field_last_pos = UBX_MON_VER_EXTENSION_POS + payload_len_excl_sw_hw
        extension = buffer2Ascii(self.msgBuffer_[UBX_MON_VER_EXTENSION_POS : extension_field_last_pos])

        # Extract SPG version from extension field
        spg_match = re.search(r"FWVER=SPG (\d+\.\d+)", extension)
        spg = float(spg_match.group(1)) if spg_match else None
        if spg < MIN_PRODUCT_FW_VER:
            logger.error(f"Product FW version SPG {spg} below minimum of {MIN_PRODUCT_FW_VER}!")

        # Extract PROTVER version from extension field
        protver_match = re.search(r"PROTVER=(\d+\.\d+)", extension)
        protver = float(protver_match.group(1)) if protver_match else None
        if protver < MIN_PROTOCOL_VER:
            logger.error(f"Protocol version {protver} below minimum of {MIN_PROTOCOL_VER}!")

        self.rx_version_ = (spg, protver)
        self.cmds.bPendingMonVer_ = False
        logger.debug(f"MON-VER parsed: {swVersion=}, {hwVersion=}, {protver=}, {spg=}")

    def parseMonGnss(self):
        supported = struct.unpack('<B', self.msgBuffer_[UBX_MON_GNSS_SUPPORTED_MASK_POS : UBX_MON_GNSS_DEFAULT_GNSS_MASK_POS])[0]
        defaultGnss = struct.unpack('<B', self.msgBuffer_[UBX_MON_GNSS_DEFAULT_GNSS_MASK_POS : UBX_MON_GNSS_ENABLED_MASK_POS])[0]
        enabled = struct.unpack('<B', self.msgBuffer_[UBX_MON_GNSS_ENABLED_MASK_POS : UBX_MON_GNSS_SIMULTANEOUS_POS])[0]
        simultaneous = struct.unpack('<B', self.msgBuffer_[UBX_MON_GNSS_SIMULTANEOUS_POS : UBX_MON_GNSS_RESERVED0_POS])[0]

        self.constellations_up_ = enabled
        self.cmds.bPendingMonGnss_ = False
        logger.debug(f"UBX-MON-GNSS returns > supported: {format(supported, '08b')} | defaultGnss: {format(defaultGnss, '08b')} | "\
                        f"enabled: {format(enabled, '08b')} | simultaneous: {simultaneous}")

    def parseMonRf(self):
        self.jamming_state = struct.unpack('<B', self.msgBuffer_[UBX_MON_RF_FLAGS_POS : UBX_MON_RF_ANTSTATUS_POS])[0]
        self.ant_status_ = struct.unpack('<B', self.msgBuffer_[UBX_MON_RF_ANTSTATUS_POS : UBX_MON_RF_ANTPOWER_POS])[0]
        self.ant_pwr_ = struct.unpack('<B', self.msgBuffer_[UBX_MON_RF_ANTPOWER_POS : UBX_MON_RF_POSTSTATUS_POS])[0]

        self.cmds.bPendingMonRf_ = False
        logger.debug(f"UBX-MON-RF returns > JAM STATE: {self.jamming_state} | ANT_STATUS: {self.ant_status_} | ANT_PWR: {self.ant_pwr_}")

    def parseNavClassMsg(self):
        if self.msgBuffer_[UBX_MSG_ID_POS] == UBX_NAV_PVT_ID:
            numSV = struct.unpack('<B', self.msgBuffer_[UBX_NAV_PVT_NUMSV_POS : UBX_NAV_PVT_LON_POS])[0]
            lon = struct.unpack('<i', self.msgBuffer_[UBX_NAV_PVT_LON_POS : UBX_NAV_PVT_LAT_POS])[0] / UBX_NAV_LON_SCALE
            lat = struct.unpack('<i', self.msgBuffer_[UBX_NAV_PVT_LAT_POS : UBX_NAV_PVT_HEIGHT_POS])[0] / UBX_NAV_LAT_SCALE
            height = struct.unpack('<i', self.msgBuffer_[UBX_NAV_PVT_LAT_POS : UBX_NAV_PVT_HEIGHT_POS])[0] / UBX_NAV_HEIGHT_SCALE

            # print(f"\r{numSV=}, {lon=:.4f}, {lat=:.4f}, {height=:.2f}", end="", flush=True)
            self.lastPVTTstamp_ = time.monotonic()
            logger.debug(f"{numSV=} {lon=} {lat=} {height=} | Last update: {self.lastPVTTstamp_}")
        else:
            logger.debug(f"Unknown NAV class message with ID {self.msgBuffer_[UBX_MSG_ID_POS]}")

    def parseRxmClassMsg(self):
        pass # TODO: implement

    def parseSecClassMsg(self):
        pass # TODO: implement

    def parseTimClassMsg(self):
        pass # TODO: implement

    def parseUpdClassMsg(self):
        pass # TODO: implement

    def validUbxClassAndID(self, msg_class, msg_id):
        return msg_class in SUPPORTED_UBX_MSGS and msg_id in SUPPORTED_UBX_MSGS[msg_class]

    def parseNmea(self):
        # NMEA msg end chars reached, else keep on storing chars in the buffer
        if self.msgBuffer_[self.msgIdx_ - 2] == ord(NMEA_END_CR_CHAR) and \
           self.msgBuffer_[self.msgIdx_ - 1] == ord(NMEA_END_LF_CHAR):
            # Whole NMEA message is in buffer, now decode its data
            self.decodeNMEA()

            self.parserState_ = MsgParserState.eParserNone
            self.msgIdx_ = 0

        # With NMEA messages always read byte per byte
        self.ringBytesToRead_ = 1

    def decodeNMEA(self):
        nmeaMsgType = self.msgBuffer_[NMEA_TYPE_POS : NMEA_TYPE_POS + NMEA_TYPE_LEN]
        msgForCRC = self.msgBuffer_[1:self.msgIdx_ - NMEA_FROM_ASTERISK_TRAIL_LEN]
        incomingCRC = chr(self.msgBuffer_[self.msgIdx_ - 4]) + chr(self.msgBuffer_[self.msgIdx_ - 3])
        incomingCRC = int(incomingCRC, 16)

        # First check that checksum is OK
        if incomingCRC != self.computeNmeaCRC(msgForCRC):
            # Ignore it and increment wrong incoming checksum messages counter
            self.cksumErrors += 1
        elif nmeaMsgType == NMEA_GGA_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_GSA_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_VTG_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_GST_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_GSV_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_ZDA_MSG_ID:
            pass # TODO: implement
        elif nmeaMsgType == NMEA_TXT_MSG_ID:
            pass # TODO: implement

    def getNextNmeaDelimiter(self, nmeaMsg, startIdx):
        for i in range(startIdx, startIdx + NMEA_MAX_FIELD_LEN):
            if nmeaMsg[i] == ord(NMEA_DELIMITER_CHAR):
                return i

    def computeUbxCRC(self, data):
        """
        Compute UBX checksum (8-bit Fletcher).
        data: bytes from CLASS through end of payload (no sync chars).
        Returns: (CK_A, CK_B)
        """
        ck_a = 0
        ck_b = 0
        for byte in data:
            ck_a = (ck_a + byte) & 0xFF
            ck_b = (ck_b + ck_a) & 0xFF
        return ck_a, ck_b

    def computeNmeaCRC(self, data):
        """
        Compute the NMEA checksum from a bytearray containing the message.
        The data must start after '$' and must not include the '*xx' checksum.
        Returns the checksum as an integer (0–255).
        """
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum




############
### Main ###
############
def input_listener(driver):
    while driver.is_connected():
        cmd = input("").strip()
        if cmd == "ibit" or cmd == "IBIT":
            driver.launch_ibit()

if __name__ == "__main__":
    driver = GNSSDriver(port='COM4', baudrate=38400)

    # Init
    driver.Initialize()

    threading.Thread(target=input_listener, args=(driver,), daemon=True).start()

    # main loop
    while driver.is_connected():
        try:
            driver.Run()  # Blocking consumer loop
            time.sleep(0.025)
        except KeyboardInterrupt:
            driver.disconnect()
            print("\n[GNSSDriver] Stopped by user.")
