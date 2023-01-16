import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class PID:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path,
                 config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'pid'
        self.masterfolder = 'CMs'
        self.config_type = config_type
        self.user_settings = self.s.user_settings

        self.cp = os.path.join(config_path, self.masterfolder, self.type)  # Config folder path
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.tia_path = os.path.join(self.output_path, self.masterfolder, self.s.TIA_DIR)
        self.it_path = os.path.join(self.output_path, self.masterfolder, self.s.INTOUCH_DIR)
        self.sql_path = os.path.join(self.output_path, self.masterfolder, self.s.SQL_DIR)

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(f'\nWARNING: {self.type.upper()} not generated, no items found in TD')

    def _tia_db(self):
        data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var')
        data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

        filename = self.type + '_db.db'
        path = os.path.join(self.tia_path, filename)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _find_plcs(self):
        """find what plcs are in the object list"""
        self.plc_set = set()  # Create a set,  doesnt allow duplicate values
        for obj in self.ol:
            self.plc_set.add(obj['plc'])

    def _tia_db_multiple_plc(self):
        for plc in self.plc_set:
            data = self.gen.single(self.cf, self.rl, 'TIA_DB_Header')
            data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Var', plc_name=plc)
            data += self.gen.single(self.cf, self.rl, 'TIA_DB_Begin')
            #  data += self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_DB_Parameters', plc_name=plc)
            data += self.gen.single(self.cf, self.rl, 'TIA_DB_Footer')

            filename = plc + '_' + self.type + '_db.db'
            pathwithplc = os.path.join(self.tia_path, plc)
            path = os.path.join(pathwithplc, filename)
            if not os.path.exists(pathwithplc):
                os.makedirs(pathwithplc)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _tia_symbol(self):
        data = self.gen.multiple_config(self.ol, self.cp, self.rl,
                                        'TIA_Symbol')

        filename = self.type + '_symbols.sdf'
        path = os.path.join(self.tia_path, filename)
        if not os.path.exists(self.tia_path):
            os.makedirs(self.tia_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _tia_help_code(self):
        for plc in self.plc_set:
            data = self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_Help_PID_Call', plc_name=plc)
            filename = plc + '_' + self.type + '_help-pid-call-to-copy.txt'
            pathwithplc = os.path.join(self.tia_path, plc)
            path = os.path.join(pathwithplc, filename)
            if not os.path.exists(pathwithplc):
                os.makedirs(pathwithplc)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _tia_idb(self):
        for plc in self.plc_set:
            data = self.gen.multiple(self.ol, self.cf, self.rl, 'TIA_iDB', plc_name=plc)
            filename = plc + '_' + self.type + '_iDBs.db'
            pathwithplc = path = os.path.join(self.tia_path, plc)
            path = os.path.join(pathwithplc, filename)
            with open(path, 'w', encoding='cp1252') as f:
                f.write(data)

    def _intouch(self):
        data = self.gen.single(self.cf, self.rl, 'Intouch_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'Intouch_Tag')

        filename = self.type + '_IT.csv'
        path = os.path.join(self.it_path, filename)
        if not os.path.exists(self.it_path):
            os.makedirs(self.it_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _sql(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'SQLProcedure')

        filename = self.type + '_sql.csv'
        path = os.path.join(self.sql_path, filename)
        if not os.path.exists(self.sql_path):
            os.makedirs(self.sql_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _Au2Mate_DB(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'Au2Mate_DB')

        filename = self.type + '_db.awl'
        path = os.path.join(self.tia_path, filename)
        if not os.path.exists(self.tia_path):
            os.makedirs(self.tia_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _Au2Mate_Code(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'Au2Mate_Code')

        filename = self.type + '_code.awl'
        path = os.path.join(self.tia_path, filename)
        if not os.path.exists(self.tia_path):
            os.makedirs(self.tia_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def _Au2Mate_Platform(self):
        data = self.gen.single(self.cf, self.rl, 'Au2Mate_Platform_Header')
        data += self.gen.multiple(self.ol, self.cf, self.rl, 'Au2Mate_Platform_Data')

        filename = self.type + '_platform.csv'
        path = os.path.join(self.tia_path, filename)
        if not os.path.exists(self.tia_path):
            os.makedirs(self.tia_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def generate(self):
        if self.ol:
            self._find_plcs()
            #self._tia_db_multiple_plc()
            #self._tia_symbol()
            #self._tia_code()
            #self._intouch()
            #self._sql()
            if self.user_settings['Au2_ENABLE']:
                self._Au2Mate_DB()
                self._Au2Mate_Code()
                self._Au2Mate_Platform()
            self.gen.result(self.rl, type=self.type.upper())
