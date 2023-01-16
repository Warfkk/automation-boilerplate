import os
import os.path
from gen_obj_func import GenObjFunc as genfunc


class Au2ParInstance:
    """Object specific code to concatenate text lines and create files"""

    def __init__(self, gen_main, output_path, obj_list, config_path,
                 config_type='mc'):
        self.s = gen_main.s  # Instanciate settings

        self.type = 'Au2ParInstance'
        self.masterfolder = 'Au2'
        self.config_type = config_type
        self.user_settings = self.s.user_settings

        self.cp = os.path.join(config_path, self.masterfolder, self.type)  # Config folder path
        self.cf = os.path.join(self.cp, self.type + '.txt')  # base config file

        self.output_path = output_path
        self.parameters_path = os.path.join(self.output_path, self.masterfolder, 'Au2ParInstance')

        self.ol = obj_list

        self.gen = genfunc(gen_main)

        self.rl = []  # Create empty list "result list"

        # Check if list is empty, if it is print an error
        if self.ol:
            self.generate()
        else:
            print(f'\nWARNING: {self.type.upper()} not generated, no items found in TD')

    def Parameters(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'Parameters')

        filename = self.type + 'Parameters.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def ParametersInput(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'ParametersInput')

        filename = self.type + 'ParametersInput.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def Tags(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'Tags')

        filename = self.type + 'Tags.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def Type(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'Type')

        filename = self.type + 'Type.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def InitValue(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'InitValue')

        filename = self.type + 'InitValue.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def PLCAddr(self):
        data = self.gen.multiple(self.ol, self.cf, self.rl, 'PLCAddr')

        filename = self.type + 'PLCAddr.txt'
        path = os.path.join(self.parameters_path, filename)
        if not os.path.exists(self.parameters_path):
            os.makedirs(self.parameters_path)
        with open(path, 'w', encoding='cp1252') as f:
            f.write(data)

    def generate(self):
        if self.ol:
            if self.user_settings['Au2_ENABLE']:
                self.Parameters()
                self.ParametersInput()
                self.Tags()
                self.Type()
                self.InitValue()
                self.PLCAddr()
            self.gen.result(self.rl, type=self.type.upper())
