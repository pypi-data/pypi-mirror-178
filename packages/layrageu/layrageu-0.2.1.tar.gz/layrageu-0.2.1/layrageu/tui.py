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

"""Layrageu : send Mastodon toots from Flat OpenDocument files.

Usage:
  tui.py send <document> [--instance=name] [--cw=title] [--sensitive]
                         [--preview] [--nopager] [--verbose]
  tui.py preview <document> [--nopager] [--verbose]
  tui.py configure [--name=<name>] [--url=<url>] [--user=<mail>]
                   [--ftv=<toot_visibility>] [--ntv=<toots_visibility>]
                   [--always-sensitive] [--verbose]
  tui.py version

Options:
  -h --help                Displays help.
  --verbose                Verbosity of the command.
  --preview                Preview toots before sending.
  --nopager                Always disable pager on toots preview.
  --sensitive              Marks the thread's toots as sensitive.
  --url=<url>              URL of the instance.
  --user=<mail>            User mail for the instance.
  --name=<name>            Name of the instance. [default: default]
  --ftv=<toot_visibility>  Visibility of first toot. Must be private,
                           unlisted or public. public by default.
  --ntv=<toots_visibility> Visibility of following toots. Must be private,
                           unlisted or public. unlisted by default.
  --always-sensitive       Posts on this instance will be marked as sensitive.

Layrageu. Copyright (C) 2022 Étienne Nadji.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.
"""

# Imports ===============================================================#

# Standard library ------------------------------

import os
import sys
import getpass

from pathlib import Path
from typing import List

# Third parties ---------------------------------

import docopt

from appdirs import user_config_dir

from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt, Confirm

# Layrageu --------------------------------------

from layrageu import TOOT_VISIBILITIES, debug_mode
from layrageu.loader import convert, Toot
from layrageu.sender import send_toots
from layrageu.settings import Settings

# Variables globales ====================================================#

__author__ = "Étienne Nadji <etnadji@eml.cc>"
__version__ = "0.2.1"

# Classes ===============================================================#


class Layrageu:
    COMMANDS = ["preview", "send", "configure", "version"]

    def __init__(
        self,
        arguments: dict,
    ):
        # CLI arguments and debug mode -----------------------------------

        self.arguments = arguments
        self.debug_mode = debug_mode()

        # Load Layrageu's settings ---------------------------------------

        self.settings = Settings(user_config_dir("layrageu"))

        # Find which command is used -------------------------------------

        self.command = False

        for command in Layrageu.COMMANDS:
            if self.arguments[command]:
                self.command = command
                break

        # Initializes rich Console ---------------------------------------

        self.console = Console()

    def _load_document(self) -> List[Toot]:
        """
        Load FODT documents as Mastodon toots.
        """
        return convert(
            self.arguments["<document>"], self.arguments["--verbose"]
        )

    def wizard(self) -> bool:
        """
        Instance access configuration wizard for the first time the user
        use a command that requires instance access.

        :rtype: bool
        :returns: Configuration success.
        """

        self.console.print(
            Panel("[yellow]Layrageu configuration wizard[/yellow]", width=33)
        )
        self.console.print(
            "\nYou didn't configure your Mastodon instance access.\n"
        )

        do_config = Confirm.ask("Would you like to configure it now?")

        if not do_config:
            return False

        clear = False
        wizard_loop = True

        url = None
        usermail = None
        first_tootv = "private"
        other_tootv = "private"

        while wizard_loop:

            if clear:
                self.console.clear()
            else:
                print()

            url = Prompt.ask("Instance URL")

            if not url:
                self.console.print("[red]Empty instance URL[/red]")
                continue

            usermail = Prompt.ask("User mail")

            if not usermail:
                self.console.print("[red]Empty user mail[/red]")
                continue

            first_tootv = Prompt.ask(
                "First toot visibility",
                choices=TOOT_VISIBILITIES,
                default="private",
            )
            other_tootv = Prompt.ask(
                "Next toots visibility",
                choices=TOOT_VISIBILITIES,
                default="unlisted",
            )

            summary_width = len(url) + 20

            print()

            self.console.print(
                Panel(
                    "\n".join(
                        [
                            "[blue]Access[/blue]",
                            "",
                            f"[yellow]User mail[/yellow] : {usermail}",
                            f"[yellow]Instance URL[/yellow] : {url}",
                            "",
                            "[blue]Toots visibilities[/blue]",
                            "",
                            f"[yellow]First toot[/yellow] : {first_tootv}",
                            f"[yellow]Next toots[/yellow] : {other_tootv}",
                        ]
                    ),
                    width=summary_width,
                )
            )

            print()

            do_set = Confirm.ask("Are you OK with those options ?")

            if do_set:
                wizard_loop = False
            else:
                clear = True

        self.console.clear()

        url = None
        usermail = None
        first_tootv = "private"
        other_tootv = "private"

        instance = self.settings.instances[-1]

        instance.url = url
        instance.usermail = usermail
        instance.first_tootv = first_tootv
        instance.other_tootv = other_tootv

        return True

    def run(self) -> int:
        methods = {
            "send": self.cmd_send,
            "preview": self.cmd_preview,
            "version": self.cmd_version,
            "configure": self.cmd_configure,
        }

        return methods[self.command]()

    def cmd_version(self) -> int:
        print(__version__)
        return 0

    def cmd_preview(self) -> int:
        """
        preview command : Preview toots.
        """

        def toot_as_preview(toot_index, toot):
            return Panel(
                toot.as_markdown(),
                width=80,
                title=f"\nToot {toot_index+1} ({len(toot)})",
            )

        toots = self._load_document()

        if self.arguments["--nopager"]:
            use_pager = False
        else:
            use_pager = sum([len(toot) for toot in toots]) >= 1500

        if use_pager:
            print("[Previewed in terminal pager]")

            with self.console.pager():
                for idx, toot in enumerate(toots):
                    self.console.print(toot_as_preview(idx, toot))

            return 0

        for idx, toot in enumerate(toots):
            self.console.print(toot_as_preview(idx, toot))

        return 0

    def cmd_send(self) -> int:
        """
        send command : Send toots to Mastodon instance.
        """

        toots = self._load_document()

        # Preview the toots before sending them --------------------------

        if self.arguments["--preview"]:
            self.cmd_preview()
            print()

        # First-time configuration wizard --------------------------------

        if self.settings.needs_first_user_action():
            configured = self.wizard()

            if not configured:
                return 1

        # Check selected instance ----------------------------------------

        instance_name = "default"

        if self.arguments["--instance"] is not None:
            instance_name = self.arguments["--instance"]

        if not self.settings.mi_exists(instance_name):
            print(
                f"Critical: Mastodon instance “{self.arguments['--instance']}” "
                "does not exists in Layrageu's configuration."
            )
            return 1

        # ----------------------------------------------------------------

        try:
            password = self.console.input(
                "[red]Password[red] : ", password=True
            )

            result = send_toots(
                instance_name,
                self.settings,
                toots,
                password,
                self.arguments["--cw"],
                self.arguments["--sensitive"],
                terminal=True,
            )
        except KeyboardInterrupt:
            return 0

        # ----------------------------------------------------------------

        return {True: 0, False: 1}[result]

    def cmd_configure(self) -> int:
        """
        configure command : create or modify a Mastodon instance.
        """

        opt_errors = False
        has_instance = self.settings.mi_exists(self.arguments["--name"])

        # Default value is not defined with docopt string, because configure
        # command is used to create AND modify instances. So if toot visibility
        # options were set, the user would override those options by mistake.
        if not has_instance:
            if self.arguments["--ftv"] is None:
                self.arguments["--ftv"] = "public"
            if self.arguments["--ntv"] is None:
                self.arguments["--ntv"] = "unlisted"

        # Check if visibility options use the correct set of values.
        for option in ["--ftv", "--ntv"]:
            if self.arguments[option] in TOOT_VISIBILITIES:
                continue

            print(
                f"Wrong option value : {option} must be "
                "private, unlisted or public (without quotes).\n\t"
                f"Got '{self.arguments[option]}'."
            )
            opt_errors = True

        # Check if mandatory options when creating an instance are not empty.
        if not has_instance:
            for option in ["--url", "--user"]:
                if self.arguments[option] is not None:
                    continue

                print(
                    f"Wrong option value : {option} is mandatory, yet empty."
                )
                opt_errors = True

        # Options are so wrong that Layrageu don't want to live anymore.
        if opt_errors:
            return 1

        # Modify a Mastodon instance -------------------------------------

        if has_instance:
            instance_name = self.arguments["--name"]

            if self.arguments["--url"] is not None:
                self.settings.instances[instance_name].url = self.arguments[
                    "--url"
                ]

            if self.arguments["--user"] is not None:
                self.settings.instances[
                    instance_name
                ].usermail = self.arguments["--user"]

            if self.arguments["--ftv"]:
                self.settings.instances[
                    instance_name
                ].first_tootv = self.arguments["--ftv"]

            if self.arguments["--ntv"]:
                self.settings.instances[
                    instance_name
                ].other_tootv = self.arguments["--ntv"]

            self.settings.instances[
                instance_name
            ].always_sensitive = self.arguments["--always-sensitive"]

            self.settings.save()

            return 0

        # Creating a Mastodon instance -----------------------------------

        self.settings.add_instance(
            self.arguments["--name"],
            self.arguments["--url"],
            self.arguments["--user"],
            self.arguments["--ftv"],
            self.arguments["--ntv"],
            self.arguments["--always-sensitive"],
        )

        self.settings.save()

        # ----------------------------------------------------------------

        return 0


# Fonctions =============================================================#


def main():
    """
    Layrageu command line entry point.
    """

    exitcode = 0

    ARGUMENTS = docopt.docopt(__doc__, version=__version__)

    if debug_mode():
        print("\nCLI arguments :", ARGUMENTS, "\n")

    app = Layrageu(ARGUMENTS)

    exitcode = app.run()

    sys.exit(exitcode)


# Programme =============================================================#

if __name__ == "__main__":
    main()


# vim:set shiftwidth=4 softtabstop=4:
