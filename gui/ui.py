import tkinter
import tkinter.messagebox
import tkinter.filedialog as filedialog
import customtkinter
import os
import os.path
from settings import Settings
from gen_main import GenMain

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class GenUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.s = Settings()

        # Constants
        self.height = 530
        self.width = 900

        self.resizable(False, False)

        # Get Current User Data
        self.user_settings = self.get_user_settings()

        self.create_window()
        self.create_window_contents()
        # self.create_dropdown()

        # "Run Script" button changes state from this function
        self.check_path_validity()

    def create_window(self):
        # configure window
        self.title("automation-boilerplate")
        self.geometry(f"{self.width}x{self.height}")

    def create_dropdown(self):
        """Create drop-down menu"""
        self.menu = customtkinter.Menu(self.master)
        self.master.config(menu=self.menu)

        # file submenu
        self.subMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Exit", command=self.master.quit)

        # view submenu
        self.viewSubMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.viewSubMenu)
        self.viewSubMenu.add_command(label="Config path", command=self.open_config_path)

        # about submenu
        self.aboutSubMenu = customtkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="About", menu=self.aboutSubMenu)
        self.aboutSubMenu.add_command(label="Version", command=self.create_about_window)

    def create_window_contents(self):
        """Create window contents"""

        # create filesheader
        self.filesheader = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.filesheader.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="W")

        self.filesheaderlabel = customtkinter.CTkLabel(
            self.filesheader,
            text="Välj filer och mappar",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.filesheaderlabel.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        # create files
        self.files = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.files.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="W")

        # Excel button
        self.excelButton = customtkinter.CTkButton(
            self.files, command=self.browse_excel, text="Välj  TD"
        )
        self.excelButton.grid(row=1, column=0, padx=20, pady=10, sticky="W")

        # Excel path label
        self.excelLabel = customtkinter.CTkLabel(
            self.files, text=(self.user_settings["excel_path"])
        )
        self.excelLabel.grid(row=1, column=1, padx=20, pady=10, sticky="W")

        # General settings header
        self.headergensettings = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.headergensettings.grid(
            row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="W"
        )

        self.gensettingslabel = customtkinter.CTkLabel(
            self.headergensettings,
            text="Generella inställningar",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            anchor=customtkinter.W,
        )
        self.gensettingslabel.grid(row=1, column=0, padx=10, pady=10)

        # create generall serrings
        self.gensettings = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.gensettings.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="W")

        self.row_placement = 1
        self.seperateFolders_var = customtkinter.BooleanVar()
        self.seperateFolders_var.initialize(self.user_settings["seperateFolders"])
        self.seperateFolders = customtkinter.CTkCheckBox(
            master=self.gensettings,
            variable=self.seperateFolders_var,
            text="Generera filer i olika PLC mappar",
        )
        self.seperateFolders.grid(
            row=self.row_placement, column=0, pady=(20, 10), padx=20, sticky="W"
        )

        # create header configs
        self.headerconfigs = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.headerconfigs.grid(row=5, column=0, padx=(20, 0), pady=(20, 0), sticky="W")

        self.configsheaderlabel = customtkinter.CTkLabel(
            self.headerconfigs,
            text="Välj vad som ska genereras",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            anchor=customtkinter.W,
        )
        self.configsheaderlabel.grid(row=1, column=0, padx=10, pady=10)

        # create configs
        self.configs = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.configs.grid(row=6, column=0, padx=(20, 0), pady=(0, 0), sticky="W")

        self.row_placement = 2
        self.valve_var = customtkinter.BooleanVar()
        self.valve_var.initialize(self.user_settings["VALVE_ENABLE"])
        self.valve_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.valve_var, text="Ventiler"
        )
        self.valve_enable.grid(
            row=self.row_placement, column=0, pady=(20, 10), padx=20, sticky="W"
        )

        self.motor_var = customtkinter.BooleanVar()
        self.motor_var.initialize(self.user_settings["MOTOR_ENABLE"])
        self.motor_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.motor_var, text="Motorer"
        )
        self.motor_enable.grid(
            row=self.row_placement, column=1, pady=(20, 10), padx=20, sticky="W"
        )

        self.di_var = customtkinter.BooleanVar()
        self.di_var.initialize(self.user_settings["DI_ENABLE"])
        self.di_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.di_var, text="Digitala Ingångar"
        )
        self.di_enable.grid(
            row=self.row_placement, column=2, pady=(20, 10), padx=20, sticky="W"
        )

        self.do_var = customtkinter.BooleanVar()
        self.do_var.initialize(self.user_settings["DO_ENABLE"])
        self.do_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.do_var, text="Digitala Utgånngar"
        )
        self.do_enable.grid(
            row=self.row_placement, column=3, pady=(20, 10), padx=20, sticky="W"
        )

        self.row_placement = 3
        self.ai_var = customtkinter.BooleanVar()
        self.ai_var.initialize(self.user_settings["AI_ENABLE"])
        self.ai_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.ai_var, text="Analoga Ingångar"
        )
        self.ai_enable.grid(
            row=self.row_placement, column=0, pady=(20, 10), padx=20, sticky="W"
        )

        self.ao_var = customtkinter.BooleanVar()
        self.ao_var.initialize(self.user_settings["AO_ENABLE"])
        self.ao_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.ao_var, text="Analoga Utgångar"
        )
        self.ao_enable.grid(
            row=self.row_placement, column=1, pady=(20, 10), padx=20, sticky="W"
        )

        self.pid_var = customtkinter.BooleanVar()
        self.pid_var.initialize(self.user_settings["PID_ENABLE"])
        self.pid_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.pid_var, text="Regulatorer (PID)"
        )
        self.pid_enable.grid(
            row=self.row_placement, column=2, pady=(20, 10), padx=20, sticky="W"
        )

        self.sum_var = customtkinter.BooleanVar()
        self.sum_var.initialize(self.user_settings["SUM_ENABLE"])
        self.sum_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.sum_var, text="Pulsräcknare (SUM)"
        )
        self.sum_enable.grid(
            row=self.row_placement, column=3, pady=(20, 10), padx=20, sticky="W"
        )

        self.row_placement = 4
        self.alarm_var = customtkinter.BooleanVar()
        self.alarm_var.initialize(self.user_settings["ALARM_ENABLE"])
        self.alarm_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.alarm_var, text="Alarm"
        )
        self.alarm_enable.grid(
            row=self.row_placement, column=0, pady=(20, 10), padx=20, sticky="W"
        )

        self.asi_var = customtkinter.BooleanVar()
        self.asi_var.initialize(self.user_settings["ASI_ENABLE"])
        self.asi_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.asi_var, text="ASI Master"
        )
        self.asi_enable.grid(
            row=self.row_placement, column=1, pady=(20, 10), padx=20, sticky="W"
        )

        self.units_var = customtkinter.BooleanVar()
        self.units_var.initialize(self.user_settings["UNITS_ENABLE"])
        self.units_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.units_var, text="Enheter"
        )
        self.units_enable.grid(
            row=self.row_placement, column=2, pady=(20, 10), padx=20, sticky="W"
        )

        self.Au2_var = customtkinter.BooleanVar()
        self.Au2_var.initialize(self.user_settings["Au2_ENABLE"])
        self.Au2_enable = customtkinter.CTkCheckBox(
            master=self.configs, variable=self.Au2_var, text="Au2"
        )
        self.Au2_enable.grid(
            row=self.row_placement, column=3, pady=(20, 10), padx=20, sticky="W"
        )

        # Run script
        self.runButton = customtkinter.CTkButton(
            self.configs,
            text="Generera",
            command=self.run_self,
            state=customtkinter.DISABLED,
        )
        self.runButton.grid(row=10, column=0, padx=20, pady=10)

    def browse_excel(self):
        excelPath = filedialog.askopenfilename(
            filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*"))
        )

        # Write to user_settings dictionary, to save it for later.
        self.user_settings["excel_path"] = excelPath
        # Update label
        self.excelLabel.configure(text=excelPath)

        # Check if all path are valid
        self.check_path_validity()

    def output_path(self):
        output_path = filedialog.askdirectory()
        # Write to user_settings dictionary, to save it for later.
        self.user_settings["output_path"] = output_path
        # Update label
        self.outpathLabel.configure(text=output_path)

    def config_path(self):
        config_path = filedialog.askdirectory()
        # Write to user_settings dictionary, to save it for later.
        self.user_settings["config_path"] = config_path
        # Update label
        self.cfgpathLabel.configure(text=config_path)

    def check_path_validity(self):
        if os.path.isfile(self.user_settings["excel_path"]):
            self.runButton.configure(state=customtkinter.NORMAL)
        else:
            self.runButton.configure(state=customtkinter.DISABLED)

    def run_self(self):
        self.check_disable_buttons()
        self.s.store_user_settings(self.user_settings)
        GenMain()

    def open_config_path(self):
        c_path = self.user_settings["config_path"]
        c2_path = os.path.realpath(c_path)
        os.startfile(c2_path)

    def create_about_window(self):
        self.about = customtkinter.Toplevel()
        self.about.title("About")
        self.label = customtkinter.Label(self.about, text=self.s.version).pack()

    def get_user_settings(self):
        return self.s.user_settings

    def check_disable_buttons(self):
        self.user_settings["VALVE_ENABLE"] = self.valve_var.get()
        self.user_settings["MOTOR_ENABLE"] = self.motor_var.get()
        self.user_settings["DI_ENABLE"] = self.di_var.get()
        self.user_settings["DO_ENABLE"] = self.do_var.get()
        self.user_settings["AI_ENABLE"] = self.ai_var.get()
        self.user_settings["AO_ENABLE"] = self.ao_var.get()
        self.user_settings["PID_ENABLE"] = self.pid_var.get()
        self.user_settings["SUM_ENABLE"] = self.sum_var.get()
        self.user_settings["ALARM_ENABLE"] = self.alarm_var.get()
        self.user_settings["ASI_ENABLE"] = self.asi_var.get()
        self.user_settings["UNITS_ENABLE"] = self.units_var.get()
        self.user_settings["Au2_ENABLE"] = self.Au2_var.get()
        self.user_settings["seperateFolders"] = self.seperateFolders_var.get()
