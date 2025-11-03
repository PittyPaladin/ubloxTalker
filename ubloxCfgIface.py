import copy
from ubloxDefines import CFG_VAL_UNKNOWN, APP_SPECIFIC_CFG

###################################
### UBX Configuration Interface ###
###################################

# Expected value for every item in UBX_DEFAULT_CFG is,
# of course, the default one defined in the ICD
UBX_COMPLETE_ICD_DEFAULT_CFG = {
    # CFG-ANA section
    # ---------------------
    0x10230001: {
        "name":"CFG-ANA-USE_ANA",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30230002: {
        "name":"CFG-ANA-ORBMAXERR",
        "type": "U2",
        "expectedVal": 100,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-BATCH section
    # ---------------------
    0x10260013: {
        "name":"CFG-BATCH-ENABLE",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10260014: {
        "name":"CFG-BATCH-PIOENABLE",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30260015: {
        "name":"CFG-BATCH-MAXENTRIES",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30260016: {
        "name":"CFG-BATCH-WARNTHRS",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10260018: {
        "name":"CFG-BATCH-PIOACTIVELOW",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20260019: {
        "name":"CFG-BATCH-PIOID",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1026001A: {
        "name":"CFG-BATCH-EXTRAPVT",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1026001B: {
        "name":"CFG-BATCH-EXTRAODO",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-GEOFENCE section
    # ---------------------
    0x20240011: {
        "name":"CFG-GEOFENCE-CONFLVL",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10240012: {
        "name":"CFG-GEOFENCE-USE_PIO",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20240013: {
        "name":"CFG-GEOFENCE-PINPOL",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20240014: {
        "name":"CFG-GEOFENCE-PIN",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10240020: {
        "name":"CFG-GEOFENCE-USE_FENCE1",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240021: {
        "name":"CFG-GEOFENCE-FENCE1_LAT",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240022: {
        "name":"CFG-GEOFENCE-FENCE1_LON",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240023: {
        "name":"CFG-GEOFENCE-FENCE1_RAD",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10240030: {
        "name":"CFG-GEOFENCE-USE_FENCE2",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240031: {
        "name":"CFG-GEOFENCE-FENCE2_LAT",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240032: {
        "name":"CFG-GEOFENCE-FENCE2_LON",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240033: {
        "name":"CFG-GEOFENCE-FENCE2_RAD",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10240040: {
        "name":"CFG-GEOFENCE-USE_FENCE3",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240041: {
        "name":"CFG-GEOFENCE-FENCE3_LAT",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240042: {
        "name":"CFG-GEOFENCE-FENCE3_LON",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240043: {
        "name":"CFG-GEOFENCE-FENCE3_RAD",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10240050: {
        "name":"CFG-GEOFENCE-USE_FENCE4",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240051: {
        "name":"CFG-GEOFENCE-FENCE4_LAT",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240052: {
        "name":"CFG-GEOFENCE-FENCE4_LON",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40240053: {
        "name":"CFG-GEOFENCE-FENCE4_RAD",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-HW section
    # ---------------------
    0x10A3002E: {
        "name":"CFG-HW-ANT_CFG_VOLTCTRL",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A3002F: {
        "name":"CFG-HW-ANT_CFG_SHORTDET",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30030: {
        "name":"CFG-HW-ANT_CFG_SHORTDET_POL",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30031: {
        "name":"CFG-HW-ANT_CFG_OPENDET",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30032: {
        "name":"CFG-HW-ANT_CFG_OPENDET_POL",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30033: {
        "name":"CFG-HW-ANT_CFG_PWRDOWN",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30034: {
        "name":"CFG-HW-ANT_CFG_PWRDOWN_POL",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10A30035: {
        "name":"CFG-HW-ANT_CFG_RECOVER",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30036: {
        "name":"CFG-HW-ANT_SUP_SWITCH_PIN",
        "type": "U1",
        "expectedVal": 16,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30037: {
        "name":"CFG-HW-ANT_SUP_SHORT_PIN",
        "type": "U1",
        "expectedVal": 15,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30038: {
        "name":"CFG-HW-ANT_SUP_OPEN_PIN",
        "type": "U1",
        "expectedVal": 8,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30A3003C: {
        "name":"CFG-HW-ANT_ON_SHORT_US",
        "type": "U2",
        "expectedVal": 500,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30054: {
        "name":"CFG-HW-ANT_SUP_ENGINE",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30055: {
        "name":"CFG-HW-ANT_SUP_SHORT_THR",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20A30056: {
        "name":"CFG-HW-ANT_SUP_OPEN_THR",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-I2C section
    # ---------------------
    0x20510001: {
        "name":"CFG-I2C-ADDRESS",
        "type": "U1",
        "expectedVal": 132,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10510002: {
        "name":"CFG-I2C-EXTENDEDTIMEOUT",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10510003: {
        "name":"CFG-I2C-ENABLED",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-I2CINPROT section
    # ---------------------
    0x10710001: {
        "name":"CFG-I2CINPROT-UBX",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10710002: {
        "name":"CFG-I2CINPROT-NMEA",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10710004: {
        "name":"CFG-I2CINPROT-RTCM3X",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-I2COUTPROT section
    # ---------------------
    0x10720001: {
        "name":"CFG-I2COUTPROT-UBX",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10720002: {
        "name":"CFG-I2COUTPROT-NMEA",
        "type": "L",
        "expectedVal": True,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-INFMSG section
    # ---------------------
    0x20920001: {
        "name":"CFG-INFMSG-UBX_I2C",
        "type": "X1",
        "expectedVal": 0x00,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920002: {
        "name":"CFG-INFMSG-UBX_UART1",
        "type": "X1",
        "expectedVal": 0x00,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920003: {
        "name":"CFG-INFMSG-UBX_UART2",
        "type": "X1",
        "expectedVal": 0x00,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920004: {
        "name":"CFG-INFMSG-UBX_USB",
        "type": "X1",
        "expectedVal": 0x00,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920005: {
        "name":"CFG-INFMSG-UBX_SPI",
        "type": "X1",
        "expectedVal": 0x00,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920006: {
        "name":"CFG-INFMSG-NMEA_I2C",
        "type": "X1",
        "expectedVal": 0x07,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920007: {
        "name":"CFG-INFMSG-NMEA_UART1",
        "type": "X1",
        "expectedVal": 0x07,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920008: {
        "name":"CFG-INFMSG-NMEA_UART2",
        "type": "X1",
        "expectedVal": 0x07,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20920009: {
        "name":"CFG-INFMSG-NMEA_USB",
        "type": "X1",
        "expectedVal": 0x07,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2092000A: {
        "name":"CFG-INFMSG-NMEA_SPI",
        "type": "X1",
        "expectedVal": 0x07,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-ITFM section
    # ---------------------
    0x20410001: {
        "name":"CFG-ITFM-BBTHRESHOLD",
        "type": "U1",
        "expectedVal": 3,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20410002: {
        "name":"CFG-ITFM-CWTHRESHOLD",
        "type": "U1",
        "expectedVal": 15,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1041000D: {
        "name":"CFG-ITFM-ENABLE",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20410010: {
        "name":"CFG-ITFM-ANTSETTING",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10410013: {
        "name":"CFG-ITFM-ENABLE_AUX",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-LOGFILTER section
    # ---------------------
    0x10DE0002: {
        "name":"CFG-LOGFILTER-RECORD_ENA",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10DE0003: {
        "name":"CFG-LOGFILTER-ONCE_PER_WAKE_UP_ENA",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10DE0004: {
        "name":"CFG-LOGFILTER-APPLY_ALL_FILTERS",
        "type": "L",
        "expectedVal": False,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30DE0005: {
        "name":"CFG-LOGFILTER-MIN_INTERVAL",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30DE0006: {
        "name":"CFG-LOGFILTER-TIME_THRS",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30DE0007: {
        "name":"CFG-LOGFILTER-SPEED_THRS",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40DE0008: {
        "name":"CFG-LOGFILTER-POSITION_THRS",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-MOT section
    # ---------------------
    0x20250038: {
        "name":"CFG-MOT-GNSSSPEED_THRS",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x3025003B: {
        "name":"CFG-MOT-GNSSDIST_THRS",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-MSGOUT section
    # ---------------------
    # NMEA DTM
    0x209100A6: {
        "name":"CFG-MSGOUT-NMEA_ID_DTM_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100AA: {
        "name":"CFG-MSGOUT-NMEA_ID_DTM_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A7: {
        "name":"CFG-MSGOUT-NMEA_ID_DTM_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A8: {
        "name":"CFG-MSGOUT-NMEA_ID_DTM_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A9: {
        "name":"CFG-MSGOUT-NMEA_ID_DTM_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GBS
    0x209100DD: {
        "name":"CFG-MSGOUT-NMEA_ID_GBS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100E1: {
        "name":"CFG-MSGOUT-NMEA_ID_GBS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100DE: {
        "name":"CFG-MSGOUT-NMEA_ID_GBS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100DF: {
        "name":"CFG-MSGOUT-NMEA_ID_GBS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100E0: {
        "name":"CFG-MSGOUT-NMEA_ID_GBS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GGA
    0x209100BA: {
        "name":"CFG-MSGOUT-NMEA_ID_GGA_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100BE: {
        "name":"CFG-MSGOUT-NMEA_ID_GGA_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100BB: {
        "name":"CFG-MSGOUT-NMEA_ID_GGA_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100BC: {
        "name":"CFG-MSGOUT-NMEA_ID_GGA_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100BD: {
        "name":"CFG-MSGOUT-NMEA_ID_GGA_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    # NMEA GLL
    0x209100C9: {
        "name":"CFG-MSGOUT-NMEA_ID_GLL_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100CD: {
        "name":"CFG-MSGOUT-NMEA_ID_GLL_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100CA: {
        "name":"CFG-MSGOUT-NMEA_ID_GLL_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100CB: {
        "name":"CFG-MSGOUT-NMEA_ID_GLL_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100CC: {
        "name":"CFG-MSGOUT-NMEA_ID_GLL_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GNS
    0x209100B5: {
        "name":"CFG-MSGOUT-NMEA_ID_GNS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100B9: {
        "name":"CFG-MSGOUT-NMEA_ID_GNS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100B6: {
        "name":"CFG-MSGOUT-NMEA_ID_GNS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100B7: {
        "name":"CFG-MSGOUT-NMEA_ID_GNS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100B8: {
        "name":"CFG-MSGOUT-NMEA_ID_GNS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GRS
    0x209100CE: {
        "name":"CFG-MSGOUT-NMEA_ID_GRS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D2: {
        "name":"CFG-MSGOUT-NMEA_ID_GRS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100CF: {
        "name":"CFG-MSGOUT-NMEA_ID_GRS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D0: {
        "name":"CFG-MSGOUT-NMEA_ID_GRS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D1: {
        "name":"CFG-MSGOUT-NMEA_ID_GRS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GSA
    0x209100BF: {
        "name":"CFG-MSGOUT-NMEA_ID_GSA_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C3: {
        "name":"CFG-MSGOUT-NMEA_ID_GSA_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C0: {
        "name":"CFG-MSGOUT-NMEA_ID_GSA_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C1: {
        "name":"CFG-MSGOUT-NMEA_ID_GSA_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C2: {
        "name":"CFG-MSGOUT-NMEA_ID_GSA_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GST
    0x209100D3: {
        "name":"CFG-MSGOUT-NMEA_ID_GST_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D7: {
        "name":"CFG-MSGOUT-NMEA_ID_GST_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D4: {
        "name":"CFG-MSGOUT-NMEA_ID_GST_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D5: {
        "name":"CFG-MSGOUT-NMEA_ID_GST_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100D6: {
        "name":"CFG-MSGOUT-NMEA_ID_GST_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA GSV
    0x209100C4: {
        "name":"CFG-MSGOUT-NMEA_ID_GSV_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C8: {
        "name":"CFG-MSGOUT-NMEA_ID_GSV_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C5: {
        "name":"CFG-MSGOUT-NMEA_ID_GSV_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C6: {
        "name":"CFG-MSGOUT-NMEA_ID_GSV_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100C7: {
        "name":"CFG-MSGOUT-NMEA_ID_GSV_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA RLM
    0x20910400: {
        "name":"CFG-MSGOUT-NMEA_ID_RLM_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910404: {
        "name":"CFG-MSGOUT-NMEA_ID_RLM_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910401: {
        "name":"CFG-MSGOUT-NMEA_ID_RLM_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910402: {
        "name":"CFG-MSGOUT-NMEA_ID_RLM_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910403: {
        "name":"CFG-MSGOUT-NMEA_ID_RLM_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA RMC
    0x209100ab: {
        "name":"CFG-MSGOUT-NMEA_ID_RMC_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100af: {
        "name":"CFG-MSGOUT-NMEA_ID_RMC_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ac: {
        "name":"CFG-MSGOUT-NMEA_ID_RMC_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ad: {
        "name":"CFG-MSGOUT-NMEA_ID_RMC_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ae: {
        "name":"CFG-MSGOUT-NMEA_ID_RMC_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA VLW
    0x209100E7: {
        "name":"CFG-MSGOUT-NMEA_ID_VLW_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100EB: {
        "name":"CFG-MSGOUT-NMEA_ID_VLW_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100E8: {
        "name":"CFG-MSGOUT-NMEA_ID_VLW_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100E9: {
        "name":"CFG-MSGOUT-NMEA_ID_VLW_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100EA: {
        "name":"CFG-MSGOUT-NMEA_ID_VLW_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA VTG
    0x209100b0: {
        "name":"CFG-MSGOUT-NMEA_ID_VTG_I2C",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100b4: {
        "name":"CFG-MSGOUT-NMEA_ID_VTG_SPI",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100b1: {
        "name":"CFG-MSGOUT-NMEA_ID_VTG_UART1",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100b2: {
        "name":"CFG-MSGOUT-NMEA_ID_VTG_UART2",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100b3: {
        "name":"CFG-MSGOUT-NMEA_ID_VTG_USB",
        "type": "U1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NMEA ZDA
    0x209100d8: {
        "name":"CFG-MSGOUT-NMEA_ID_ZDA_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100dc: {
        "name":"CFG-MSGOUT-NMEA_ID_ZDA_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100d9: {
        "name":"CFG-MSGOUT-NMEA_ID_ZDA_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100da: {
        "name":"CFG-MSGOUT-NMEA_ID_ZDA_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100db: {
        "name":"CFG-MSGOUT-NMEA_ID_ZDA_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # PUBX POLYP
    0x209100ec: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYP_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100f0: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYP_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ed: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYP_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ee: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYP_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100ef: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYP_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # PUBX POLYS
    0x209100F1: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F5: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F2: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F3: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F4: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # PUBX POLYT
    0x209100F6: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYT_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100FA: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYT_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F7: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYT_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F8: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYT_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100F9: {
        "name":"CFG-MSGOUT-PUBX_ID_POLYT_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # LOG INFO
    0x20910259: {
        "name":"CFG-MSGOUT-UBX_LOG_INFO_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091025D: {
        "name":"CFG-MSGOUT-UBX_LOG_INFO_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091025A: {
        "name":"CFG-MSGOUT-UBX_LOG_INFO_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091025B: {
        "name":"CFG-MSGOUT-UBX_LOG_INFO_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091025C: {
        "name":"CFG-MSGOUT-UBX_LOG_INFO_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON COMMS
    0x2091034F: {
        "name":"CFG-MSGOUT-UBX_MON_COMMS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910353: {
        "name":"CFG-MSGOUT-UBX_MON_COMMS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910350: {
        "name":"CFG-MSGOUT-UBX_MON_COMMS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910351: {
        "name":"CFG-MSGOUT-UBX_MON_COMMS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910352: {
        "name":"CFG-MSGOUT-UBX_MON_COMMS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON HW2
    0x209101B9: {
        "name":"CFG-MSGOUT-UBX_MON_HW2_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101BD: {
        "name":"CFG-MSGOUT-UBX_MON_HW2_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101BA: {
        "name":"CFG-MSGOUT-UBX_MON_HW2_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101BB: {
        "name":"CFG-MSGOUT-UBX_MON_HW2_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101BC: {
        "name":"CFG-MSGOUT-UBX_MON_HW2_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910354: {
        "name":"CFG-MSGOUT-UBX_MON_HW3_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910358: {
        "name":"CFG-MSGOUT-UBX_MON_HW3_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910355: {
        "name":"CFG-MSGOUT-UBX_MON_HW3_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910356: {
        "name":"CFG-MSGOUT-UBX_MON_HW3_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910357: {
        "name":"CFG-MSGOUT-UBX_MON_HW3_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101B4: {
        "name":"CFG-MSGOUT-UBX_MON_HW_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101B8: {
        "name":"CFG-MSGOUT-UBX_MON_HW_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101B5: {
        "name":"CFG-MSGOUT-UBX_MON_HW_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101B6: {
        "name":"CFG-MSGOUT-UBX_MON_HW_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101B7: {
        "name":"CFG-MSGOUT-UBX_MON_HW_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A5: {
        "name":"CFG-MSGOUT-UBX_MON_IO_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A9: {
        "name":"CFG-MSGOUT-UBX_MON_IO_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A6: {
        "name":"CFG-MSGOUT-UBX_MON_IO_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A7: {
        "name":"CFG-MSGOUT-UBX_MON_IO_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A8: {
        "name":"CFG-MSGOUT-UBX_MON_IO_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON MSGPP
    0x20910196: {
        "name":"CFG-MSGOUT-UBX_MON_MSGPP_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091019A: {
        "name":"CFG-MSGOUT-UBX_MON_MSGPP_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910197: {
        "name":"CFG-MSGOUT-UBX_MON_MSGPP_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910198: {
        "name":"CFG-MSGOUT-UBX_MON_MSGPP_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910199: {
        "name":"CFG-MSGOUT-UBX_MON_MSGPP_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON RF
    0x20910359: {
        "name":"CFG-MSGOUT-UBX_MON_RF_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091035D: {
        "name":"CFG-MSGOUT-UBX_MON_RF_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091035A: {
        "name":"CFG-MSGOUT-UBX_MON_RF_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091035B: {
        "name":"CFG-MSGOUT-UBX_MON_RF_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091035C: {
        "name":"CFG-MSGOUT-UBX_MON_RF_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON RXBUF
    0x209101A0: {
        "name":"CFG-MSGOUT-UBX_MON_RXBUF_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A4: {
        "name":"CFG-MSGOUT-UBX_MON_RXBUF_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A1: {
        "name":"CFG-MSGOUT-UBX_MON_RXBUF_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A2: {
        "name":"CFG-MSGOUT-UBX_MON_RXBUF_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209101A3: {
        "name":"CFG-MSGOUT-UBX_MON_RXBUF_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON RXR
    0x20910187: {
        "name":"CFG-MSGOUT-UBX_MON_RXR_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091018B: {
        "name":"CFG-MSGOUT-UBX_MON_RXR_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910188: {
        "name":"CFG-MSGOUT-UBX_MON_RXR_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910189: {
        "name":"CFG-MSGOUT-UBX_MON_RXR_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091018A: {
        "name":"CFG-MSGOUT-UBX_MON_RXR_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON SPAN
    0x2091038B: {
        "name":"CFG-MSGOUT-UBX_MON_SPAN_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091038F: {
        "name":"CFG-MSGOUT-UBX_MON_SPAN_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091038C: {
        "name":"CFG-MSGOUT-UBX_MON_SPAN_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091038D: {
        "name":"CFG-MSGOUT-UBX_MON_SPAN_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091038E: {
        "name":"CFG-MSGOUT-UBX_MON_SPAN_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # MON TXBUF
    0x2091019B: {
        "name":"CFG-MSGOUT-UBX_MON_TXBUF_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091019F: {
        "name":"CFG-MSGOUT-UBX_MON_TXBUF_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091019C: {
        "name":"CFG-MSGOUT-UBX_MON_TXBUF_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091019D: {
        "name":"CFG-MSGOUT-UBX_MON_TXBUF_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091019E: {
        "name":"CFG-MSGOUT-UBX_MON_TXBUF_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV AOPSTATUS
    0x20910079: {
        "name":"CFG-MSGOUT-UBX_NAV_AOPSTATUS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091007D: {
        "name":"CFG-MSGOUT-UBX_NAV_AOPSTATUS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091007A: {
        "name":"CFG-MSGOUT-UBX_NAV_AOPSTATUS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091007B: {
        "name":"CFG-MSGOUT-UBX_NAV_AOPSTATUS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091007C: {
        "name":"CFG-MSGOUT-UBX_NAV_AOPSTATUS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV CLOCK
    0x20910065: {
        "name":"CFG-MSGOUT-UBX_NAV_CLOCK_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910069: {
        "name":"CFG-MSGOUT-UBX_NAV_CLOCK_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910066: {
        "name":"CFG-MSGOUT-UBX_NAV_CLOCK_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910067: {
        "name":"CFG-MSGOUT-UBX_NAV_CLOCK_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910068: {
        "name":"CFG-MSGOUT-UBX_NAV_CLOCK_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV COV
    0x20910083: {
        "name":"CFG-MSGOUT-UBX_NAV_COV_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910087: {
        "name":"CFG-MSGOUT-UBX_NAV_COV_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910084: {
        "name":"CFG-MSGOUT-UBX_NAV_COV_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910085: {
        "name":"CFG-MSGOUT-UBX_NAV_COV_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910086: {
        "name":"CFG-MSGOUT-UBX_NAV_COV_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV DOP
    0x20910038: {
        "name":"CFG-MSGOUT-UBX_NAV_DOP_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091003C: {
        "name":"CFG-MSGOUT-UBX_NAV_DOP_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910039: {
        "name":"CFG-MSGOUT-UBX_NAV_DOP_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091003A: {
        "name":"CFG-MSGOUT-UBX_NAV_DOP_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091003B: {
        "name":"CFG-MSGOUT-UBX_NAV_DOP_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV EOE
    0x2091015F: {
        "name":"CFG-MSGOUT-UBX_NAV_EOE_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910163: {
        "name":"CFG-MSGOUT-UBX_NAV_EOE_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910160: {
        "name":"CFG-MSGOUT-UBX_NAV_EOE_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910161: {
        "name":"CFG-MSGOUT-UBX_NAV_EOE_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910162: {
        "name":"CFG-MSGOUT-UBX_NAV_EOE_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV GEOFENCE
    0x209100A1: {
        "name":"CFG-MSGOUT-UBX_NAV_GEOFENCE_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A5: {
        "name":"CFG-MSGOUT-UBX_NAV_GEOFENCE_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A2: {
        "name":"CFG-MSGOUT-UBX_NAV_GEOFENCE_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A3: {
        "name":"CFG-MSGOUT-UBX_NAV_GEOFENCE_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209100A4: {
        "name":"CFG-MSGOUT-UBX_NAV_GEOFENCE_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV ODO
    0x2091007E: {
        "name":"CFG-MSGOUT-UBX_NAV_ODO_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910082: {
        "name":"CFG-MSGOUT-UBX_NAV_ODO_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091007F: {
        "name":"CFG-MSGOUT-UBX_NAV_ODO_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910080: {
        "name":"CFG-MSGOUT-UBX_NAV_ODO_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910081: {
        "name":"CFG-MSGOUT-UBX_NAV_ODO_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV ORB
    0x20910010: {
        "name":"CFG-MSGOUT-UBX_NAV_ORB_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910014: {
        "name":"CFG-MSGOUT-UBX_NAV_ORB_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910011: {
        "name":"CFG-MSGOUT-UBX_NAV_ORB_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910012: {
        "name":"CFG-MSGOUT-UBX_NAV_ORB_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910013: {
        "name":"CFG-MSGOUT-UBX_NAV_ORB_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV POSECEF
    0x20910024: {
        "name":"CFG-MSGOUT-UBX_NAV_POSECEF_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910028: {
        "name":"CFG-MSGOUT-UBX_NAV_POSECEF_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910025: {
        "name":"CFG-MSGOUT-UBX_NAV_POSECEF_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910026: {
        "name":"CFG-MSGOUT-UBX_NAV_POSECEF_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910027: {
        "name":"CFG-MSGOUT-UBX_NAV_POSECEF_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV POSLLH
    0x20910029: {
        "name":"CFG-MSGOUT-UBX_NAV_POSLLH_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091002D: {
        "name":"CFG-MSGOUT-UBX_NAV_POSLLH_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091002A: {
        "name":"CFG-MSGOUT-UBX_NAV_POSLLH_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091002B: {
        "name":"CFG-MSGOUT-UBX_NAV_POSLLH_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091002C: {
        "name":"CFG-MSGOUT-UBX_NAV_POSLLH_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV PVT
    0x20910006: {
        "name":"CFG-MSGOUT-UBX_NAV_PVT_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091000A: {
        "name":"CFG-MSGOUT-UBX_NAV_PVT_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910007: {
        "name":"CFG-MSGOUT-UBX_NAV_PVT_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910008: {
        "name":"CFG-MSGOUT-UBX_NAV_PVT_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910009: {
        "name":"CFG-MSGOUT-UBX_NAV_PVT_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV SAT
    0x20910015: {
        "name":"CFG-MSGOUT-UBX_NAV_SAT_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910019: {
        "name":"CFG-MSGOUT-UBX_NAV_SAT_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910016: {
        "name":"CFG-MSGOUT-UBX_NAV_SAT_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910017: {
        "name":"CFG-MSGOUT-UBX_NAV_SAT_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910018: {
        "name":"CFG-MSGOUT-UBX_NAV_SAT_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV SBAS
    0x2091006A: {
        "name":"CFG-MSGOUT-UBX_NAV_SBAS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091006E: {
        "name":"CFG-MSGOUT-UBX_NAV_SBAS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091006B: {
        "name":"CFG-MSGOUT-UBX_NAV_SBAS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091006C: {
        "name":"CFG-MSGOUT-UBX_NAV_SBAS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091006D: {
        "name":"CFG-MSGOUT-UBX_NAV_SBAS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV SIG
    0x20910345: {
        "name":"CFG-MSGOUT-UBX_NAV_SIG_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910349: {
        "name":"CFG-MSGOUT-UBX_NAV_SIG_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910346: {
        "name":"CFG-MSGOUT-UBX_NAV_SIG_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910347: {
        "name":"CFG-MSGOUT-UBX_NAV_SIG_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910348: {
        "name":"CFG-MSGOUT-UBX_NAV_SIG_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV SLAS
    0x20910336: {
        "name":"CFG-MSGOUT-UBX_NAV_SLAS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091033A: {
        "name":"CFG-MSGOUT-UBX_NAV_SLAS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910337: {
        "name":"CFG-MSGOUT-UBX_NAV_SLAS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910338: {
        "name":"CFG-MSGOUT-UBX_NAV_SLAS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910339: {
        "name":"CFG-MSGOUT-UBX_NAV_SLAS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV STATUS
    0x2091001a: {
        "name":"CFG-MSGOUT-UBX_NAV_STATUS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091001e: {
        "name":"CFG-MSGOUT-UBX_NAV_STATUS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091001b: {
        "name":"CFG-MSGOUT-UBX_NAV_STATUS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091001c: {
        "name":"CFG-MSGOUT-UBX_NAV_STATUS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091001d: {
        "name":"CFG-MSGOUT-UBX_NAV_STATUS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEBDS
    0x20910051: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEBDS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910055: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEBDS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910052: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEBDS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910053: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEBDS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910054: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEBDS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEGAL
    0x20910056: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGAL_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091005a: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGAL_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910057: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGAL_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910058: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGAL_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910059: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGAL_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEGLO
    0x2091004c: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGLO_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910050: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGLO_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091004d: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGLO_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091004e: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGLO_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091004f: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGLO_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEGPS
    0x20910047: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGPS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091004b: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGPS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910048: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGPS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910049: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGPS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091004a: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEGPS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMELS
    0x20910060: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMELS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910064: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMELS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910061: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMELS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910062: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMELS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910063: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMELS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEQZSS
    0x20910386: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEQZSS_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091038a: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEQZSS_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910387: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEQZSS_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910388: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEQZSS_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910389: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEQZSS_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV TIMEUTC
    0x2091005b: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEUTC_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091005f: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEUTC_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091005c: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEUTC_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091005d: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEUTC_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091005e: {
        "name":"CFG-MSGOUT-UBX_NAV_TIMEUTC_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV VELECEF
    0x2091003d: {
        "name":"CFG-MSGOUT-UBX_NAV_VELECEF_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910041: {
        "name":"CFG-MSGOUT-UBX_NAV_VELECEF_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091003e: {
        "name":"CFG-MSGOUT-UBX_NAV_VELECEF_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091003f: {
        "name":"CFG-MSGOUT-UBX_NAV_VELECEF_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910040: {
        "name":"CFG-MSGOUT-UBX_NAV_VELECEF_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # NAV VELNED
    0x20910042: {
        "name":"CFG-MSGOUT-UBX_NAV_VELNED_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910046: {
        "name":"CFG-MSGOUT-UBX_NAV_VELNED_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910043: {
        "name":"CFG-MSGOUT-UBX_NAV_VELNED_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910044: {
        "name":"CFG-MSGOUT-UBX_NAV_VELNED_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910045: {
        "name":"CFG-MSGOUT-UBX_NAV_VELNED_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # RXM MEASX
    0x20910204: {
        "name":"CFG-MSGOUT-UBX_RXM_MEASX_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910208: {
        "name":"CFG-MSGOUT-UBX_RXM_MEASX_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910205: {
        "name":"CFG-MSGOUT-UBX_RXM_MEASX_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910206: {
        "name":"CFG-MSGOUT-UBX_RXM_MEASX_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910207: {
        "name":"CFG-MSGOUT-UBX_RXM_MEASX_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # RXM RAWX
    0x209102a4: {
        "name":"CFG-MSGOUT-UBX_RXM_RAWX_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209102a8: {
        "name":"CFG-MSGOUT-UBX_RXM_RAWX_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209102a5: {
        "name":"CFG-MSGOUT-UBX_RXM_RAWX_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209102a6: {
        "name":"CFG-MSGOUT-UBX_RXM_RAWX_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x209102a7: {
        "name":"CFG-MSGOUT-UBX_RXM_RAWX_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # RXM RLM
    0x2091025e: {
        "name":"CFG-MSGOUT-UBX_RXM_RLM_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910262: {
        "name":"CFG-MSGOUT-UBX_RXM_RLM_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091025f: {
        "name":"CFG-MSGOUT-UBX_RXM_RLM_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910260: {
        "name":"CFG-MSGOUT-UBX_RXM_RLM_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910261: {
        "name":"CFG-MSGOUT-UBX_RXM_RLM_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # RXM RTCM
    0x20910268: {
        "name":"CFG-MSGOUT-UBX_RXM_RTCM_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091026c: {
        "name":"CFG-MSGOUT-UBX_RXM_RTCM_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910269: {
        "name":"CFG-MSGOUT-UBX_RXM_RTCM_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091026a: {
        "name":"CFG-MSGOUT-UBX_RXM_RTCM_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091026b: {
        "name":"CFG-MSGOUT-UBX_RXM_RTCM_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # RXM SFRXB
    0x20910231: {
        "name":"CFG-MSGOUT-UBX_RXM_SFRBX_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910235: {
        "name":"CFG-MSGOUT-UBX_RXM_SFRBX_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910232: {
        "name":"CFG-MSGOUT-UBX_RXM_SFRBX_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910233: {
        "name":"CFG-MSGOUT-UBX_RXM_SFRBX_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910234: {
        "name":"CFG-MSGOUT-UBX_RXM_SFRBX_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # TIM TM2
    0x20910178: {
        "name":"CFG-MSGOUT-UBX_TIM_TM2_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091017c: {
        "name":"CFG-MSGOUT-UBX_TIM_TM2_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910179: {
        "name":"CFG-MSGOUT-UBX_TIM_TM2_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091017a: {
        "name":"CFG-MSGOUT-UBX_TIM_TM2_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091017b: {
        "name":"CFG-MSGOUT-UBX_TIM_TM2_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # TIM TP
    0x2091017d: {
        "name":"CFG-MSGOUT-UBX_TIM_TP_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910181: {
        "name":"CFG-MSGOUT-UBX_TIM_TP_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091017e: {
        "name":"CFG-MSGOUT-UBX_TIM_TP_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2091017f: {
        "name":"CFG-MSGOUT-UBX_TIM_TP_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910180: {
        "name":"CFG-MSGOUT-UBX_TIM_TP_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # TIM VRFY
    0x20910092: {
        "name":"CFG-MSGOUT-UBX_TIM_VRFY_I2C",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910096: {
        "name":"CFG-MSGOUT-UBX_TIM_VRFY_SPI",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910093: {
        "name":"CFG-MSGOUT-UBX_TIM_VRFY_UART1",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910094: {
        "name":"CFG-MSGOUT-UBX_TIM_VRFY_UART2",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20910095: {
        "name":"CFG-MSGOUT-UBX_TIM_VRFY_USB",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-NAVSPG section
    # ---------------------
    0x20110011: {
        "name":"CFG-NAVSPG-FIXMODE",
        "type": "E1",
        "expectedVal": 3,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10110013: {
        "name":"CFG-NAVSPG-INIFIX3D",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30110017: {
        "name":"CFG-NAVSPG-WKNROLLOVER",
        "type": "U2",
        "expectedVal": 2117,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10110019: {
        "name":"CFG-NAVSPG-USE_PPP",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2011001c: {
        "name":"CFG-NAVSPG-UTCSTANDARD",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20110021: {
        "name":"CFG-NAVSPG-DYNMODEL",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10110025: {
        "name":"CFG-NAVSPG-ACKAIDING",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10110061: {
        "name":"CFG-NAVSPG-USE_USRDAT",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50110062: {
        "name":"CFG-NAVSPG-USRDAT_MAJA",
        "type": "R8",
        "expectedVal": 6378137,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50110063: {
        "name":"CFG-NAVSPG-USRDAT_FLAT",
        "type": "R8",
        "expectedVal": 298.25722356300002502,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110064: {
        "name":"CFG-NAVSPG-USRDAT_DX",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110065: {
        "name":"CFG-NAVSPG-USRDAT_DY",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110066: {
        "name":"CFG-NAVSPG-USRDAT_DZ",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110067: {
        "name":"CFG-NAVSPG-USRDAT_ROTX",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110068: {
        "name":"CFG-NAVSPG-USRDAT_ROTY",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40110069: {
        "name":"CFG-NAVSPG-USRDAT_ROTZ",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x4011006a: {
        "name":"CFG-NAVSPG-USRDAT_SCALE",
        "type": "R4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100a1: {
        "name":"CFG-NAVSPG-INFIL_MINSVS",
        "type": "U1",
        "expectedVal": 3,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100a2: {
        "name":"CFG-NAVSPG-INFIL_MAXSVS",
        "type": "U1",
        "expectedVal": 32,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100a3: {
        "name":"CFG-NAVSPG-INFIL_MINCNO",
        "type": "U1",
        "expectedVal": 6,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100a4: {
        "name":"CFG-NAVSPG-INFIL_MINELEV",
        "type": "I1",
        "expectedVal": 5,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100aa: {
        "name":"CFG-NAVSPG-INFIL_NCNOTHRS",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100ab: {
        "name":"CFG-NAVSPG-INFIL_CNOTHRS",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x301100b1: {
        "name":"CFG-NAVSPG-OUTFIL_PDOP",
        "type": "U2",
        "expectedVal": 250,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x301100b2: {
        "name":"CFG-NAVSPG-OUTFIL_TDOP",
        "type": "U2",
        "expectedVal": 250,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x301100b3: {
        "name":"CFG-NAVSPG-OUTFIL_PACC",
        "type": "U2",
        "expectedVal": 100,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x301100b4: {
        "name":"CFG-NAVSPG-OUTFIL_TACC",
        "type": "U2",
        "expectedVal": 350,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x301100b5: {
        "name":"CFG-NAVSPG-OUTFIL_FACC",
        "type": "U2",
        "expectedVal": 150,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x401100c1: {
        "name":"CFG-NAVSPG-CONSTR_ALT",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x401100c2: {
        "name":"CFG-NAVSPG-CONSTR_ALTVAR",
        "type": "U4",
        "expectedVal": 10000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100c4: {
        "name":"CFG-NAVSPG-CONSTR_DGNSSTO",
        "type": "U1",
        "expectedVal": 60,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x201100d6: {
        "name":"CFG-NAVSPG-SIGATTCOMP",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-NMEA section
    # ---------------------
    0x20930001: {
        "name":"CFG-NMEA-PROTVER",
        "type": "E1",
        "expectedVal": 41,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20930002: {
        "name":"CFG-NMEA-MAXSVS",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930003: {
        "name":"CFG-NMEA-COMPAT",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930004: {
        "name":"CFG-NMEA-CONSIDER",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930005: {
        "name":"CFG-NMEA-LIMIT82",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930006: {
        "name":"CFG-NMEA-HIGHPREC",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20930007: {
        "name":"CFG-NMEA-SVNUMBERING",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930011: {
        "name":"CFG-NMEA-FILT_GPS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930012: {
        "name":"CFG-NMEA-FILT_SBAS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930013: {
        "name":"CFG-NMEA-FILT_GAL",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930015: {
        "name":"CFG-NMEA-FILT_QZSS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930016: {
        "name":"CFG-NMEA-FILT_GLO",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930017: {
        "name":"CFG-NMEA-FILT_BDS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930021: {
        "name":"CFG-NMEA-OUT_INVFIX",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930022: {
        "name":"CFG-NMEA-OUT_MSKFIX",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930023: {
        "name":"CFG-NMEA-OUT_INVTIME",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930024: {
        "name":"CFG-NMEA-OUT_INVDATE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930025: {
        "name":"CFG-NMEA-OUT_ONLYGPS",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10930026: {
        "name":"CFG-NMEA-OUT_FROZENCOG",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20930031: {
        "name":"CFG-NMEA-MAINTALKERID",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20930032: {
        "name":"CFG-NMEA-GSVTALKERID",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30930033: {
        "name":"CFG-NMEA-BDSTALKERID",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-ODO section
    # ---------------------
    0x10220001: {
        "name":"CFG-ODO-USE_ODO",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20220005: {
        "name":"CFG-ODO-PROFILE",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-PM section
    # ---------------------
    0x20d00001: {
        "name":"CFG-PM-OPERATEMODE",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40d00002: {
        "name":"CFG-PM-POSUPDATEPERIOD",
        "type": "U4",
        "expectedVal": 10,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40d00003: {
        "name":"CFG-PM-ACQPERIOD",
        "type": "U4",
        "expectedVal": 10,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40d00004: {
        "name":"CFG-PM-GRIDOFFSET",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30d00005: {
        "name":"CFG-PM-ONTIME",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20d00006: {
        "name":"CFG-PM-MINACQTIME",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20d00007: {
        "name":"CFG-PM-MAXACQTIME",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d00008: {
        "name":"CFG-PM-DONOTENTEROFF",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d00009: {
        "name":"CFG-PM-WAITTIMEFIX",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d0000a: {
        "name":"CFG-PM-UPDATEEPH",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20d0000b: {
        "name":"CFG-PM-EXTINTSEL",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d0000c: {
        "name":"CFG-PM-EXTINTWAKE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d0000d: {
        "name":"CFG-PM-EXTINTBACKUP",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d0000e: {
        "name":"CFG-PM-EXTINTINACTIVE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40d0000f: {
        "name":"CFG-PM-EXTINTINACTIVITY",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10d00010: {
        "name":"CFG-PM-LIMITPEAKCURR",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-QZSS section
    # ---------------------
    0x10370005: {
        "name":"CFG-QZSS-USE_SLAS_DGNSS",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10370006: {
        "name":"CFG-QZSS-USE_SLAS_TESTMODE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10370007: {
        "name":"CFG-QZSS-USE_SLAS_RAIM_UNCORR",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-RATE section
    # ---------------------
    0x30210001: {
        "name":"CFG-RATE-MEAS",
        "type": "U2",
        "expectedVal": 1000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30210002: {
        "name":"CFG-RATE-NAV",
        "type": "U2",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20210003: {
        "name":"CFG-RATE-TIMEREF",
        "type": "E1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-RINV section
    # ---------------------
    0x10c70001: {
        "name":"CFG-RINV-DUMP",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10c70002: {
        "name":"CFG-RINV-BINARY",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20c70003: {
        "name":"CFG-RINV-DATA_SIZE",
        "type": "U1",
        "expectedVal": 22,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50c70004: {
        "name":"CFG-RINV-CHUNK0",
        "type": "X8",
        "expectedVal": 0x203a656369746f4e,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50c70005: {
        "name":"CFG-RINV-CHUNK1",
        "type": "X8",
        "expectedVal": 0x2061746164206f6e,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50c70006: {
        "name":"CFG-RINV-CHUNK2",
        "type": "X8",
        "expectedVal": 0x0000216465766173,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50c70007: {
        "name":"CFG-RINV-CHUNK3",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SBAS
    # ---------------------
    0x10360002: {
        "name":"CFG-SBAS-USE_TESTMODE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10360003: {
        "name":"CFG-SBAS-USE_RANGING",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10360004: {
        "name":"CFG-SBAS-USE_DIFFCORR",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10360005: {
        "name":"CFG-SBAS-USE_INTEGRITY",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50360006: {
        "name":"CFG-SBAS-PRNSCANMASK",
        "type": "X8",
        "expectedVal": 0x0000000000072b88,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SEC section
    # ---------------------
    0x10f60009: {
        "name":"CFG-SEC-CFG_LOCK",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30f6000a: {
        "name":"CFG-SEC-CFG_LOCK_UNLOCKGRP1",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30f6000b: {
        "name":"CFG-SEC-CFG_LOCK_UNLOCKGRP2",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SIGNAL section
    # ---------------------
    0x1031001f: {
        "name":"CFG-SIGNAL-GPS_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310001: {
        "name":"CFG-SIGNAL-GPS_L1CA_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310020: {
        "name":"CFG-SIGNAL-SBAS_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310005: {
        "name":"CFG-SIGNAL-SBAS_L1CA_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310021: {
        "name":"CFG-SIGNAL-GAL_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310007: {
        "name":"CFG-SIGNAL-GAL_E1_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310022: {
        "name":"CFG-SIGNAL-BDS_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1031000d: {
        "name":"CFG-SIGNAL-BDS_B1_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310024: {
        "name":"CFG-SIGNAL-QZSS_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310012: {
        "name":"CFG-SIGNAL-QZSS_L1CA_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310025: {
        "name":"CFG-SIGNAL-GLO_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10310018: {
        "name":"CFG-SIGNAL-GLO_L1_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SPI section
    # ---------------------
    0x20640001: {
        "name":"CFG-SPI-MAXFF",
        "type": "U1",
        "expectedVal": 50,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10640002: {
        "name":"CFG-SPI-CPOLARITY",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10640003: {
        "name":"CFG-SPI-CPHASE",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10640005: {
        "name":"CFG-SPI-EXTENDEDTIMEOUT",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10640006: {
        "name":"CFG-SPI-ENABLED",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SPIINPROT section
    # ---------------------
    0x10790001: {
        "name":"CFG-SPIINPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10790002: {
        "name":"CFG-SPIINPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10790004: {
        "name":"CFG-SPIINPROT-RTCM3X",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-SPIOUTPROT section
    # ---------------------
    0x107a0001: {
        "name":"CFG-SPIOUTPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x107a0002: {
        "name":"CFG-SPIOUTPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-TP section
    # ---------------------
    0x20050023: {
        "name":"CFG-TP-PULSE_DEF",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20050030: {
        "name":"CFG-TP-PULSE_LENGTH_DEF",
        "type": "E1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30050001: {
        "name":"CFG-TP-ANT_CABLEDELAY",
        "type": "I2",
        "expectedVal": 50,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050002: {
        "name":"CFG-TP-PERIOD_TP1",
        "type": "U4",
        "expectedVal": 1000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050003: {
        "name":"CFG-TP-PERIOD_LOCK_TP1",
        "type": "U4",
        "expectedVal": 1000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050024: {
        "name":"CFG-TP-FREQ_TP1",
        "type": "U4",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050025: {
        "name":"CFG-TP-FREQ_LOCK_TP1",
        "type": "U4",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050004: {
        "name":"CFG-TP-LEN_TP1",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050005: {
        "name":"CFG-TP-LEN_LOCK_TP1",
        "type": "U4",
        "expectedVal": 100000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5005002a: {
        "name":"CFG-TP-DUTY_TP1",
        "type": "R8",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5005002b: {
        "name":"CFG-TP-DUTY_LOCK_TP1",
        "type": "R8",
        "expectedVal": 10,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050006: {
        "name":"CFG-TP-USER_DELAY_TP1",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050007: {
        "name":"CFG-TP-TP1_ENA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050008: {
        "name":"CFG-TP-SYNC_GNSS_TP1",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050009: {
        "name":"CFG-TP-USE_LOCKED_TP1",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1005000a: {
        "name":"CFG-TP-ALIGN_TO_TOW_TP1",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x1005000b: {
        "name":"CFG-TP-POL_TP1",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x2005000c: {
        "name":"CFG-TP-TIMEGRID_TP1",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x4005000d: {
        "name":"CFG-TP-PERIOD_TP2",
        "type": "U4",
        "expectedVal": 1000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x4005000e: {
        "name":"CFG-TP-PERIOD_LOCK_TP2",
        "type": "U4",
        "expectedVal": 1000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050026: {
        "name":"CFG-TP-FREQ_TP2",
        "type": "U4",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050027: {
        "name":"CFG-TP-FREQ_LOCK_TP2",
        "type": "U4",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x4005000f: {
        "name":"CFG-TP-LEN_TP2",
        "type": "U4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050010: {
        "name":"CFG-TP-LEN_LOCK_TP2",
        "type": "U4",
        "expectedVal": 100000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5005002c: {
        "name":"CFG-TP-DUTY_TP2",
        "type": "R8",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5005002d: {
        "name":"CFG-TP-DUTY_LOCK_TP2",
        "type": "R8",
        "expectedVal": 10,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x40050011: {
        "name":"CFG-TP-USER_DELAY_TP2",
        "type": "I4",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050012: {
        "name":"CFG-TP-TP2_ENA",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050013: {
        "name":"CFG-TP-SYNC_GNSS_TP2",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050014: {
        "name":"CFG-TP-USE_LOCKED_TP2",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050015: {
        "name":"CFG-TP-ALIGN_TO_TOW_TP2",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10050016: {
        "name":"CFG-TP-POL_TP2",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20050017: {
        "name":"CFG-TP-TIMEGRID_TP2",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-TXREADY section
    # ---------------------
    0x10a20001: {
        "name":"CFG-TXREADY-ENABLED",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10a20002: {
        "name":"CFG-TXREADY-POLARITY",
        "type": "L",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20a20003: {
        "name":"CFG-TXREADY-PIN",
        "type": "U1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x30a20004: {
        "name":"CFG-TXREADY-THRESHOLD",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20a20005: {
        "name":"CFG-TXREADY-INTERFACE",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART1 section
    # ---------------------
    0x40520001: {
        "name":"CFG-UART1-BAUDRATE",
        "type": "U4",
        "expectedVal": 38400,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20520002: {
        "name":"CFG-UART1-STOPBITS",
        "type": "E1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20520003: {
        "name":"CFG-UART1-DATABITS",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20520004: {
        "name":"CFG-UART1-PARITY",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10520005: {
        "name":"CFG-UART1-ENABLED",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART1INPROT section
    # ---------------------
    0x10730001: {
        "name":"CFG-UART1INPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10730002: {
        "name":"CFG-UART1INPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10730004: {
        "name":"CFG-UART1INPROT-RTCM3X",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART1OUTPROT section
    # ---------------------
    0x10740001: {
        "name":"CFG-UART1OUTPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10740002: {
        "name":"CFG-UART1OUTPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART2 section
    # ---------------------
    0x40530001: {
        "name":"CFG-UART2-BAUDRATE",
        "type": "U4",
        "expectedVal": 38400,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20530002: {
        "name":"CFG-UART2-STOPBITS",
        "type": "E1",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20530003: {
        "name":"CFG-UART2-DATABITS",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x20530004: {
        "name":"CFG-UART2-PARITY",
        "type": "E1",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10530005: {
        "name":"CFG-UART2-ENABLED",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART2INPROT section
    # ---------------------
    0x10750001: {
        "name":"CFG-UART2INPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10750002: {
        "name":"CFG-UART2INPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10750004: {
        "name":"CFG-UART2INPROT-RTCM3X",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-UART2OUTPROT section
    # ---------------------
    0x10760001: {
        "name":"CFG-UART2OUTPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10760002: {
        "name":"CFG-UART2OUTPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-USB section
    # ---------------------
    0x10650001: {
        "name":"CFG-USB-ENABLED",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10650002: {
        "name":"CFG-USB-SELFPOW",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x3065000a: {
        "name":"CFG-USB-VENDOR_ID",
        "type": "U2",
        "expectedVal": 5446,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x3065000b: {
        "name":"CFG-USB-PRODUCT_ID",
        "type": "U2",
        "expectedVal": 425,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x3065000c: {
        "name":"CFG-USB-POWER",
        "type": "U2",
        "expectedVal": 0,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5065000d: {
        "name":"CFG-USB-VENDOR_STR0",
        "type": "X8",
        "expectedVal": 0x4120786f6c622d75,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5065000e: {
        "name":"CFG-USB-VENDOR_STR1",
        "type": "X8",
        "expectedVal": 0x2e777777202d2047,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x5065000f: {
        "name":"CFG-USB-VENDOR_STR2",
        "type": "X8",
        "expectedVal": 0x632e786f6c622d75,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650010: {
        "name":"CFG-USB-VENDOR_STR3",
        "type": "X8",
        "expectedVal": 0x0000000000006d6f,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650011: {
        "name":"CFG-USB-PRODUCT_STR0",
        "type": "X8",
        "expectedVal": 0x4720786f6c622d75,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650012: {
        "name":"CFG-USB-PRODUCT_STR1",
        "type": "X8",
        "expectedVal": 0x656365722053534e,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650013: {
        "name":"CFG-USB-PRODUCT_STR2",
        "type": "X8",
        "expectedVal": 0x0000000072657669,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650014: {
        "name":"CFG-USB-PRODUCT_STR3",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650015: {
        "name":"CFG-USB-SERIAL_NO_STR0",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650016: {
        "name":"CFG-USB-SERIAL_NO_STR1",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650017: {
        "name":"CFG-USB-SERIAL_NO_STR2",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x50650018: {
        "name":"CFG-USB-SERIAL_NO_STR3",
        "type": "X8",
        "expectedVal": 0x0000000000000000,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-USBINPROT section
    # ---------------------
    0x10770001: {
        "name":"CFG-USBINPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10770002: {
        "name":"CFG-USBINPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10770004: {
        "name":"CFG-USBINPROT-RTCM3X",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },

    # CFG-USBOUTPROT section
    # ---------------------
    0x10780001: {
        "name":"CFG-USBOUTPROT-UBX",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    },
    0x10780002: {
        "name":"CFG-USBOUTPROT-NMEA",
        "type": "L",
        "expectedVal": 1,
        "actualVal": CFG_VAL_UNKNOWN,
    }
}

# From the default config dictionary, exclude those config items in the
# application-specific configuration dict
UBX_REMAINS_DEFAULT_CFG = copy.deepcopy(UBX_COMPLETE_ICD_DEFAULT_CFG)
for keyId in APP_SPECIFIC_CFG:
    if keyId in UBX_REMAINS_DEFAULT_CFG:
        del UBX_REMAINS_DEFAULT_CFG[keyId]
