import PySimpleGUI as sg
import os
import json
import uuid
import mimetypes
# for debug purposes
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
    
    # ================================================
    #                      CONSTANTS
    # ================================================
    
    ITEM_CATEGORY_LIST = {
            "General":"general", 
            "Dev Tools":"dev_tools", 
            "Documentations":"doc", 
            "Study Resources":"study_resources", 
            "Games":"games", 
            "Other":"other", 
        }
    
    # default filter applied
    FILTER = "All"
        
    # ================================================
    #                  EVENT CONSTANTS
    # ================================================
    
    # TODO: add event constants 
    EVENTS = {
        "register_item": "-REGISTER_ITEM-",
        "delete_item": "_delete_item",
        "open_item": "_open_item",
        "apply_filter": "-FILTER-",
        "set_app_theme": "-SET_THEME-",
        "set_app_id": "-SET_TITLE-",
        "go_to_repo": "-GOTO_REPO-",
        "go_to_blog": "-GOTO_BLOG-",
        "add_category_popup": "-ADD_CATEGORY_POPUP-",
        "delete_category_popup": "-DELETE_CATEGORY_POPUP-",
        "add_category": "-ADD_CATEGORY-",
        "delete_category": "-DELETE_CATEGORY-",
    }
    
    # ================================================
    #                    CONSTRUCTOR
    # ================================================
        
    def __init__(self):
        self.setting_file = "sk_cfg.json"
        self._settings = self.get_settings(self.setting_file)
            
        self.app_id = self._settings["app_settings"]["app_id"]
        self.app_theme = self._settings["app_settings"]["app_theme"]
        sg.theme(self.app_theme)
        self.app_icon = "./edit.ico"
        self.window_size = (320, 220)
        
        # fonts
        self.section_title_font = ("MS sans serif", 17, "bold")
        self.section_normal_font = ("MS sans serif", 11)
        self.section_hint_font = ("MS sans serif", 10, "bold")
        self.section_hint_font_color = "gray"
        
        # item categories
        self.item_categories = self.set_item_categories() #self.get_settings(self.setting_file)['itemCategories']
        
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
        count_of_list_item = 0
        
        registered_items = self.get_registered_items()
        
        list_of_registered_items = []
        
        for i, file_data in enumerate(registered_items):
            
            try:
                if self.FILTER=="All":
                    # item to be added to the list
                    item = lambda : [
                        sg.Button(
                            "❎", 
                            key=file_data['key'] + self.EVENTS['delete_item'], 
                            tooltip=f" Delete {file_data['name']} from registry "
                            ),
                        sg.Button(
                            "↗️", 
                            key=file_data['key'] + self.EVENTS['open_item'], 
                            tooltip=f" Open {file_data['name']} "
                            ),
                        sg.Text(
                            os.path.basename(f"({file_data['type']}) {file_data['name']}"),
                            font=self.section_normal_font,
                            key=f"{file_data['key']}_path_button", 
                            tooltip=f" ({file_data['category']}) {file_data['path']} "
                            )
                    ]
                    list_of_registered_items.append(item())
                
                elif file_data['category'] == self.item_categories[self.FILTER]:
                    # item to be added to the list
                    item = lambda : [
                        sg.Button(
                            "❎", 
                            key=file_data['key'] + self.EVENTS['delete_item'], 
                            tooltip=f" Delete {file_data['name']} from registry "
                            ),
                        sg.Button(
                            "↗️", 
                            key=file_data['key'] + self.EVENTS['open_item'], 
                            tooltip=f" Open {file_data['name']} "
                            ),
                        sg.Text(
                            os.path.basename(f"({file_data['type']}) {file_data['name']}"),
                            font=self.section_normal_font, 
                            tooltip=f" ({file_data['category']}) {file_data['path']} "
                            )
                    ]
                    list_of_registered_items.append(item())
                
            except:
                pass

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
            [
                sg.Text("Filter: ", font=self.section_normal_font),
                sg.DropDown(
                    default_value=self.FILTER,
                    values=["All"]+list(self.item_categories.keys()),
                    key=self.EVENTS["apply_filter"],
                    size=(35, 220),
                    enable_events=True
                ),
            ],
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
        layout = [
            [sg.Text("📋 Register  an  Item", font=self.section_title_font)],
            [sg.HorizontalSeparator()],
            [
                sg.Text("File/Folder Path:", font=self.section_normal_font),
                sg.Text("(?)", font=self.section_hint_font, text_color=self.section_hint_font_color, tooltip=" Path of the file ")
            ],
            [
                sg.InputText(key="path_input", size=(30, 200)),
                sg.FileBrowse(file_types=(("All files", "*.*"),))
            ],
            [
                sg.Text("File Name:", font=self.section_normal_font),
                sg.Text("(?)", font=self.section_hint_font, text_color=self.section_hint_font_color, tooltip=" Name to be displayed ")
            ],
            [
                sg.InputText(key="file_name_input", size=(30, 200)),
            ],
            [
                sg.Text("File Category:", font=self.section_normal_font),
                sg.Text("(?)", font=self.section_hint_font, text_color=self.section_hint_font_color, tooltip=" Choose a file category ")
            ],
            [
                sg.DropDown(
                    default_value=list(self.item_categories.keys())[0],
                    values=list(self.item_categories.keys()),
                    key="file_category_input",
                    size=(30, 200),
                )
            ],
            [
                sg.Button(
                    "Submit", 
                    key=self.EVENTS['register_item']
                    )
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
            [sg.Text("🔗 https://github.com/Blankscreen-exe", 
                     enable_events=True, 
                     font=("Consolas", 12),
                     text_color='#0F3FD8', 
                     background_color='lightyellow', 
                     key=self.EVENTS['go_to_repo'], 
                     tooltip="Go to Github Repository"
                     )]
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
                ),
                sg.Text(
                    "(?)",
                    font=self.section_hint_font,
                    text_color=self.section_hint_font_color,
                    tooltip=""" For future use, but this acts only 
 as your window title for now """
                ),
                sg.InputText(
                    default_text=self.get_app_title(),
                    key="new_window_title",
                    size=(inp_size[0]+2, inp_size[1])
                ),
                sg.Button(
                    button_text="  Set  ",
                    key=self.EVENTS['set_app_id']
                ),
            ],
            [
                sg.Text("Theme: ", font=self.section_normal_font),
                sg.Text(
                    "(?)",
                    font=self.section_hint_font,
                    text_color=self.section_hint_font_color,
                    tooltip=" Select a Theme "
                ),
                sg.DropDown(
                    default_value=self.get_app_theme(),
                    values=self.get_app_theme_list(),
                    key="theme_dropdown",
                    size=inp_size,
                    
                ),
                sg.Button(
                    button_text="  Set  ",
                    key=self.EVENTS['set_app_theme']
                )
            ],
            [
                sg.Text(
                    "Category: ", 
                    font=self.section_normal_font
                    ),
                sg.Text(
                    "(?)",
                    font=self.section_hint_font,
                    text_color=self.section_hint_font_color,
                    tooltip=" Add/Delete file categories "
                ),
                sg.Button(
                    "➕", 
                    key=self.EVENTS['add_category_popup']
                    ),
                sg.Button(
                    "➖", 
                    key=self.EVENTS['delete_category_popup']
                    ),
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
            ], key="-TAB_GROUP-")
        ]]
        return tab_group

    def get_add_category_layout(self):
        return  [
            [sg.Text('Add Your custom file category here:', font=self.section_normal_font)],
            [sg.InputText(key="category", size=(30, 200))],
            [sg.Button('Add', key=self.EVENTS['add_category'])]
        ]
        
    def get_delete_category_layout(self):
        return  [
            [sg.Text('Select a file category to delete:', font=self.section_normal_font)],
            [
                sg.DropDown(
                    default_value=list(self.item_categories.keys())[0],
                    values=list(self.item_categories.keys()),
                    key="file_category_input",
                    size=(30, 200),
                )
            ],
            [sg.Button('Delete', key=self.EVENTS['delete_category'])]
        ]

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
            app_id = self.app_id
            app_theme = self.app_theme
        except:
            app_id = "Shortcut Keeper"
            app_theme = "Reddit"
            
        return {
                "app_settings":{
                    "app_id": app_id,
                    "app_theme": app_theme
                },
                "itemCategories": self.ITEM_CATEGORY_LIST,
                "fileList": []
            }
    
    def get_window_size(self) -> tuple:
        """getter method for window_size

        Returns:
            tuple: (length, width,)
        """
        return self.window_size
    
    def set_item_categories(self):
        self.item_categories = self.get_settings(self.setting_file)['itemCategories']
        return self.item_categories
        
    def delete_item_category(self, name):
        self.item_categories = self.get_settings(self.setting_file)['itemCategories']
        
        try:
            del self.item_categories[name]
            self.modify_settings("itemCategories", self.item_categories)
        except:
            pass

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
    
    def add_item(self, file_obj) -> None:
        """adds/writes path to a file to the config file

        Args:
            file_obj (dict): file data dictionary
        """
        registered_items = self.get_registered_items()
        registered_items.append(file_obj)
            
        self.modify_settings("fileList", registered_items)

    def delete_item(self, key) -> None:
        """deletes/removes path to a file from the config file

        Args:
            index (key): index of the path in the file
        """
        registered_items = self.get_registered_items()
        for i, item_key in enumerate(registered_items):
            if key==item_key['key']:
                del registered_items[i]
                break
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
    #                 APP UTILITIES
    # ================================================
    
    def get_uuid(self):
        # make a UUID based on the host address and current time
        return str(uuid.uuid1())
    
    def get_file_extension(self, file_name):
        extension = os.path.splitext(file_name)[1]
        return  extension if len(extension)!=0 else "?"
    
    def find_item_index(self, key):
        item_list = self.get_registered_items()
        for index, item in enumerate(item_list):
            if item['key']==key:
                return index
    def slugify_name(self, name):
        return name.replace(" ", "_").lower()
    
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
            
            # Close Event
            if event in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                break

            # EVENT: Register a new item
            if event == self.EVENTS['register_item']:
                file_path = values["path_input"]
                file_name = values["file_name_input"]
                file_category = self.item_categories[values["file_category_input"]]
                file_key = self.get_uuid()
                file_type = self.get_file_extension(file_path)
                
                file_data = {
                    "key": file_key,
                    "name": file_name,
                    "path": file_path,
                    "type": file_type,
                    "category": file_category
                }
                self.add_item(file_data)
                window.close()
                # TODO: select Tab 2 on refresh
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            # EVENT: Delete an item
            elif event.endswith(self.EVENTS['delete_item']):
                key = event.split("_")[0]
                self.delete_item(key)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            # EVENT: execute an item 
            elif event.endswith(self.EVENTS['open_item']):
                key = event.split("_")[0]
                index = self.find_item_index(key)
                os.startfile(self.get_registered_items()[index]['path'])
                
            # EVENT: apply filter to list of items
            elif event == self.EVENTS['apply_filter']:
                self.FILTER = values[event]
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            # EVENT: visit the repository link
            elif event == self.EVENTS['go_to_repo']:
                os.startfile("https://github.com/Blankscreen-exe/shortcut_keeper")

            # EVENT: set app theme
            elif event == self.EVENTS['set_app_theme']:
                theme = values["theme_dropdown"]
                self.update_app_theme(theme)
                window.close()
                sg.theme(self.app_theme)
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            # EVENT: set app title/id
            elif event == self.EVENTS['set_app_id']:
                title = values["new_window_title"]
                self.update_app_title(title)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)
                
            # EVENT: add file category
            elif event == self.EVENTS['add_category_popup']:
                popup_window = sg.Window('Add Category', self.get_add_category_layout())
                while True:
                    event_popup, value = popup_window.read()
                    if event_popup in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                        popup_window.close()
                        break
                        
                    elif event_popup == self.EVENTS['add_category']:
                        self.modify_settings(f"itemCategories.{value['category']}", self.slugify_name(value['category']))
                        self.set_item_categories()
                        popup_window.close()
                        break
                        
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)
                
            # EVENT: delete file category
            elif event == self.EVENTS['delete_category_popup']:
                popup_window = sg.Window('Delete Category', self.get_delete_category_layout())
                while True:
                    event_popup, value = popup_window.read()
                    if event_popup in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                        popup_window.close()
                        break
                        
                    elif event_popup == self.EVENTS['delete_category']:
                        self.delete_item_category(value['file_category_input'])
                        self.modify_settings(f"itemCategories", self.item_categories)
                        self.set_item_categories()
                        popup_window.close()
                        break
                        
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)
                
            

        window.close()


if __name__ == '__main__':
    App = shortcut_keeper()
    App.main()
