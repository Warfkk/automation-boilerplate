import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class General:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path, type=''):
        self.s = gen_main.s  # Instance settings

        self.type = type
        self.masterfolder = 'CMs'
        self.user_settings = self.s.user_settings

        self.seperateFolders = self.user_settings['seperateFolders']

        # Config folder path
        self.cp = os.path.join(config_path, self.masterfolder)
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.tia_path = os.path.join(
            self.output_path, self.masterfolder, self.s.TIA_DIR)
        self.it_path = os.path.join(
            self.output_path, self.masterfolder, self.s.INTOUCH_DIR)
        self.systemplatform_path = os.path.join(
            self.output_path, self.masterfolder, self.s.SYSTEMPLATFORM_DIR)
        self.sql_path = os.path.join(
            self.output_path, self.masterfolder, self.s.SQL_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(
                f'\nWARNING: {self.type.upper()} not generated, no items found in TD')

    def _find_plcs(self):
        """find what plcs are in the object list"""
        self.plc_set = set()  # Create a set,  doesnt allow duplicate values
        for obj in self.ol:
            self.plc_set.add(obj['plc'])

    def _systemPlatform(self):
        if self.seperateFolders:
            for plc in self.plc_set:
                data = self.gen.multiple(
                    self.ol, self.cf, self.rl, 'MC_System_Platform', plc_name=plc)
                filename = plc + '_' + self.type + '_SPO.csv'
                pathwithplc = path = os.path.join(
                    self.systemplatform_path, plc)
                path = os.path.join(pathwithplc, filename)
                if not os.path.exists(pathwithplc):
                    os.makedirs(pathwithplc)
                with open(path, 'w', encoding='cp1252') as f:
                    f.write(data)
        else:
            data = self.gen.multiple(
                self.ol, self.cf, self.rl, 'MC_System_Platform')
            filename = self.type + '_SPO.csv'
            path = os.path.join(self.systemplatform_path, filename)
            if not os.path.exists(self.systemplatform_path):
                os.makedirs(self.systemplatform_path)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _sql(self):
        if self.seperateFolders:
            for plc in self.plc_set:
                data = self.gen.multiple(
                    self.ol, self.cf, self.rl, 'SQLProcedure', plc_name=plc)
                filename = plc + '_' + self.type + '_sql.sql'
                pathwithplc = path = os.path.join(self.sql_path, plc)
                path = os.path.join(pathwithplc, filename)
                if not os.path.exists(pathwithplc):
                    os.makedirs(pathwithplc)
                with open(path, 'w', encoding='cp1252') as f:
                    f.write(data)
        else:
            data = self.gen.multiple(self.ol, self.cf, self.rl, 'SQLProcedure')

            filename = self.type + '_sql.sql'
            path = os.path.join(self.sql_path, filename)
            if not os.path.exists(self.sql_path):
                os.makedirs(self.sql_path)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _intouchTags(self):
        if self.seperateFolders:
            for plc in self.plc_set:
                data = self.gen.single(self.cf, self.rl, "Intouch_Header")
                data += self.gen.multiple(self.ol,
                                          self.cf, self.rl, "Intouch_Tag")
                filename = plc + '_' + self.type + '_sql.sql'
                pathwithplc = path = os.path.join(self.it_path, plc)
                path = os.path.join(pathwithplc, filename)
                if not os.path.exists(pathwithplc):
                    os.makedirs(pathwithplc)
                with open(path, 'w', encoding='cp1252') as f:
                    f.write(data)
        else:
            data = self.gen.single(self.cf, self.rl, "Intouch_Header")
            data += self.gen.multiple(self.ol, self.cf, self.rl, "Intouch_Tag")

            filename = self.type + '_IT.csv'
            path = os.path.join(self.it_path, filename)
            if not os.path.exists(self.it_path):
                os.makedirs(self.it_path)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def generate(self):
        if self.ol:
            self._find_plcs()
            self._sql()
            self._systemPlatform()
            self._sql()
            self._intouchTags()
            self.gen.result(self.rl, type=self.type.upper())
