#!/usr/bin/python3
# -*- coding:Utf-8 -*-

# +--------------------------------------------------------------------------+
# | Layrageu                                                                 |
# | Copyright (C) 2022 Étienne Nadji                                         |
# |                                                                          |
# | This program is free software: you can redistribute it and/or modify     |
# | it under the terms of the GNU Affero General Public License as           |
# | published by the Free Software Foundation, either version 3 of the       |
# | License, or (at your option) any later version.                          |
# |                                                                          |
# | This program is distributed in the hope that it will be useful,          |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of           |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |
# | GNU Affero General Public License for more details.                      |
# |                                                                          |
# | You should have received a copy of the GNU Affero General Public License |
# | along with this program.  If not, see <https://www.gnu.org/licenses/>.   |
# +--------------------------------------------------------------------------+

"""
Layrageu : send Mastodon toots from Flat OpenDocument files. GUI.
"""

# Imports ===============================================================#

# Standard library ------------------------------

import os
import sys
import copy
import tempfile
import webbrowser

from functools import partial
from pathlib import Path
from typing import Optional, NoReturn

# Third parties ---------------------------------------------------

from appdirs import user_config_dir

# Tkinter -------------------------------------------------

import tkinter

from tkinter import ttk as ttk
from tkinter import filedialog as tkdialog
from tkinter import messagebox as messagebox

# ttkSimpleDialog -----------------------------------------

from ttkSimpleDialog import ttkSimpleDialog

# Layrageu --------------------------------------------------------

from layrageu import TOOT_VISIBILITIES, debug_mode
from layrageu.loader import convert
from layrageu.sender import send_toots
from layrageu.settings import Settings, slugify_instance_url

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"
__version__ = "0.2"

PREVIEW_DOC = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset=utf-8 />
        <title>Toot thread preview</title>
        <style>
            html { background-color: #191b22; color: white; }
            body {
                margin: 1em 0;
                display: grid;
                grid-template-columns: 1fr 4fr 1fr;
            }
            main { grid-column: 2; }
            @media screen and (max-width: 800px) {
                body { grid-template-columns: 1em 4fr 1em; }
            }
            article {
              font-size: 1em;
              line-height: 1.5;
              font-family: sans-serif;
              text-align: justify;
              margin-bottom: 1em;
              background-color: #282c37;
              padding: 5px 10px;
              border-radius: 5px;
            }
            article h1 {
                font-size: medium;
                text-align: center;
                margin: 0;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <main>
        {TOOTS}
        </main>
    </body>
</html>
"""

TOOT_PREVIEW = """\n<article>
<h1>Toot #{TOOT_IDX} ({TOOT_LENGTH})</h1><section>{TOOT_CONTENT}</section>
</article>\n"""

# Functions =============================================================#


def validate_missing(
    url: str, usermail: str, init_tootv: str, other_tootv: str
):
    """
    Common function to check Mastodon instance configuration form validity.
    """

    missing, message = False, "Some infos are missing:\n"

    for data, msg in [
        [url, "  – Instance url"],
        [usermail, "  – User mail"],
    ]:
        if not len(data):
            missing = True
            message += msg

    if missing:
        return False, message

    return True, ""


# Classes ===============================================================#


class NewInstanceWindow(tkinter.Toplevel):
    """
    New instance window.
    """

    def __init__(self, settings: Settings, app_frame: ttk.Frame):
        tkinter.Toplevel.__init__(self)

        self.app = app_frame
        self.settings = settings

        self.init_ui()

    def init_ui(self) -> NoReturn:
        """
        Initialize window's UI.
        """

        # Instance URL ---------------------------------------------------

        url_label = ttk.Label(self, text="Instance URL")
        self.url_entry = ttk.Entry(self)

        # Instance user mail ---------------------------------------------

        user_label = ttk.Label(self, text="User (mail)")
        self.user_entry = ttk.Entry(self)

        # Toots visibilities ---------------------------------------------

        # Initial toot -----------------------------------------

        initv_label = ttk.Label(self, text="Initial toot visibility")
        self.initv_combo = ttk.Combobox(self, values=TOOT_VISIBILITIES)
        self.initv_combo.current(TOOT_VISIBILITIES.index("public"))

        # Following toots --------------------------------------

        otherv_label = ttk.Label(self, text="Next toots visibility")
        self.otherv_combo = ttk.Combobox(self, values=TOOT_VISIBILITIES)
        self.otherv_combo.current(TOOT_VISIBILITIES.index("unlisted"))

        # Packing everything ---------------------------------------------

        ui_row = 2

        for label, widget in [
            [url_label, self.url_entry],
            [user_label, self.user_entry],
            [initv_label, self.initv_combo],
            [otherv_label, self.otherv_combo],
        ]:
            label.grid(column=1, row=ui_row, padx=5, pady=5, sticky=tkinter.E)
            widget.grid(
                column=2, row=ui_row, padx=5, columnspan=2, sticky=tkinter.W
            )
            ui_row += 1

        ui_row += 1

        ok_btn = ttk.Button(self, text="OK", command=self.validate)
        ok_btn.grid(column=2, row=ui_row, padx=5, pady=5, sticky=tkinter.E)

        cancel_btn = ttk.Button(self, text="Cancel", command=self.cancel)
        cancel_btn.grid(
            column=1,
            row=ui_row,
            padx=5,
            pady=5,
            columnspan=2,
            sticky=tkinter.W,
        )

    def validate(self) -> NoReturn:
        """
        Callback for OK button.
        """

        validated = False

        url = self.url_entry.get()
        usermail = self.user_entry.get()
        init_tootv = self.initv_combo.get()
        other_tootv = self.otherv_combo.get()

        validated, message = validate_missing(
            url, usermail, init_tootv, other_tootv
        )

        if not validated:
            messagebox.showwarning(title="Missing infos", message=message)
            return

        instance_name = slugify_instance_url(url)

        if self.settings.has_instance(instance_name):
            messagebox.showwarning(
                title=f"Instance already exists",
                message=f"“{instance_name}” instance already exists.",
            )
            return

        self.settings.add_instance(
            instance_name,
            url,
            usermail,
            init_tootv,
            other_tootv,
        )

        self.settings.save()
        self.app.refresh_settings()

        self.destroy()

    def cancel(self) -> NoReturn:
        """
        Callback for Cancel button.
        """
        self.destroy()


class FirstTimeSettings(tkinter.Toplevel):
    """
    First-time launch settings window.
    """

    def __init__(self, settings: Settings, app_frame: ttk.Frame):
        tkinter.Toplevel.__init__(self)

        self.app = app_frame
        self.settings = settings

        self.init_ui()

    def init_ui(self) -> NoReturn:
        """
        Initialize window's UI.
        """

        intro_label = ttk.Label(
            self,
            text="\n".join(
                [
                    "Please enter the details of your Mastodon",
                    "instance access.",
                    "",
                ]
            ),
        )
        intro_label.grid(
            column=1, row=1, padx=5, pady=5, columnspan=2, sticky=tkinter.EW
        )

        # Instance URL ---------------------------------------------------

        url_label = ttk.Label(self, text="Instance URL")
        self.url_entry = ttk.Entry(self)
        self.url_entry.insert(0, self.settings.instance_url("default"))

        # Instance user mail ---------------------------------------------

        user_label = ttk.Label(self, text="User (mail)")
        self.user_entry = ttk.Entry(self)

        # Toots visibilities ---------------------------------------------

        # Initial toot -----------------------------------------

        initv_label = ttk.Label(self, text="Initial toot visibility")
        self.initv_combo = ttk.Combobox(self, values=TOOT_VISIBILITIES)
        self.initv_combo.current(
            TOOT_VISIBILITIES.index(
                self.settings.instance_init_tootv("default")
            )
        )

        # Following toots --------------------------------------

        otherv_label = ttk.Label(self, text="Next toots visibility")
        self.otherv_combo = ttk.Combobox(self, values=TOOT_VISIBILITIES)
        self.otherv_combo.current(
            TOOT_VISIBILITIES.index(self.settings.instance_tootv("default"))
        )

        # Packing everything ---------------------------------------------

        ui_row = 2

        for label, widget in [
            [url_label, self.url_entry],
            [user_label, self.user_entry],
            [initv_label, self.initv_combo],
            [otherv_label, self.otherv_combo],
        ]:
            label.grid(column=1, row=ui_row, padx=5, pady=5, sticky=tkinter.E)
            widget.grid(
                column=2, row=ui_row, padx=5, columnspan=2, sticky=tkinter.W
            )
            ui_row += 1

        ui_row += 1

        ok_btn = ttk.Button(self, text="OK", command=self.validate)
        ok_btn.grid(column=2, row=ui_row, padx=5, pady=5, sticky=tkinter.E)

        cancel_btn = ttk.Button(self, text="Cancel", command=self.cancel)
        cancel_btn.grid(
            column=1,
            row=ui_row,
            padx=5,
            pady=5,
            columnspan=2,
            sticky=tkinter.W,
        )

    def validate(self) -> NoReturn:
        """
        Callback for OK button.
        """

        validated = False

        url = self.url_entry.get()
        usermail = self.user_entry.get()
        init_tootv = self.initv_combo.get()
        other_tootv = self.otherv_combo.get()

        validated, message = validate_missing(
            url, usermail, init_tootv, other_tootv
        )

        if not validated:
            messagebox.showwarning(title="Missing infos", message=message)
            return

        self.settings.instances["default"].url = url
        self.settings.instances["default"].usermail = usermail
        self.settings.instances["default"].first_tootv = init_tootv
        self.settings.instances["default"].other_tootv = other_tootv

        self.settings.save()
        self.app.refresh_settings()

        self.destroy()

    def cancel(self) -> NoReturn:
        """
        Callback for Cancel button.
        """
        self.destroy()
        self.app.quit()


class InstancesWindow(tkinter.Toplevel):
    """
    Settings window for Layrageu GUI.
    """

    def __init__(self, settings: Settings, app_frame: ttk.Frame):
        tkinter.Toplevel.__init__(self)

        self.app = app_frame
        self.settings = settings
        self.instances_ui = {}

        self.init_ui()

    def init_ui(self) -> NoReturn:
        """
        Initialize window's UI.
        """

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(
            column=1, row=1, padx=5, pady=5, columnspan=2, sticky=tkinter.W
        )

        for tab_id, instance in enumerate(self.settings.instances.keys()):
            self.instance_frame(instance, tab_id)

        ok_btn = ttk.Button(self, text="OK", command=self.validate)
        ok_btn.grid(column=2, row=2, padx=5, pady=5, sticky=tkinter.E)

        cancel_btn = ttk.Button(self, text="Cancel", command=self.cancel)
        cancel_btn.grid(
            column=1, row=2, padx=5, pady=5, columnspan=2, sticky=tkinter.W
        )

    def cancel(self) -> NoReturn:
        """
        Callback for Cancel button.
        """
        self.destroy()

    def validate(self) -> NoReturn:
        """
        Callback for OK button.
        """

        close = True

        for instance in self.settings.instances.keys():

            if instance not in self.instances_ui:
                continue

            url = self.instances_ui[instance]["url"].get()
            usermail = self.instances_ui[instance]["user"].get()
            init_tootv = self.instances_ui[instance]["init_tootv"].get()
            other_tootv = self.instances_ui[instance]["tootv"].get()

            validated, message = validate_missing(
                url, usermail, init_tootv, other_tootv
            )

            if not validated:
                messagebox.showwarning(
                    title="Missing infos : {instance} instance",
                    message=message,
                )
                close = False
                continue

            self.settings.instances[instance].url = url
            self.settings.instances[instance].usermail = usermail
            self.settings.instances[instance].first_tootv = init_tootv
            self.settings.instances[instance].other_tootv = other_tootv
            self.settings.save()

        if close:
            self.app.refresh_settings()
            self.destroy()

    def delete_instance(self, instance_name: str) -> NoReturn:
        """
        Tells Layrageu settings to delete instance called `instance_name`.
        """

        result = messagebox.askquestion(
            f"Delete “{instance_name}” instance ?",
            f"Are you sure you want to delete “{instance_name}” instance ?",
        )

        if result == "yes":
            self.notebook.forget(self.instances_ui[instance_name]["tab_id"])
            self.instances_ui.pop(instance_name)

            self.settings.delete_instance(instance_name)

            self.app.refresh_instances()

            if len(self.settings.instances) == 1:
                self.destroy()

    def instance_frame(self, instance_name: str, tab_id: int) -> NoReturn:
        """
        Create an instance settings Frame to put in the Instances window
        notebook.
        """

        instance_frame = ttk.Frame(self.notebook)

        self.instances_ui[instance_name] = {
            "name": instance_name,
            "frame": instance_frame,
            "tab_id": tab_id,
        }

        # Instance URL ---------------------------------------------------

        url_label = ttk.Label(instance_frame, text="Instance URL")
        url_entry = ttk.Entry(instance_frame)
        url_entry.insert(0, self.settings.instance_url(instance_name))
        self.instances_ui[instance_name]["url"] = url_entry

        # Instance user mail ---------------------------------------------

        user_label = ttk.Label(instance_frame, text="User (mail)")
        user_entry = ttk.Entry(instance_frame)
        user_entry.insert(0, self.settings.instance_user(instance_name))
        self.instances_ui[instance_name]["user"] = user_entry

        # Toots visibilities ---------------------------------------------

        # Initial toot -----------------------------------------

        initv_label = ttk.Label(instance_frame, text="Initial toot visibility")
        initv_combo = ttk.Combobox(instance_frame, values=TOOT_VISIBILITIES)
        initv_combo.current(
            TOOT_VISIBILITIES.index(
                self.settings.instance_init_tootv(instance_name)
            )
        )
        self.instances_ui[instance_name]["init_tootv"] = initv_combo

        # Following toots --------------------------------------

        otherv_label = ttk.Label(instance_frame, text="Next toots visibility")
        otherv_combo = ttk.Combobox(instance_frame, values=TOOT_VISIBILITIES)
        otherv_combo.current(
            TOOT_VISIBILITIES.index(
                self.settings.instance_tootv(instance_name)
            )
        )
        self.instances_ui[instance_name]["tootv"] = otherv_combo

        # Delete instance button -----------------------------------------

        delete_btn = ttk.Button(
            instance_frame,
            text="Delete instance",
            command=partial(self.delete_instance, instance_name),
        )

        # Packing everything ---------------------------------------------

        ui_row = 1

        for label, widget in [
            [url_label, url_entry],
            [user_label, user_entry],
            [initv_label, initv_combo],
            [otherv_label, otherv_combo],
        ]:
            label.grid(column=1, row=ui_row, padx=5, pady=5, sticky=tkinter.E)
            widget.grid(
                column=2, row=ui_row, padx=5, columnspan=2, sticky=tkinter.W
            )
            ui_row += 1

        delete_btn.grid(column=2, row=ui_row, padx=5, pady=5, sticky=tkinter.W)

        # Add instance tab -----------------------------------------------

        self.notebook.add(instance_frame, text=instance_name)


class Layrageu(ttk.Frame):
    """
    Main window of Layrageu GUI.
    """

    def __init__(
        self,
        master: Optional[tkinter.Tk] = None,
    ):
        ttk.Frame.__init__(self, master)

        self.debug_mode = debug_mode()

        # Settings ---------------------------------------------

        self.settings = Settings(user_config_dir("layrageu"))

        # Window style -----------------------------------------

        style = ttk.Style(self)

        if sys.platform.startswith("linux"):
            style.theme_use("clam")

        # GUI data ---------------------------------------------

        self.document = None
        self.toots = []

        # ------------------------------------------------------

        self.master = master

        self.ui_vars = {"sensible": tkinter.IntVar()}

        self.init_ui()
        self.init_menu()

        if self.settings.needs_first_user_action():
            wizard_window = FirstTimeSettings(self.settings, self)
            wizard_window.title("First time configuration")

    def init_menu(self) -> NoReturn:
        """
        Initialize menus.
        """

        def new_menu(parent, menu_items):
            new_menu = tkinter.Menu(parent)

            for item in menu_items:
                if item[0] == "<separator>":
                    new_menu.add_separator()
                else:
                    new_menu.add_command(label=item[0], command=item[1])

            return new_menu

        app_menu = tkinter.Menu(self.master)
        self.master.config(menu=app_menu)

        file_menu = new_menu(
            app_menu,
            [
                # ["<separator>", None],
                ["Quit", self.quit],
            ],
        )

        instances_menu = new_menu(
            app_menu,
            [
                ["Configure", self.open_instances],
                ["New", self.new_instance],
            ],
        )

        help_menu = new_menu(
            app_menu,
            [
                ["About", self.about],
            ],
        )

        instance_menu_label = {True: "Instances", False: "Instance"}[
            self.settings.instances_count() > 1
        ]

        for submenu in [
            ["File", file_menu],
            [instance_menu_label, instances_menu],
            ["Help", help_menu],
        ]:
            app_menu.add_cascade(
                label=submenu[0],
                menu=submenu[1],
            )

    def init_ui(self) -> NoReturn:
        """
        Initialize Layrageu's UI.
        """

        # Main frame (we want some padding around everything) ------------

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.grid(padx=5, pady=5)

        # Document -------------------------------------------------------

        doc_btn = ttk.Button(
            self.main_frame, text="Document", command=self.select_document
        )
        doc_btn.grid(column=1, row=1, padx=5)

        self.doc_entry = ttk.Entry(self.main_frame)
        self.doc_entry.grid(
            column=2, row=1, padx=5, columnspan=2, sticky=tkinter.W
        )

        # Content warning ------------------------------------------------

        cw_label = ttk.Label(self.main_frame, text="Warning")
        cw_label.grid(column=1, row=2, padx=5, pady=5, sticky=tkinter.E)

        self.cw_entry = ttk.Entry(self.main_frame)
        self.cw_entry.grid(
            column=2, row=2, padx=5, columnspan=2, sticky=tkinter.W
        )

        # Instances ------------------------------------------------------

        instances_label = ttk.Label(self.main_frame, text="Send on instance")
        instances_label.grid(column=1, row=3, padx=5, pady=5, sticky=tkinter.E)

        self.instances_combo = ttk.Combobox(self.main_frame)
        self.instances_combo.grid(
            column=2, row=3, padx=5, pady=5, columnspan=2, sticky=tkinter.W
        )
        self.refresh_instances()

        # Sensible posts -------------------------------------------------

        self.sensible_check = ttk.Checkbutton(
            self.main_frame, text="Sensible", variable=self.ui_vars["sensible"]
        )
        self.sensible_check.grid(column=1, row=4, pady=5)

        # Send and preview buttons ---------------------------------------

        send_btn = ttk.Button(
            self.main_frame, text="Send toots", command=self.send
        )
        send_btn.grid(column=2, row=5, columnspan=3, padx=5, sticky=tkinter.EW)

        prev_btn = ttk.Button(
            self.main_frame, text="Preview", command=self.preview
        )
        prev_btn.grid(column=1, row=5, padx=5)

    def open_instances(self) -> NoReturn:
        """
        Open the Settings window.
        """
        instances_window = InstancesWindow(self.settings, self)
        instances_window.title("Instances")

    def new_instance(self) -> NoReturn:
        """
        Open the New instance window.
        """
        instances_window = NewInstanceWindow(self.settings, self)
        instances_window.title("New instance")

    def refresh_instances(self) -> NoReturn:
        self.instances_combo["values"] = self.settings.instances_names()
        self.instances_combo.delete(0, "end")
        self.instances_combo.current(0)

    def refresh_settings(self) -> NoReturn:
        """
        Refresh settings when InstancesWindow window is destroyed with
        `InstancesWindow.validate`.
        """
        self.refresh_instances()

    def about(self) -> NoReturn:
        """
        Layrageu's About window.
        """

        messagebox.showinfo(
            "About Layrageu",
            "\n".join(
                [
                    f"Layrageu {__version__}",
                    "",
                    "Copyright © 2022 Étienne Nadji",
                    "",
                    "Layrageu is published under GNU Affero General Public "
                    "License v3 or later (AGPLv3+)",
                ]
            ),
        )

        return True

    def quit(self) -> NoReturn:
        """
        Quit Layrageu GUI.
        """
        sys.exit()

    def select_document(self) -> NoReturn:
        document = tkdialog.askopenfile().name
        self.document = Path(document).resolve(True)

        self.toots = []

        self.doc_entry.delete(0, "end")
        self.doc_entry.insert(0, self.document.name)

    def load_toots(self) -> bool:
        """
        Load Mastodon thread toots.

        :rtype: bool
        :returns: True if toots were loaded.
        """

        if self.document is None:
            return False

        if self.toots:
            return True

        # Load toots from Flat OpenDocument files
        self.toots = convert(self.document)

        return True

    def preview(self) -> bool:
        """
        Preview loaded document's Mastodon thread.

        :rtype: bool
        """

        # Check if there is toots to use ---------------------------------

        toots_loaded = self.load_toots()

        if not toots_loaded:
            return False

        # Create an HTML preview file ------------------------------------

        preview_doc = copy.deepcopy(PREVIEW_DOC)
        toots_content = ""

        for idx, toot in enumerate(self.toots):
            toot_content = copy.deepcopy(TOOT_PREVIEW)

            toot_content = toot_content.replace("{TOOT_IDX}", str(idx + 1))
            toot_content = toot_content.replace(
                "{TOOT_LENGTH}", str(len(toot))
            )
            toot_content = toot_content.replace(
                "{TOOT_CONTENT}", toot.as_html()
            )

            toots_content += toot_content

        preview_doc = preview_doc.replace("{TOOTS}", toots_content)

        # Write and open the temporary file ------------------------------

        webpreview = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False
        )
        webpreview.write(preview_doc)

        url = f"file://{webpreview.name}"

        webpreview.close()

        # ----------------------------------------------------------------

        webbrowser.open_new_tab(url)

        return True

    def send(self) -> bool:
        """
        Send loaded document's Mastodon thread.

        :rtype: bool
        """

        # Check if there is toots to use ---------------------------------

        toots_loaded = self.load_toots()

        if not toots_loaded:
            return False

        # Prepare toots send ---------------------------------------------

        # Get instance name
        instance_name = self.instances_combo.get()

        if not self.settings.has_instance(instance_name):
            return False

        # Password ---------------------------------------------

        password = ttkSimpleDialog.askstring(
            title="Layrageu",
            prompt="Enter your Mastodon's instance password.",
            show="*",
        )

        if password is None or not password:
            messagebox.showerror(
                title="Empty password",
                message="You entered an empty password.",
            )
            return False

        # Content warning --------------------------------------

        content_warning = self.cw_entry.get().rstrip()

        if not content_warning:
            content_warning = None

        # Send toots -----------------------------------------------------

        result = send_toots(
            instance_name,
            self.settings,
            self.toots,
            password,
            content_warning,
            bool(self.ui_vars["sensitive"].get()),
        )

        # Open Mastodon instance in case of sending success --------------

        if result:
            webbrowser.open_new_tab(self.settings.instance_url(instance_name))

        return True


# Fonctions =============================================================#


def starting_dimensions() -> str:
    os_window_dims = {
        "win": [345, 175],
        "linux": [345, 175],
        "darwin": [345, 175],
    }

    # MacOS always needs bigger dimensions, so this a good fallback
    dimensions = os_window_dims["darwin"]

    try:
        dimensions = os_window_dims[sys.platform]
    except IndexError:
        for platform, sizes in os_window_dims.items():
            if not sys.platform.startswith(platform):
                continue

            dimensions = sizes

    return f"{dimensions[0]}x{dimensions[1]}"


def main() -> NoReturn:
    """
    Layrageu GUI entry point.
    """

    # --- Tkinter / Layrageu startup -------------------------------------

    env = tkinter.Tk()
    application = Layrageu(env)

    env.wm_title("Layrageu")
    env.geometry(starting_dimensions())

    # --- Running the GUI ------------------------------------------------

    env.mainloop()
    sys.exit(0)


# Programme =============================================================#

if __name__ == "__main__":
    main()

# vim:set shiftwidth=4 softtabstop=4:
