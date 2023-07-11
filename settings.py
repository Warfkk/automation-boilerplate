import json
import os
import sys


class Settings:
    """A class to store all settings, user-data in JSON format."""

    def __init__(self):
        self.version = 2.31

        """Settings"""
        self.HEADER_ROW = 3  # Excel header
        self.UNIT_HEADER_ROW = 4  # Excel header in unit sheet
        self.ROW = 6  # Excel start row of data
        self.UNIT_ROW = 5  # Excel start row of data in unit sheet

        self.INDEX_REPLACE = "@INDEX"  # string to be replaced in config file

        self.COL_ID_NAME = "ID"
        self.ID_REPLACE = "@ID"  # string to be replaced in config file

        self.COL_IOID_NAME = "IO ID"
        self.IOID_REPLACE = "@IOID"  # string to be replaced in config file

        self.COL_IDPV_NAME = "ID PV"
        self.IDPV_REPLACE = "@IDPV"  # string to be replaced in config file

        self.COL_IDCV_NAME = "ID CV"
        self.IDCV_REPLACE = "@IDCV"  # string to be replaced in config file

        self.COL_TYPE_NAME = "Type"
        self.TYPE_REPLACE = "@TYPE"  # string to be replaced in config file

        self.COL_COMMENT_NAME = "Description"
        self.COMMENT_REPLACE = "@CMT"  # string to be replaced in config file

        self.COL_CONFIG_NAME = "Config ID"
        self.CONFIG_REPLACE = "@CFG"  # string to be replaced in config file

        self.COL_ENG_UNIT_NAME = "Eng. Unit"
        self.ENG_UNIT_REPLACE = "@ENGUNIT"  # string to be replaced

        self.COL_ENG_MIN_NAME = "Eng. Min"
        self.ENG_MIN_REPLACE = "@ENGMIN"  # string to be replaced

        self.COL_ENG_MAX_NAME = "Eng. Max"
        self.ENG_MAX_REPLACE = "@ENGMAX"  # string to be replaced

        self.COL_ALARM_GROUP_NAME = "Alarm Group"
        self.ALARM_GROUP_REPLACE = "@AlarmGroup"  # string to be replaced

        self.COL_ALARM_PRIO_NAME = "Alarm Prio ID"
        self.ALARM_PRIO_REPLACE = "@AlarmPrio"  # string to be replaced

        self.COL_ALARM_TEXT_NAME = "Alarm Text"
        self.ALARM_TEXT_REPLACE = "@AlarmText"  # string to be replaced

        self.COL_PLC_NAME = "PLC"  # Used in Intouch
        self.PLC_REPLACE = "@PLC"  # string to be replaced in config file

        self.COL_VolumePerPulse_Name = "Volume Per Pulse"  # Used in Intouch
        self.VolumePerPulse_REPLACE = (
            "@VolumePerPulse"  # string to be replaced in config file
        )

        self.COL_ASI_ADDR_NAME = "ASI Addr"  # Used in TIA
        self.ASI_ADDR_REPLACE = "@NODEADDR"  # string to be replaced in config file

        self.COL_ASI_MASTER_NAME = "ASI Master"  # Used in TIA
        self.ASI_MASTER_REPLACE = "@ASIMASTER"  # string to be replaced in config file

        self.COL_DB_START_ADDR_NAME = "DB_start_address"

        self.OFFSET_IDENTIFIER = "@OFFSET"
        self.OFFSET_END_IDENTIFIER = "@END_OFFSET"
        self.DB_NR_REPLACE = "@DB_NR"

        self.DI_START_INDEX = 0  # Start-position index in datablock
        self.DI_SHEETNAME = "DI"

        self.DO_START_INDEX = 0
        self.DO_SHEETNAME = "DO"

        self.VALVE_START_INDEX = 0
        self.VALVE_SHEETNAME = "Valve"

        self.MOTOR_START_INDEX = 0
        self.MOTOR_SHEETNAME = "Motor"

        self.AI_START_INDEX = 0
        self.AI_SHEETNAME = "AI"

        self.AO_START_INDEX = 0
        self.AO_SHEETNAME = "AO"

        self.PID_START_INDEX = 0
        self.PID_SHEETNAME = "PID"

        self.SUM_START_INDEX = 0
        self.SUM_SHEETNAME = "Sum"

        self.ALARM_START_INDEX = 0
        self.ALARM_SHEETNAME = "Alarm"

        self.ASI_START_INDEX = 0
        self.ASI_SHEETNAME = "Valve"

        self.UNIT_START_INDEX = 0
        self.UNIT_SHEETNAME = "Units_Phases"

        self.TIA_DIR = "TIA"
        self.INTOUCH_DIR = "InTouch"
        self.SQL_DIR = "SQL"
        self.SYSTEMPLATFORM_DIR = "SYSTEMPLATFORM"

        # UI
        self.SHOW_CONFIG_ROW = False

        # internal var, used below in functions
        self.json_file = "user_settings.json"
        self.indent = 1

        # If terminal argument supplied, set debug level
        if len(sys.argv) > 1:
            self.debug_level = int(sys.argv[1])
        else:
            self.debug_level = 0

        self.user_settings = self.load_user_settings()

    def _create_user_settings(self):
        """Create dict which contains all user data"""
        user_settings = {
            "excel_path": "No excel specified",
            "output_path": "output",
            "config_path": "config",
            "DI_ENABLE": "false",
            "DO_ENABLE": "false",
            "VALVE_ENABLE": "false",
            "MOTOR_ENABLE": "false",
            "AI_ENABLE": "false",
            "AO_ENABLE": "false",
            "PID_ENABLE": "false",
            "SUM_ENABLE": "false",
            "ALARM_ENABLE": "false",
            "ASI_ENABLE": "false",
            "UNITS_ENABLE": "false",
            "Au2_ENABLE": "false",
            "seperateFolders": "false",
        }

        return user_settings

    def load_user_settings(self):
        """Load stored user settings, otherwise create .json file"""

        # Check if settings file already exists, else create it.
        if os.path.isfile(self.json_file):
            with open(self.json_file, "r") as f:
                user_settings = json.load(f)
        else:
            user_settings = self._create_user_settings()

            with open(self.json_file, "w") as f:
                json.dump(user_settings, f, indent=self.indent)

        return user_settings

    def store_user_settings(self, user_settings):
        """Dump Dict to JSON file"""
        with open(self.json_file, "w") as f:
            json.dump(user_settings, f, indent=self.indent)
