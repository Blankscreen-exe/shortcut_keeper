import PySimpleGUI as sg
import os

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
    app_title: str
        The default title of the app.
    app_id: str
        The unique ID of the app.
    window: PySimpleGUI.Window
        The main window of the app.
        
    Methods:
    --------
    get_registered_items_layout() -> list:
        Generates the layout for the list view of the registered items.
        
    get_register_item_layout() -> list:
        Generates the layout for the shortcut registration form.
        
    about_section() -> list:
        Generates the layout for the about section.
        
    settings_layout() -> list:
        Generates the layout for the settings section.
        
    add_registered_item(path: str) -> None:
        Adds/writes the path to a file to the config file.
        
    delete_registered_item(index: int) -> None:
        Deletes/removes the path to a file from the config file.
    """

    def __init__(self):
        self.app_theme = "Reddit"
        self.window_size = (300, 220)
        self.section_title_font = ("Arcadeclassic", 17)
        self.section_normal_font = ("MS Sans Serif", 10)
        self.app_icon = "./edit.ico"
        self.app_title = "Shortcut Keeper"
        self.app_id = "asd"
        self.window = sg.Window(self.get_app_title(),
                                self.tab_group(), icon=self.app_icon)

    def get_registered_items_layout(self) -> list:
        """generates layout for List view of the registered items

        Returns:
            layout (list): pysimplegui layout list
        """
        registered_items = self.get_registered_item()
        list_of_registered_items = []
        for i, path in enumerate(registered_items):
            list_of_registered_items.append([
                sg.Button("❌", key=f"{i}_delete_button"),
                sg.Button("↗️", key=f"{i}_open_button"),
                sg.Text(os.path.basename(path),
                        key=f"{i}_path_button", tooltip=path)
            ])

        empty_message = [
            [sg.Text("=====================", font=self.section_normal_font)],
            [sg.Text("WOW Such Empty!", font=self.section_normal_font)],
            [sg.Text("=====================", font=self.section_normal_font)]
        ]

        list_out = [
            sg.Column(
                empty_message if list_of_registered_items == 0 else list_of_registered_items,
                scrollable=True,
                vertical_scroll_only=True,
                size=self.get_window_size()
            )
        ]

        layout = [
            [sg.HorizontalSeparator()],

            list_out

        ]
        return layout

    def get_register_item_layout(self) -> list:
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
                sg.Button("Submit", key="submit_button")
            ]
        ]
        return layout

    def about_section(self) -> list:
        """about section

        Returns:
            layout (list): pysimplegui layout list
        """
        layout = [
            [sg.Text("📜 About  Shortcut  Keeper",
                     font=self.section_title_font)],
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
            [sg.Text("🔗 https://www.abc.com", enable_events=True, font=("Consolas", 12),
                     text_color='#0F3FD8', background_color='#B2C00D', key="-ABOUT-LINK-")]
        ]
        return layout

    def settings_layout(self) -> list:
        """settings section

        Returns:
            layout (list): pysimplegui layout list
        """
        inp_size = (20, 200)

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

    def add_registered_item(self, path) -> None:
        """adds/writes path to a file to the config file

        Args:
            path (str): path to file
        """
        registered_items = self.get_registered_item()
        registered_items.append(path)
        with open('sk_cfg.txt', 'w') as f:
            for path in registered_items:
                f.write(path + '\n')

    def delete_registered_item(self, index) -> None:
        """deletes/removes path to a file from the config file

        Args:
            index (int): index of the path in the file
        """
        registered_items = self.get_registered_item()
        del registered_items[index]
        with open('sk_cfg.txt', 'w') as f:
            for path in registered_items:
                f.write(path + '\n')

    def tab_group(self) -> list:
        """config for displaying tabs

        Returns:
            tab_group (list): pysimplegui layout lists
        """
        tab_group = [[
            sg.TabGroup([
                [sg.Tab('List', self.get_registered_items_layout())],
                [sg.Tab('Register Shortcuts', self.get_register_item_layout())],
                [sg.Tab("Settings", self.settings_layout())],
                [sg.Tab('About', self.about_section())]
            ])
        ]]
        return tab_group

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
        return sg.theme_list()

    def get_registered_item(self) -> list:
        """getter method for list of registered items (filess)

        Returns:
            registered_items (list): list of paths
        """
        registered_items = []
        if os.path.isfile('sk_cfg.txt'):
            with open('sk_cfg.txt', 'r') as f:
                for path in f:
                    registered_items.append(path.strip())
        return registered_items

    def get_app_title(self) -> str:
        """getter method for app title

        Returns:
            str: app's title
        """
        return self.app_title

    def reset_app_theme(self, theme) -> None:
        """sets app theme

        Args:
            theme (str): theme for the app
        """
        self.app_theme = theme

    def reset_app_title(self, title) -> None:
        """sets app theme

        Args:
            theme (str): theme for the app
        """
        self.app_title = title

    def main(self) -> None:
        """Main window loop to start this app
        """
        # sg.theme(self.app_theme)
        window = self.window

        while True:

            # set theme
            sg.theme(self.app_theme)
            # read events and their values
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "WIN_CLOSED", "Exit"):
                break

            # shortcut events
            if event == "submit_button":
                path = values["path_input"]
                self.add_registered_item(path)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event.endswith("_delete_button"):
                index = int(event.split("_")[0])
                self.delete_registered_item(index)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event.endswith("_open_button"):
                index = int(event.split("_")[0])
                os.startfile(self.get_registered_item()[index])

            # hyperlink events
            elif event == "-ABOUT-LINK-":
                os.startfile("https://www.abc.com")

            # settings events
            elif event == "set_theme":
                theme = values["theme_dropdown"]
                self.reset_app_theme(theme)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

            elif event == "set_app_title":
                title = values["new_window_title"]
                self.reset_app_title(title)
                window.close()
                window = sg.Window(self.get_app_title(),
                                   self.tab_group(), icon=self.app_icon)

        window.close()


if __name__ == '__main__':
    App = shortcut_keeper()
    sg.theme("Reddit")
    App.main()
