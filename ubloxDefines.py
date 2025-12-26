import time
from enum import IntEnum
from dataclasses import fields, MISSING

##########################
### Modes and submodes ###
##########################
class GnssDriverMode(IntEnum):
    NoMode = 1
    PBIT = 2
    CBIT = 3
    IBIT = 4
    Operational = 5
    Failure = 6

class PBITSubMode(IntEnum):
    SubModeRst = 1
    SubModeReqVer = 2
    SubModeReqConstellations = 3
    SubModeBITRun = 4
    SubModeASCfgHandler = 5
    SubModeFailure = 6

class CBITSubMode(IntEnum):
    SubModeBITRun = 1
    SubModeDefCfgChecker = 2
    SubModeFailure = 3

class BITSubMode(IntEnum):
    SubModeCheckCommsErrs = 1
    SubModeCheckDyns = 2
    SubModeItfState = 3
    SubModeCheckAnt = 4
    SubModeSuccess = 5
    SubModeFailure = 6

class IBITSubMode(IntEnum):
    SubModeClearAll = 1
    SubModeRst = 2
    SubModeBITRun = 3
    SubmodeSetASCfg = 4
    SubModeFailure = 5

class MsgParserState(IntEnum):
    eParserNone = 1
    eParserUBX_SyncChar2 = 2
    eParserNMEA = 3
    eParserUBX_PayloadLen = 4
    eParserUBX_Payload = 5

class CfgCtrlSubmode(IntEnum):
    SubModeValget = 0
    SubModeValset = 1

class CfgMemLayer(IntEnum):
    eLayerRAM = 0
    eLayerBBR = 1
    eLayerFlash = 2
    eLayerEnumSize = 3

class GeofenceState(IntEnum):
    eOFF = 0
    eRequesting = 1
    eON = 2

#########################
### Physics Constants ###
#########################
MS_TO_SEC = 1e-3

#####################
### CFG Constants ###
#####################
MIN_PRODUCT_FW_VER = 4.04
MIN_PROTOCOL_VER = 32.01

BIT_MAX_TRIES = 3
BIT_TIMEOUT = 10 # [seconds]
CBIT_TIMEOUT = 10 # [seconds]
CBIT_STAY_TIME = 10 # [seconds]
CBIT_PERIOD = 10*100 # [seconds]
IBIT_WAIT_AFTER_RST = 10.0
IBIT_TIMEOUT = IBIT_WAIT_AFTER_RST + 10.0 # [seconds]

MIN_FILESTORE_CAPACITY = 10_000 # [bytes]

GEOFENCE_REQ_PERIOD = 10 # [seconds]
GEOREFERENCE_CONFIDENCE = 2 # 95%
GEOREFERENCE_RADIUS_M = 20 # [meters]
GEOREFERENCE_RADIUS_SCALE = 1e-2

UBX_NAV_LAT_SCALE = 1e-7
UBX_NAV_LON_SCALE = 1e-7
UBX_NAV_HEIGHT_SCALE = 1e-3 # mm to m

CFG_VAL_UNKNOWN = "NA"

APP_SPECIFIC_CFG = {
    # CFG-ANA section
    # ---------------------
    0x10230001: {
        "name": "CFG-ANA-USE_ANA",
        "type": "L",
        "expectedVal": False, # Disabled
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-I2C section
    # ---------------------
    0x10510003: {
        "name": "CFG-I2C-ENABLED",
        "type": "L",
        "expectedVal": False, # Disabled
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-INFMSG messages
    # ---------------------
    0x20920001: {
        "name": "CFG-INFMSG-UBX_I2C",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920002: {
        "name": "CFG-INFMSG-UBX_UART1",
        "type": "X1",
        "expectedVal": 0x01 | 0x02, # ERROR and WARNING messages enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920003: {
        "name": "CFG-INFMSG-UBX_UART2",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920005: {
        "name": "CFG-INFMSG-UBX_SPI",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920006: {
        "name": "CFG-INFMSG-NMEA_I2C",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920007: {
        "name": "CFG-INFMSG-NMEA_UART1",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920008: {
        "name": "CFG-INFMSG-NMEA_UART2",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20920009: {
        "name": "CFG-INFMSG-NMEA_USB",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x2092000A: {
        "name": "CFG-INFMSG-NMEA_SPI",
        "type": "X1",
        "expectedVal": 0x00, # No message enabled
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-MSGOUT messages
    # ---------------------
    # GGA
    0x209100ba: {
        "name": "CFG-MSGOUT-NMEA_ID_GGA_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100be: {
        "name": "CFG-MSGOUT-NMEA_ID_GGA_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100bb: {
        "name": "CFG-MSGOUT-NMEA_ID_GGA_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100bc: {
        "name": "CFG-MSGOUT-NMEA_ID_GGA_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100bd: {
        "name": "CFG-MSGOUT-NMEA_ID_GGA_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    # GLL
    0x209100c9: {
        "name": "CFG-MSGOUT-NMEA_ID_GLL_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100cd: {
        "name": "CFG-MSGOUT-NMEA_ID_GLL_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100ca: {
        "name": "CFG-MSGOUT-NMEA_ID_GLL_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100cb: {
        "name": "CFG-MSGOUT-NMEA_ID_GLL_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100cc: {
        "name": "CFG-MSGOUT-NMEA_ID_GLL_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    # GSA
    0x209100bf: {
        "name": "CFG-MSGOUT-NMEA_ID_GSA_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c3: {
        "name": "CFG-MSGOUT-NMEA_ID_GSA_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c0: {
        "name": "CFG-MSGOUT-NMEA_ID_GSA_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c1: {
        "name": "CFG-MSGOUT-NMEA_ID_GSA_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c2: {
        "name": "CFG-MSGOUT-NMEA_ID_GSA_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    # GSV
    0x209100c4: {
        "name": "CFG-MSGOUT-NMEA_ID_GSV_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c8: {
        "name": "CFG-MSGOUT-NMEA_ID_GSV_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c5: {
        "name": "CFG-MSGOUT-NMEA_ID_GSV_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c6: {
        "name": "CFG-MSGOUT-NMEA_ID_GSV_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100c7: {
        "name": "CFG-MSGOUT-NMEA_ID_GSV_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    # RMC
    0x209100ab: {
        "name": "CFG-MSGOUT-NMEA_ID_RMC_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100af: {
        "name": "CFG-MSGOUT-NMEA_ID_RMC_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100ac: {
        "name": "CFG-MSGOUT-NMEA_ID_RMC_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100ad: {
        "name": "CFG-MSGOUT-NMEA_ID_RMC_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100ae: {
        "name": "CFG-MSGOUT-NMEA_ID_RMC_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    # VTG
    0x209100b0: {
        "name": "CFG-MSGOUT-NMEA_ID_VTG_I2C",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100b4: {
        "name": "CFG-MSGOUT-NMEA_ID_VTG_SPI",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100b1: {
        "name": "CFG-MSGOUT-NMEA_ID_VTG_UART1",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100b2: {
        "name": "CFG-MSGOUT-NMEA_ID_VTG_UART2",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x209100b3: {
        "name": "CFG-MSGOUT-NMEA_ID_VTG_USB",
        "type": "U1",
        "expectedVal": 0, # Rate null (no messages)
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20910009: {
        "name": "CFG-MSGOUT-UBX_NAV_PVT_USB",
        "type": "U1",
        "expectedVal": 1, # enable with rate 1
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x2091001d: {
        "name": "CFG-MSGOUT-UBX_NAV_STATUS_USB",
        "type": "U1",
        "expectedVal": 1, # enable with rate 1
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-NAVSPG messages
    # ---------------------
    # 0x20110011: {
    #     "name": "CFG-NAVSPG-FIXMODE",
    #     "type": "E1",
    #     "expectedVal": 2, # 3D only
    #     "actualVal": CFG_VAL_UNKNOWN
    # },
    # 0x10110013: {
    #     "name": "CFG-NAVSPG-INIFIX3D",
    #     "type": "L",
    #     "expectedVal": True,
    #     "actualVal": CFG_VAL_UNKNOWN
    # },
    0x10110019: {
        "name": "CFG-NAVSPG-USE_PPP",
        "type": "L",
        "expectedVal": False, # Disabled
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x20110021: {
        "name": "CFG-NAVSPG-DYNMODEL",
        "type": "E1",
        "expectedVal": 2, # Stationary
        "actualVal": CFG_VAL_UNKNOWN
    },
    # 0x201100a1: {
    #     "name": "CFG-NAVSPG-INFIL_MINSVS",
    #     "type": "U1",
    #     "expectedVal": 4, # sats
    #     "actualVal": CFG_VAL_UNKNOWN
    # },
    # 0x201100a4: {
    #     "name": "CFG-NAVSPG-INFIL_MINELEV",
    #     "type": "I1",
    #     "expectedVal": 15, # deg
    #     "actualVal": CFG_VAL_UNKNOWN
    # },

    # CFG-PM messages
    # ---------------------
    0x20d00001: {
        "name": "CFG-PM-OPERATEMODE",
        "type": "E1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x40d00002: {
        "name": "CFG-PM-POSUPDATEPERIOD",
        "type": "U4",
        "expectedVal": 60,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-QZSS messages
    # ---------------------
    0x10370005: {
        "name": "CFG-QZSS-USE_SLAS_DGNSS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-RATE messages
    # ---------------------
    # 0x30210001: {
    #     "name": "CFG-RATE-MEAS",
    #     "type": "U2",
    #     "expectedVal": 10_000,
    #     "actualVal": CFG_VAL_UNKNOWN
    # },
    # 0x30210002: {
    #     "name": "CFG-RATE-NAV",
    #     "type": "U2",
    #     "expectedVal": 3,
    #     "actualVal": CFG_VAL_UNKNOWN
    # },

    # CFG-SBAS messages
    # ---------------------
    0x10360003: {
        "name": "CFG-SBAS-USE_RANGING",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x10360004: {
        "name": "CFG-SBAS-USE_DIFFCORR",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-SIGNAL messages
    # ---------------------
    0x10310020: {
        "name": "CFG-SIGNAL-SBAS_ENA",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x10310005: {
        "name": "CFG-SIGNAL-SBAS_L1CA_ENA",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-UART1INPROT messages
    # ---------------------
    0x10730001: {
        "name": "CFG-UART1INPROT-UBX",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },
    0x10730004: {
        "name": "CFG-UART1INPROT-RTCM3X",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-UART1OUTPROT messages
    # ---------------------
    0x10740002: {
        "name": "CFG-UART1OUTPROT-NMEA",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },

    # CFG-UART2 messages
    # ---------------------
    0x10530005: {
        "name": "CFG-UART2-ENABLED",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN
    },
}

#################
### Constants ###
#################
UBX_PREAMBLE_SYNC_CHAR_1 = 0xb5
UBX_PREAMBLE_SYNC_CHAR_2 = 0x62

UBX_MSG_CLASS_POS = 2
UBX_MSG_ID_POS = 3
UBX_MSG_PAYLOAD_LEN_POS = 4
UBX_CHECKSUM_LEN = 2 # checksum composed of 2 bytes (CK_A and CK_B)
UBX_PAYLOAD_POS = 6

# UBX-ACK-ACK
UBX_ACK_CLSID_POS = UBX_PAYLOAD_POS + 0
UBX_ACK_MSGID_POS = UBX_PAYLOAD_POS + 1

# UBX-MON-COMMS
UBX_MON_COMMS_TXERRORS_POS = UBX_PAYLOAD_POS + 2
UBX_MON_COMMS_RESERVED0_POS = UBX_PAYLOAD_POS + 3

# UBX-MON-VER
UBX_MON_VER_SW_VERSION_LEN = 30
UBX_MON_VER_HW_VERSION_LEN = 10
UBX_MON_VER_SW_VERSION_POS = UBX_PAYLOAD_POS + 0
UBX_MON_VER_HW_VERSION_POS = UBX_MON_VER_SW_VERSION_POS + UBX_MON_VER_SW_VERSION_LEN
UBX_MON_VER_EXTENSION_POS = UBX_MON_VER_HW_VERSION_POS + UBX_MON_VER_HW_VERSION_LEN
JAMMING_STATE_UNK = 0
JAMMING_STATE_OK = 1
JAMMING_STATE_WARN_OK = 2
JAMMING_STATE_CRITICAL = 3
ANT_STATUS_INIT = 0x00
ANT_STATUS_DONTKNOW = 0x01
ANT_STATUS_OK = 0x02
ANT_STATUS_SHORT = 0x03
ANT_STATUS_OPEN = 0x04
ANT_PWR_OFF = 0x00
ANT_PWR_ON = 0x01
ANT_PWR_DONTKNOW = 0x02

# UBX-MON-GNSS
UBX_MON_GNSS_SUPPORTED_MASK_POS = UBX_PAYLOAD_POS + 1
UBX_MON_GNSS_DEFAULT_GNSS_MASK_POS = UBX_PAYLOAD_POS + 2
UBX_MON_GNSS_ENABLED_MASK_POS = UBX_PAYLOAD_POS + 3
UBX_MON_GNSS_SIMULTANEOUS_POS = UBX_PAYLOAD_POS + 4
UBX_MON_GNSS_RESERVED0_POS = UBX_PAYLOAD_POS + 5

UBX_MON_GNSS_GPS_BIT_MASK = 0b00000001
UBX_MON_GNSS_GLO_BIT_MASK = 0b00000010
UBX_MON_GNSS_BDS_BIT_MASK = 0b00000100
UBX_MON_GNSS_GAL_BIT_MASK = 0b00001000

# UBX-MON-RF
UBX_MON_RF_FLAGS_POS = UBX_PAYLOAD_POS + 5
UBX_MON_RF_ANTSTATUS_POS = UBX_PAYLOAD_POS + 6
UBX_MON_RF_ANTPOWER_POS = UBX_PAYLOAD_POS + 7
UBX_MON_RF_POSTSTATUS_POS = UBX_PAYLOAD_POS + 8

# UBX-LOG-INFO
UBX_LOG_INFO_FILESTORE_CAPACITY_POS = UBX_PAYLOAD_POS + 4
UBX_LOG_INFO_RESERVED1 = UBX_PAYLOAD_POS + 8

# UBX-CFG-VALGET
MAX_VALGET_REQ_ITEMS = 64
UBX_CFG_KEYID_LEN = 4
UBX_CFG_VALGET_VERSION_POS = UBX_PAYLOAD_POS + 0
UBX_CFG_VALGET_LAYER_POS = UBX_PAYLOAD_POS + 1
UBX_CFG_VALGET_POSITION_POS = UBX_PAYLOAD_POS + 2
UBX_CFG_VALGET_FIRST_KEYID_POS = UBX_PAYLOAD_POS + 4

# UBX-CFG-VALSET
MAX_VALSET_REQ_ITEMS = 64

# UBX-NAV-PVT
UBX_NAV_PVT_ITOW_POS = UBX_PAYLOAD_POS + 0
UBX_NAV_PVT_YEAR_POS = UBX_PAYLOAD_POS + 4
UBX_NAV_PVT_MONTH_POS = UBX_PAYLOAD_POS + 6
UBX_NAV_PVT_DAY_POS = UBX_PAYLOAD_POS + 7
UBX_NAV_PVT_HOUR_POS = UBX_PAYLOAD_POS + 8
UBX_NAV_PVT_MIN_POS = UBX_PAYLOAD_POS + 9
UBX_NAV_PVT_SEC_POS = UBX_PAYLOAD_POS + 10
UBX_NAV_PVT_VALID_POS = UBX_PAYLOAD_POS + 11
UBX_NAV_PVT_TACC_POS = UBX_PAYLOAD_POS + 12
UBX_NAV_PVT_FIXTYPE_POS = UBX_PAYLOAD_POS + 20
UBX_NAV_PVT_FLAGS_POS = UBX_PAYLOAD_POS + 21
UBX_NAV_PVT_GNSSFIXOK_BIT = 0
UBX_NAV_PVT_DIFFSOLN_BIT = 1
UBX_NAV_PVT_PSMSTATE_BIT = 2
UBX_NAV_PVT_NUMSV_POS = UBX_PAYLOAD_POS + 23
UBX_NAV_PVT_LON_POS = UBX_PAYLOAD_POS + 24
UBX_NAV_PVT_LAT_POS = UBX_PAYLOAD_POS + 28
UBX_NAV_PVT_HEIGHT_POS = UBX_PAYLOAD_POS + 32
UBX_NAV_PVT_HMSL_POS = UBX_PAYLOAD_POS + 36
UBX_NAV_PVT_HACC_POS = UBX_PAYLOAD_POS + 40
UBX_NAV_PVT_VELN_POS = UBX_PAYLOAD_POS + 48
UBX_NAV_PVT_VELE_POS = UBX_PAYLOAD_POS + 52
UBX_NAV_PVT_VELD_POS = UBX_PAYLOAD_POS + 56

# UBX-NAV-STATUS
UBX_NAV_STATUS_ITOW_POS = UBX_PAYLOAD_POS + 0
UBX_NAV_STATUS_GPSFIX_POS = UBX_PAYLOAD_POS + 4
UBX_NAV_STATUS_FLAGS_POS = UBX_PAYLOAD_POS + 5
UBX_NAV_STATUS_FIXSTAT_POS = UBX_PAYLOAD_POS + 6
UBX_NAV_STATUS_FLAGS2_POS = UBX_PAYLOAD_POS + 7
UBX_NAV_STATUS_TTFF_POS = UBX_PAYLOAD_POS + 8
UBX_NAV_STATUS_MSSS_POS = UBX_PAYLOAD_POS + 12

# UBX-NAV-GEOFENCE
UBX_NAV_GEOFENCE_ITOW_POS = UBX_PAYLOAD_POS + 0
UBX_NAV_GEOFENCE_STATUS_POS = UBX_PAYLOAD_POS + 5
UBX_NAV_GEOFENCE_NUMFENCES_POS = UBX_PAYLOAD_POS + 6
UBX_NAV_GEOFENCE_COMBSTATE_POS = UBX_PAYLOAD_POS + 7

##############################
### NMEA parsing constants ###
##############################
NMEA_START_CHAR = '$'
NMEA_END_CR_CHAR = '\r'
NMEA_END_LF_CHAR = '\n'
NMEA_DELIMITER_CHAR = ','

NMEA_TYPE_POS = 3
NMEA_TYPE_LEN = 3
NMEA_FIRST_DELIMITER_POS = 6
NMEA_MAX_FIELD_LEN = 20
NMEA_FROM_ASTERISK_TRAIL_LEN = 5 # length of asterisk + checksum (as 2 ascii ints) + \r + \n

NMEA_GGA_MSG_ID = b"GGA"
NMEA_GSA_MSG_ID = b"GSA"
NMEA_GLL_MSG_ID = b"GLL"
NMEA_VTG_MSG_ID = b"VTG"
NMEA_GST_MSG_ID = b"GST"
NMEA_GSV_MSG_ID = b"GSV"
NMEA_ZDA_MSG_ID = b"ZDA"
NMEA_TXT_MSG_ID = b"TXT"

###########################
### UBX CLASSES and IDs ###
###########################

# UBX MSG CLASSES
UBX_ACK_CLASS = 0x05
UBX_CFG_CLASS = 0x06
UBX_INF_CLASS = 0x04
UBX_LOG_CLASS = 0x21
UBX_MGA_CLASS = 0x13
UBX_MON_CLASS = 0x0a
UBX_NAV_CLASS = 0x01
UBX_RXM_CLASS = 0x02
UBX_SEC_CLASS = 0x27
UBX_TIM_CLASS = 0x0d
UBX_UPD_CLASS = 0x09

# ACK Class IDs
UBX_ACK_ACK_ID = 0x01
UBX_ACK_NAK_ID = 0x00

# CFG Class IDs
UBX_CFG_ANT_ID = 0x13
UBX_CFG_BATCH_ID = 0x93
UBX_CFG_CFG_ID = 0x09
UBX_CFG_DAT_ID = 0x06
UBX_CFG_GEOFENCE_ID = 0x69
UBX_CFG_GNSS_ID = 0x3E
UBX_CFG_INF_ID = 0x02
UBX_CFG_ITFM_ID = 0x39
UBX_CFG_LOGFILTER_ID = 0x47
UBX_CFG_MSG_ID = 0x01
UBX_CFG_NAV5_ID = 0x24
UBX_CFG_NAVX5_ID = 0x23
UBX_CFG_NMEA_ID = 0x17
UBX_CFG_ODO_ID = 0x1E
UBX_CFG_PM2_ID = 0x3B
UBX_CFG_PMS_ID = 0x86
UBX_CFG_PRT_ID = 0x00
UBX_CFG_PWR_ID = 0x57
UBX_CFG_RATE_ID = 0x08
UBX_CFG_RINV_ID = 0x34
UBX_CFG_RST_ID = 0x04
UBX_CFG_RXM_ID = 0x11
UBX_CFG_SBAS_ID = 0x16
UBX_CFG_TP5_ID = 0x31
UBX_CFG_USB_ID = 0x1B
UBX_CFG_VALDEL_ID = 0x8C
UBX_CFG_VALGET_ID = 0x8B
UBX_CFG_VALSET_ID = 0x8A

# INF Class IDs
UBX_INF_DEBUG_ID = 0x04
UBX_INF_ERROR_ID = 0x00
UBX_INF_NOTICE_ID = 0x02
UBX_INF_TEST_ID = 0x03
UBX_INF_WARNING_ID = 0x01

# LOG Class IDs
UBX_LOG_BATCH_ID = 0x11
UBX_LOG_CREATE_ID = 0x07
UBX_LOG_ERASE_ID = 0x03
UBX_LOG_FINDTIME_ID = 0x0E
UBX_LOG_INFO_ID = 0x08
UBX_LOG_RETRIEVE_ID = 0x09
UBX_LOG_RETRIEVEBATCH_ID = 0x10
UBX_LOG_RETRIEVEPOS_ID = 0x0B
UBX_LOG_RETRIEVEPOSEXTRA_ID = 0x0F
UBX_LOG_RETRIEVESTRING_ID = 0x0D
UBX_LOG_STRING_ID = 0x04

# MGA Class IDs
UBX_MGA_ACK_ID = 0x60
UBX_MGA_ANO_ID = 0x20
UBX_MGA_BDS_ID = 0x03
UBX_MGA_DBD_ID = 0x80
UBX_MGA_FLASH_ID = 0x21
UBX_MGA_GAL_ID = 0x02
UBX_MGA_GLO_ID = 0x06
UBX_MGA_GPS_ID = 0x00
UBX_MGA_INI_ID = 0x40
UBX_MGA_QZSS_ID = 0x05

# MON Class IDs
UBX_MON_BATCH_ID = 0x32
UBX_MON_COMMS_ID = 0x36
UBX_MON_GNSS_ID = 0x28
UBX_MON_HW_ID = 0x09
UBX_MON_HW2_ID = 0x0B
UBX_MON_HW3_ID = 0x37
UBX_MON_IO_ID = 0x02
UBX_MON_MSGPP_ID = 0x06
UBX_MON_PATCH_ID = 0x27
UBX_MON_RF_ID = 0x38
UBX_MON_RXBUF_ID = 0x07
UBX_MON_RXR_ID = 0x21
UBX_MON_SPAN_ID = 0x2B
UBX_MON_TXBUF_ID = 0x08
UBX_MON_VER_ID = 0x04

# NAV Class IDs
UBX_NAV_AOPSTATUS_ID = 0x60
UBX_NAV_CLOCK_ID = 0x22
UBX_NAV_COV_ID = 0x36
UBX_NAV_DOP_ID = 0x04
UBX_NAV_EOE_ID = 0x61
UBX_NAV_GEOFENCE_ID = 0x39
UBX_NAV_ODO_ID = 0x09
UBX_NAV_ORB_ID = 0x34
UBX_NAV_POSECEF_ID = 0x01
UBX_NAV_POSLLH_ID = 0x02
UBX_NAV_PVT_ID = 0x07
UBX_NAV_RESETODO_ID = 0x14
UBX_NAV_SAT_ID = 0x35
UBX_NAV_SBAS_ID = 0x16
UBX_NAV_SIG_ID = 0x43
UBX_NAV_SLAS_ID = 0x42
UBX_NAV_STATUS_ID = 0x03
UBX_NAV_TIMEBDS_ID = 0x24
UBX_NAV_TIMEGAL_ID = 0x25
UBX_NAV_TIMEGLO_ID = 0x23
UBX_NAV_TIMEGPS_ID = 0x20
UBX_NAV_TIMELS_ID = 0x26
UBX_NAV_TIMEQZSS_ID = 0x27
UBX_NAV_TIMEUTC_ID = 0x21
UBX_NAV_VELECEF_ID = 0x11
UBX_NAV_VELNED_ID = 0x12

# RXM Class IDs
UBX_RXM_MEASX_ID = 0x14
UBX_RXM_PMREQ_ID = 0x41
UBX_RXM_RLM_ID = 0x59
UBX_RXM_RTCM_ID = 0x32
UBX_RXM_SFRBX_ID = 0x13

# SEC Class IDs
UBX_SEC_UNIQID_ID = 0x03

# TIM Class IDs
UBX_TIM_TM2_ID = 0x03
UBX_TIM_TP_ID = 0x01
UBX_TIM_VRFY_ID = 0x06

# UPD Class IDs
UBX_UPD_SOS_ID = 0x14

# Supported UBX messages
SUPPORTED_UBX_MSGS = {
    UBX_ACK_CLASS: [UBX_ACK_NAK_ID, UBX_ACK_ACK_ID],
    UBX_CFG_CLASS: [
        UBX_CFG_ANT_ID, UBX_CFG_BATCH_ID, UBX_CFG_CFG_ID, UBX_CFG_DAT_ID,
        UBX_CFG_GEOFENCE_ID, UBX_CFG_GNSS_ID, UBX_CFG_INF_ID, UBX_CFG_ITFM_ID,
        UBX_CFG_LOGFILTER_ID, UBX_CFG_MSG_ID, UBX_CFG_NAV5_ID, UBX_CFG_NAVX5_ID,
        UBX_CFG_NMEA_ID, UBX_CFG_ODO_ID, UBX_CFG_PM2_ID, UBX_CFG_PMS_ID,
        UBX_CFG_PRT_ID, UBX_CFG_PWR_ID, UBX_CFG_RATE_ID, UBX_CFG_RINV_ID,
        UBX_CFG_RST_ID, UBX_CFG_RXM_ID, UBX_CFG_SBAS_ID, UBX_CFG_TP5_ID,
        UBX_CFG_USB_ID, UBX_CFG_VALDEL_ID, UBX_CFG_VALGET_ID, UBX_CFG_VALSET_ID
    ],
    UBX_INF_CLASS: [
        UBX_INF_ERROR_ID, UBX_INF_WARNING_ID, UBX_INF_NOTICE_ID,
        UBX_INF_TEST_ID, UBX_INF_DEBUG_ID
    ],
    UBX_LOG_CLASS: [
        UBX_LOG_BATCH_ID, UBX_LOG_CREATE_ID, UBX_LOG_ERASE_ID,
        UBX_LOG_FINDTIME_ID, UBX_LOG_INFO_ID, UBX_LOG_RETRIEVE_ID,
        UBX_LOG_RETRIEVEBATCH_ID, UBX_LOG_RETRIEVEPOS_ID,
        UBX_LOG_RETRIEVEPOSEXTRA_ID, UBX_LOG_RETRIEVESTRING_ID,
        UBX_LOG_STRING_ID
    ],
    UBX_MGA_CLASS: [
        UBX_MGA_ACK_ID, UBX_MGA_ANO_ID, UBX_MGA_BDS_ID, UBX_MGA_DBD_ID,
        UBX_MGA_FLASH_ID, UBX_MGA_GAL_ID, UBX_MGA_GLO_ID, UBX_MGA_GPS_ID,
        UBX_MGA_INI_ID, UBX_MGA_QZSS_ID
    ],
    UBX_MON_CLASS: [
        UBX_MON_BATCH_ID, UBX_MON_COMMS_ID, UBX_MON_GNSS_ID, UBX_MON_HW_ID,
        UBX_MON_HW2_ID, UBX_MON_HW3_ID, UBX_MON_IO_ID, UBX_MON_MSGPP_ID,
        UBX_MON_PATCH_ID, UBX_MON_RF_ID, UBX_MON_RXBUF_ID, UBX_MON_RXR_ID,
        UBX_MON_SPAN_ID, UBX_MON_TXBUF_ID, UBX_MON_VER_ID
    ],
    UBX_NAV_CLASS: [
        UBX_NAV_AOPSTATUS_ID, UBX_NAV_CLOCK_ID, UBX_NAV_COV_ID, UBX_NAV_DOP_ID,
        UBX_NAV_EOE_ID, UBX_NAV_GEOFENCE_ID, UBX_NAV_ODO_ID, UBX_NAV_ORB_ID,
        UBX_NAV_POSECEF_ID, UBX_NAV_POSLLH_ID, UBX_NAV_PVT_ID,
        UBX_NAV_RESETODO_ID, UBX_NAV_SAT_ID, UBX_NAV_SBAS_ID, UBX_NAV_SIG_ID,
        UBX_NAV_SLAS_ID, UBX_NAV_STATUS_ID, UBX_NAV_TIMEBDS_ID,
        UBX_NAV_TIMEGAL_ID, UBX_NAV_TIMEGLO_ID, UBX_NAV_TIMEGPS_ID,
        UBX_NAV_TIMELS_ID, UBX_NAV_TIMEQZSS_ID, UBX_NAV_TIMEUTC_ID,
        UBX_NAV_VELECEF_ID, UBX_NAV_VELNED_ID
    ],
    UBX_RXM_CLASS: [
        UBX_RXM_MEASX_ID, UBX_RXM_PMREQ_ID, UBX_RXM_RLM_ID,
        UBX_RXM_RTCM_ID, UBX_RXM_SFRBX_ID
    ],
    UBX_SEC_CLASS: [UBX_SEC_UNIQID_ID],
    UBX_TIM_CLASS: [UBX_TIM_TM2_ID, UBX_TIM_TP_ID, UBX_TIM_VRFY_ID],
    UBX_UPD_CLASS: [UBX_UPD_SOS_ID]
}

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

def default_dc_reset(instance):
    for f in fields(instance):
        if f.default is not MISSING:
            setattr(instance, f.name, f.default)
        elif f.default_factory is not MISSING:
            setattr(instance, f.name, f.default_factory())
        else:
            setattr(instance, f.name, None)

def get_cfg_by_name(cfgdb, cfg_name):
    for keyId, cfg_data in cfgdb.items():
        if cfg_name == cfg_data["name"]:
            return cfg_data
    return None
