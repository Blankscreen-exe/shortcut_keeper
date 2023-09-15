"""
Module Name: shortcut_keeper
Version: 0.1

This script contains code for a desktoip applet which helps in keeping symbolic links in one place. This applet is built with PySimpleGui which is a Python based desktop application framework built on Tkinter.

Author: Muhammad Hammad Hassan
Date: April 2023

Classes:
    shortcut_keeper: Initializes the PySimpleGui Applet with all of its other functionalities.

Usage Example:
    # Example code demonstrating how to use this module/package.

    App = shortcut_keeper()
    App.main()

Notes:
    This is a compact software which only consists of a single class. It is currently v0.1. In case this software is developed further, I might add some more dependent files.
"""

import PySimpleGUI as sg
import os
import json
import uuid

from pprint import pprint as pp
class shortcut_keeper():
    """
    This class represents an app that allows users to register and view quick launch shortcuts.
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

    def get_single_list_item(self, key, file_obj) -> list:
        """generates layout for a single List item

        Returns:
            single_list_item (list): pysimplegui layout list
        """
        single_list_item = [
                sg.Button("❌", key=f"{key}__delete_button"),
                sg.Button("↗️", key=f"{key}__open_button"),
                sg.Text(os.path.basename(file_obj['path']),
                        key=f"{key}_path_button", tooltip=file_obj['path'])
            ]
        return single_list_item
    
    def items_list_generator(self) -> list:
        """generates layout for List of all registered items

        Returns:
            list_of_registered_items (list): pysimplegui layout list
        """
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
            [sg.Text("",
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
                    "Personalization: ",
                    font=self.section_normal_font,
                    tooltip="Personalization settings"
                )
            ],
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
        """Getter method for the window object which is used throughout the application
        
        Returns:
            sg.Window (obj): pysimplegui window object
        """
        return sg.Window(
            self.get_app_title(),
            self.tab_group(), 
            icon=self.app_icon,
            finalize=True
            )
        
    def get_settings(self, setting_file) -> dict:
        """reads data from json file

        Args:
            setting_file (dict): all the configurations
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
            title (str): title for the app
        """
        self.app_id = title
        self.modify_settings("app_settings.app_id", title)
    
    # =================== SHORTCUTS CRUD ======================
    
    def add_registered_item(self, key, file_obj) -> None:
        """adds/writes path to a file to the config file

        Args:
            key (str): uuid based key for the specific file
            file_obj (dict): dictionary containing file information about one file
        """
        registered_items = self.get_registered_item_list()
        registered_items[key] = file_obj
            
        self.modify_settings("fileList", registered_items)

    def delete_registered_item(self, key) -> None:
        """deletes/removes path to a file from the config file

        Args:
            key (str): uuid based key for the specific file
        """
        registered_items = self.get_registered_item_list()
        del registered_items[key]
        self.modify_settings("fileList", registered_items)

    def get_registered_item_list(self) -> dict:
        """getter method for list of registered items (filess)

        Returns:
            registered_items (dict): dictionary of all file info
        """
        registered_items = self.get_settings(self.setting_file)["fileList"]
        return registered_items
    
    # =================== ACTIONS ======================
    
    def action_switch_tab(self, window, event, values) -> None:
        """Triggers when you switch between tabs.
        Do all the actions which needs to be done after tab switching

        Args:
            window (obj): pysimplegui window object
            event (str): string value for the event
            values (dict): dictionary containing all the data that is passed with each event
        """
        
        # set submit success message to null
        window["-SUBMIT_SUCCESS-"].update("")
        
    def action_register_item(self, window, event, values) -> None:
        """Triggers when you register an item.
        stores the files information in the settings file
        and reflects the new changes immediately.
        
        Args:
            window (obj): pysimplegui window object
            event (str): string value for the event
            values (dict): dictionary containing all the data that is passed with each event
        """
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
    
    def action_open_item(self, window, event, values) -> None:
        """Triggers when you hit the open file button.
        executes the selected file immediately using the path stored.
        
        Args:
            window (obj): pysimplegui window object
            event (str): string value for the event
            values (dict): dictionary containing all the data that is passed with each event
        """
        key = event.split("__")[0]
        os.startfile(self.get_registered_item_list()[key]["path"])   
    
    def action_goto_repo_link(self, window, event, values) -> None:
        """Triggers when you click the open the GitHub Repository link.
        Takes you to the repository for the source code.
        
        Args:
            window (obj): pysimplegui window object
            event (str): string value for the event
            values (dict): dictionary containing all the data that is passed with each event
        """
        os.startfile("https://github.com/Blankscreen-exe/shortcut_keeper")
        
    
    # =================== MAIN ======================

    def main(self) -> None:
        """Main window loop to start this app
        """
        window = self.get_app_window()

        while True:
            
            # NOTE: those events which are not performed using any methods are the ones which uses `window.close()`. 
            # If they are used withing a separate method of their own, then unexpected behaviour will be observed.
            
            # read events and their values
            event, values = window.read()
            
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
                key = event.split("__")[0]
                file_obj = self.get_settings(self.setting_file)['fileList'][key]
                self.delete_registered_item(key)
                
                window.close()
                window = self.get_app_window()

            # EVENT: open item
            elif event.endswith("__open_button"):
                self.action_open_item(window, event, values)

            # EVENT: Goto repo link
            elif event == "-ABOUT-LINK-":
                self.action_goto_repo_link(window, event, values)

            # EVENT: set the theme of the app
            elif event == "set_theme":
                self.reset_app_theme(values["theme_dropdown"])
                window.close()
                sg.theme(self.app_theme)
                window = self.get_app_window()
                
            # EVENT: set the title of the app
            elif event == "set_app_title":
                title = values["new_window_title"]
                self.reset_app_title(title)
                window.close()
                window = self.get_app_window()
                
        window.close()


if __name__ == '__main__':
    App = shortcut_keeper()
    App.main()