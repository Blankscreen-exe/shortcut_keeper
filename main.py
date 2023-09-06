import PySimpleGUI as sg
import os
import json

class shortcut_keeper():
    """
    This class represents an app that allows users to register and view quick launch shortcuts.
    
    Attributes:
    -----------
    app_theme: str
        The default theme of the app.
    window_size: tuple
        The default size of the app window.
    section_title_font: tuple
        The default font of section titles.
    section_normal_font: tuple
        The default font of normal text.
    app_icon: str
        The file path to the app icon.
    app_id: str
        The unique ID of the app (also the title of the app).
    window: PySimpleGUI.Window
        The main window of the app.
    """

    def __init__(self):
        self.setting_file = "sk_cfg.json"
        self._settings = self.get_settings(self.setting_file)
            
        self.app_id = self._settings["app_settings"]["app_id"]
        self.app_theme = self._settings["app_settings"]["app_theme"]
        sg.theme(self.app_theme)
        self.app_icon = "./edit.ico"
        self.window_size = (320, 220)
        self.section_title_font = ("MS sans serif", 17, "bold")
        self.section_normal_font = ("MS sans serif", 11)
        self.window = sg.Window(
                                self.get_app_title(),
                                self.tab_group(), 
                                icon=self.app_icon
                                )

    # ================================================
    #                      LAYOUTS
    # ================================================

    def get_registered_items_layout(self) -> list:
        """generates layout for List view of the registered items

        Returns:
            layout (list): pysimplegui layout list
        """
        registered_items = self.get_registered_items()
        list_of_registered_items = []
        for i, path in enumerate(registered_items):
            list_of_registered_items.append([
                sg.Button("❎", key=f"{i}_delete_button"),
                sg.Button("↗️", key=f"{i}_open_button"),
                sg.Text(os.path.basename(path),
                        key=f"{i}_path_button", tooltip=path)
            ])

        empty_message = [
            [sg.Text("WOW Such Empty!", font=self.section_title_font, text_color="lightgray")]
        ]

        final_list = [
            sg.Column(
                empty_message if len(list_of_registered_items) == 0 else list_of_registered_items,
                scrollable=True,
                vertical_scroll_only=True,
                size=self.get_window_size()
            )
        ]

        layout = [
            [sg.HorizontalSeparator()],
            final_list
        ]
        return layout

    def get_add_item_layout(self) -> list:
        """shorcut registration form

        Returns:
            layout (list): pysimplegui layout list
        """
        settings = self.get_settings(self.setting_file)
        key_list = list(settings["fileList"])
        print(key_list)
        layout = [
            [sg.Text("📋 Register  an  Item", font=self.section_title_font)],
            [sg.HorizontalSeparator()],
            [sg.Text("File/Folder Path: ", font=self.section_normal_font)],
            [
                sg.InputText(key="path_input", size=(30, 200)),
                sg.FileBrowse(file_types=(("All files", "*.*"),))
            ],
            [
                sg.Button("Submit", key="submit_button")
            ]
        ]
        return layout

    def get_about_section_layout(self) -> list:
        """about section

        Returns:
            layout (list): pysimplegui layout list
        """
        layout = [
            [
                sg.Text("📜 About Shortcut Keeper", font=self.section_title_font),
                sg.Text("(v0.1)", font=self.section_normal_font)
            ],
            [sg.HorizontalSeparator()],
            [sg.Text("This app was created by M.Hammad Hassan",
                     font=self.section_normal_font)],
            [sg.Text("using PySimpleGUI. This app aims to solve",
                     font=self.section_normal_font)],
            [sg.Text("the problem of your desktop being cluttered",
                     font=self.section_normal_font)],
            [sg.Text("with several icons. You can now keep all your",
                     font=self.section_normal_font)],
            [sg.Text("quick launch shortcuts here without messing up",
                     font=self.section_normal_font)],
            [sg.Text("This is intended mainly for windows users",
                     font=self.section_normal_font)],
            [sg.Text("For more information, please visit:",
                     font=self.section_normal_font)],
            [sg.Text("🔗 https://github.com/Blankscreen-exe", enable_events=True, font=("Consolas", 12),
                     text_color='#0F3FD8', background_color='#B2C00D', key="-ABOUT-LINK-")]
        ]
        return layout

    def get_settings_layout(self) -> list:
        """settings section

        Returns:
            layout (list): pysimplegui layout list
        """
        inp_size = (20, 200)

        layout = [
            [sg.Text("🔄 Settings", font=self.section_title_font)],
            [sg.HorizontalSeparator()],
            [
                sg.Text(
                    "App ID: ",
                    font=self.section_normal_font,
                    tooltip="This is also your window title"
                ),
                sg.InputText(
                    default_text=self.get_app_title(),
                    key="new_window_title",
                    size=(inp_size[0]+2, inp_size[1])
                ),
                sg.Button(
                    button_text="  Set  ",
                    key="set_app_title"
                ),
            ],
            [
                sg.Text("Theme: ", font=self.section_normal_font),
                sg.DropDown(
                    default_value=self.get_app_theme(),
                    values=self.get_app_theme_list(),
                    key="theme_dropdown",
                    size=inp_size,
                    
                ),
                sg.Button(
                    button_text="  Set  ",
                    key="set_theme"
                )
            ]
        ]
        return layout

    def tab_group(self) -> list:
        """config for displaying tabs

        Returns:
            tab_group (list): pysimplegui layout lists
        """
        tab_group = [[
            sg.TabGroup([
                [sg.Tab('List', self.get_registered_items_layout())],
                [sg.Tab('Register Shortcuts', self.get_add_item_layout())],
                [sg.Tab("Settings", self.get_settings_layout())],
                [sg.Tab('About', self.get_about_section_layout())]
            ])
        ]]
        return tab_group

    # ================================================
    #                  SETTINGS CRUD
    # ================================================
    
    def get_settings(self, setting_file) -> dict:
        """reads data from json file

        Returns:
            data (dict): all settings and config
        """
        if os.path.isfile(setting_file):
            with open(os.path.abspath(setting_file), "r") as file:
                data = json.load(file)
        else:
            data = self.get_settings_file_template()
            with open(os.path.abspath(setting_file), "w") as file:
                json.dump(data, file)
        return data
    
    def modify_settings(self, key, data) -> None:
        """write the config file with given data

        Args:
            key (str): key to cfg json file. can be written as "key1.key2.key3"
            data (any): data to store at the specified key
        """
        keys = key.split('.')
        settings = self.get_settings(self.setting_file)
        d = settings
        for k in keys[:-1]:
            d = d[k]
        d[keys[-1]] = data
        with open(os.path.abspath(self.setting_file), "w") as file:
            json.dump(settings, file)
    
    def get_settings_file_template(self) -> dict:
        """default template for the cfg json file

        Returns:
            dict: default settings template
        """
        try:
            return {
                    "app_settings":{
                        "app_id": self.app_id,
                        "app_theme": self.app_theme
                    },
                    "fileList": []
                } 
        except:
            return {
                    "app_settings":{
                        "app_id": "Shortcut Keeper",
                        "app_theme": "Reddit"
                    },
                    "fileList": []
                }
    
    def get_window_size(self) -> tuple:
        """getter method for window_size

        Returns:
            tuple: (length, width,)
        """
        return self.window_size
    
    # ================================================
    #                 SHORTCUTS CRUD
    # ================================================
    
    def get_registered_items(self) -> list:
        """getter method for list of registered items (filess)

        Returns:
            registered_items (list): list of paths
        """
        data = self.get_settings(self.setting_file)
        return data["fileList"]
    
    def add_item(self, path) -> None:
        """adds/writes path to a file to the config file

        Args:
            path (str): path to file
        """
        registered_items = self.get_registered_items()
        print(registered_items)
        registered_items.append(path)
            
        self.modify_settings("fileList", registered_items)

    def delete_item(self, index) -> None:
        """deletes/removes path to a file from the config file

        Args:
            index (int): index of the path in the file
        """
        registered_items = self.get_registered_items()
        del registered_items[index]
        self.modify_settings("fileList", registered_items)

    # ================================================
    #                APP THEME & TITLE
    # ================================================

    def get_app_theme(self) -> str:
        """getter method for app_theme

        Returns:
            str: app's theme
        """
        return self.app_theme

    def get_app_theme_list(self) -> list:
        """getter method for app_theme_list

        Returns:
            list: list of themes for the app
        """
        return sg.theme_list()

    def get_app_title(self) -> str:
        """getter method for app title

        Returns:
            str: app's title
        """
        return self.app_id

    def update_app_theme(self, theme) -> None:
        """changes app theme

        Args:
            theme (str): theme for the app
        """
        self.app_theme = theme
        self.modify_settings("app_settings.app_theme", theme)

    def update_app_title(self, title) -> None:
        """sets app theme

        Args:
            theme (str): theme for the app
        """
        self.app_id = title
        self.modify_settings("app_settings.app_id", title)
        
    # ================================================
    #                APP MAIN METHOD
    # ================================================
        
    def main(self) -> None:
        """Main window loop to start this app
        """
        window = self.window

        while True:
            # read events and their values
            event, values = window.read()
            # set theme
            sg.theme(self.app_theme)

            if event in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                break

            # shortcut events
            if event == "submit_button":
                path = values["path_input"]
                self.add_item(path)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event.endswith("_delete_button"):
                index = int(event.split("_")[0])
                self.delete_item(index)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event.endswith("_open_button"):
                index = int(event.split("_")[0])
                os.startfile(self.get_registered_items()[index])

            # hyperlink events
            elif event == "-ABOUT-LINK-":
                os.startfile("https://github.com/Blankscreen-exe/shortcut_keeper")

            # settings events
            elif event == "set_theme":
                theme = values["theme_dropdown"]
                self.update_app_theme(theme)
                window.close()
                sg.theme(self.app_theme)
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event == "set_app_title":
                title = values["new_window_title"]
                self.update_app_title(title)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

        window.close()


if __name__ == '__main__':
    App = shortcut_keeper()
    App.main()
