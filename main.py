import PySimpleGUI as sg
import os
import json
import uuid

from pprint import pprint as pp
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

    # =================== CONSTANTS ======================

    THEMES = [
        'LightGreen1',
        'Reddit',
        'DarkBlack',
        'GreenMono',
        'DefaultNoMoreNagging',
        'GrayGrayGray'
    ]
    
    def __init__(self):
        self.setting_file = "sk_cfg.json"
        self._settings = self.get_settings(self.setting_file)
            
        self.app_id = self._settings["app_settings"]["app_id"]
        self.app_theme = self._settings["app_settings"]["app_theme"]
        sg.theme(self.app_theme)
        self.app_icon = "./edit.ico"
        self.window_size = (300, 220)
        self.section_title_font = ("MS Sans Serif", 17, 'bold')
        self.section_normal_font = ("MS Sans Serif", 10)
        self.section_mini_font = ("MS Sans Serif", 8)
        self.font_colors = {
            "primary": "black",
            "secondary": "blue",
            "tertiary": "gray"
        }
        self.window = sg.Window(
                                self.get_app_title(),
                                self.tab_group(), 
                                icon=self.app_icon
                                )

    # =================== LAYOUTS ======================

    def get_single_list_item(self, key, file_obj):
        output = [
                sg.Button("❌", key=f"{key}__delete_button"),
                sg.Button("↗️", key=f"{key}__open_button"),
                sg.Text(os.path.basename(file_obj['path']),
                        key=f"{key}_path_button", tooltip=file_obj['path'])
            ]
        return output
    
    def items_list_generator(self) -> list:
        registered_items = self.get_registered_item_list()
        list_of_registered_items = []
        for i, key in enumerate(registered_items.keys()):
            list_of_registered_items.append(self.get_single_list_item(key, registered_items[key]))
            
        return list_of_registered_items
    
    def get_registered_items_layout(self) -> list:
        """generates layout for List view of the registered items

        Returns:
            layout (list): pysimplegui layout list
        """
        list_of_registered_items = self.items_list_generator()

        empty_message = [
            [sg.Text("WOW Such Empty!", font=self.section_title_font)]
        ]

        list_to_output = [
            sg.Column(
                empty_message if len(list_of_registered_items) == 0 else list_of_registered_items,
                scrollable=True,
                vertical_scroll_only=True,
                size=self.get_window_size(),
                key="-ITEM_LIST-"
            )
        ]

        final_layout = [
            list_to_output
        ]
        return final_layout

    def get_add_item_layout(self) -> list:
        """shorcut registration form

        Returns:
            layout (list): pysimplegui layout list
        """
        layout = [
            [sg.Text("📒 Register  an  Item", font=self.section_title_font)],
            [sg.HorizontalSeparator()],
            [sg.Text("File/Folder Path: ")],
            [
                sg.InputText(key="path_input", size=(30, 200)),
                sg.FileBrowse(file_types=(("All files", "*.*"),))
            ],
            [
                sg.Button("Submit", key="submit_button"),
                sg.Text("", font=self.section_mini_font, text_color=self.font_colors['tertiary'], key="-SUBMIT_SUCCESS-")
            ]
        ]
        return layout

    def get_about_layout(self) -> list:
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
            [sg.Text("with several icons.",
                     font=self.section_normal_font)],
            [sg.Text("This is intended mainly for Windows users",
                     font=self.section_normal_font)],
            [sg.Text("For more information, please visit:",
                     font=self.section_normal_font)],
            [sg.Text("🔗 https://github.com/Blankscreen-exe", enable_events=True, font=self.section_normal_font,
                     text_color='#0F3FD8', background_color='lightyellow', key="-ABOUT-LINK-")]
        ]
        return layout

    def get_settings_layout(self) -> list:
        """settings section

        Returns:
            layout (list): pysimplegui layout list
        """
        inp_size = (20, 10)

        layout = [
            [sg.Text("⚙️ Settings", font=self.section_title_font)],
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
                    size=inp_size
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
                [sg.Tab('List', self.get_registered_items_layout(), key="-TAB-LIST-")],
                [sg.Tab('Register Shortcuts', self.get_add_item_layout(), key="-TAB-REGISTER-")],
                [sg.Tab("Settings", self.get_settings_layout(), key="-TAB-SETTINGS-")],
                [sg.Tab('About', self.get_about_layout(), key="-TAB-ABOUT-")]
            ],
            enable_events=True, 
            key="-TABGROUP-")
        ]]
        return tab_group

    # =================== SETTINGS CRUD ======================

    def get_app_window(self):
        return sg.Window(
            self.get_app_title(),
            self.tab_group(), 
            icon=self.app_icon,
            finalize=True
            )
        
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
                        "fileList": {}
                } 
        except:
            return {
                        "app_settings":{
                            "app_id": "Shortcut Keeper",
                            "app_theme": "Reddit"
                        },
                        "fileList": {}
                }
    
    def get_window_size(self) -> tuple:
        """getter method for window_size

        Returns:
            tuple: (length, width,)
        """
        return self.window_size

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
        return self.THEMES
    
    def get_app_title(self) -> str:
        """getter method for app title

        Returns:
            str: app's title
        """
        return self.app_id

    def reset_app_theme(self, theme) -> None:
        """sets app theme

        Args:
            theme (str): theme for the app
        """
        self.app_theme = theme
        self.modify_settings("app_settings.app_theme", theme)

    def reset_app_title(self, title) -> None:
        """sets app theme

        Args:
            theme (str): theme for the app
        """
        self.app_id = title
        self.modify_settings("app_settings.app_id", title)
    
    # =================== SHORTCUTS CRUD ======================
    
    def add_registered_item(self, key, file_obj) -> None:
        """adds/writes path to a file to the config file

        Args:
            path (str): path to file
        """
        registered_items = self.get_registered_item_list()
        registered_items[key] = file_obj
            
        self.modify_settings("fileList", registered_items)

    def delete_registered_item(self, key) -> None:
        """deletes/removes path to a file from the config file

        Args:
            index (int): index of the path in the file
        """
        registered_items = self.get_registered_item_list()
        del registered_items[key]
        self.modify_settings("fileList", registered_items)

    def get_registered_item_list(self) -> list:
        """getter method for list of registered items (filess)

        Returns:
            registered_items (list): list of paths
        """
        data = self.get_settings(self.setting_file)
        return data["fileList"]
    
    # =================== ACTIONS ======================
    
    def action_switch_tab(self, window, event, values):
        # set submit success message to null
        window["-SUBMIT_SUCCESS-"].update("")
        
    def action_register_item(self, window, event, values):
        path = values["path_input"]
        id = str(uuid.uuid1())
        file_obj = {
            'key': id,
            'path': path 
        }
        self.add_registered_item(id, file_obj)
        window["-SUBMIT_SUCCESS-"].update(f"✔️{os.path.basename(file_obj['path']).strip()} Added successfully!")
        # set path input text to null
        window["path_input"].update("")

        window.extend_layout(window['-ITEM_LIST-'], [self.get_single_list_item(key=id, file_obj=file_obj)])
        window.refresh()
        window['-ITEM_LIST-'].contents_changed()
        
    def action_delete_item(self, window, event, values):
        self.get_app_window().read()
        
        key = event.split("__")[0]
        print(key)
        file_obj = self.get_settings(self.setting_file)['fileList'][key]
        pp(file_obj)
        print("HERE" ,1)
        self.delete_registered_item(key)
        print("HERE" ,2)
        # BOOKMARK:
        # self.get_app_window().finalize()
        # self.window['-ITEM_LIST-'].update([])
        # self.window[key+"__path_button"].Widget.tkpack_forget()
        # self.window[key+"__path_button"].destroy()
        # self.get_app_window().read()
        window["-ITEM_LIST-"].update("")
        # window.finalize()
        print("HERE" ,3)
        
        # window.extend_layout(window['-ITEM_LIST-'], self.items_list_generator())
        print("HERE" ,4)
        
        # window.close()
        # window = self.get_app_window()
    
    def action_open_item(self, window, event, values):
        key = event.split("__")[0]
        os.startfile(self.get_registered_item_list()[key]["path"])   
    
    def action_goto_repo_link(self, window, event, values):
        os.startfile("https://github.com/Blankscreen-exe/shortcut_keeper")
        
    
    # =================== MAIN ======================

    def main(self) -> None:
        """Main window loop to start this app
        """
        window = self.get_app_window()

        while True:
            
            # read events and their values
            event, values = window.read()

            # MSG: enable for debugging
            # pp(values)
            
            # EVENT: close app
            if event in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                break
            
            # EVENT: switch Tab
            if values["-TABGROUP-"].startswith("-TAB-"):
                self.action_switch_tab(window, event, values)
            
            # EVENT: add item
            if event == "submit_button":
                self.action_register_item(window, event, values)

            # EVENT: delete item
            elif event.endswith("__delete_button"):
                self.action_delete_item(window, event, values)

            # EVENT: open item
            elif event.endswith("__open_button"):
                self.action_open_item(window, event, values)

            # EVENT: Goto repo link
            elif event == "-ABOUT-LINK-":
                self.action_goto_repo_link(window, event, values)

            # EVENT: set the theme of the app
            elif event == "set_theme":
                # FIXME: remove the function call. its muda muda
                # self.action_set_app_theme(window, event, values)
                self.reset_app_theme(values["theme_dropdown"])
                window.close()
                sg.theme(self.app_theme)
                window = self.get_app_window()
                
            # EVENT: set the title of the app
            elif event == "set_app_title":
                # self.action_set_app_title(window, event, values)
                title = values["new_window_title"]
                self.reset_app_title(title)
                window.close()
                window = self.get_app_window()
                
        window.close()


if __name__ == '__main__':
    App = shortcut_keeper()
    App.main()