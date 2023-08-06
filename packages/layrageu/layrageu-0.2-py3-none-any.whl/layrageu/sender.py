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
Layrageu : module file for sending toots.
"""

# Imports ===============================================================#

# Standard library ------------------------------

from typing import List, Optional

# Third parties ---------------------------------

from rich.progress import Progress

from mastodon import Mastodon

# Layrageu --------------------------------------

from layrageu.loader import Toot
from layrageu.settings import Settings

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# Fonctions =============================================================#


def send_toots(
    instance_name: str,
    settings: Settings,
    toots: List[Toot],
    password: str,
    warning: Optional[str] = None,
    sensitive: bool = False,
    terminal: bool = False,
) -> bool:
    """
    Send toots to Mastodon.

    :type instance_name: str
    :param instance_name: Name of the Mastodon instance in Layrageu settings.
    :type settings: layrageu.settings.Settings
    :param settings: Layrageu settings
    :type toots: List[layrageu.loader.Toot]
    :param toots: List of Mastodon toots to send.
    :type password: str
    :param password: User's password for the Mastodon instance.
    :type warning: Optional[str]
    :param warning: Content warning title.
    :type sensitive: bool
    :param sensitive: Content warning title.
    :rtype: bool
    """

    def send_toot(
        toot_idx: int,
        instance: Mastodon,
        toot_visiblity: str,
        init_toot_visiblity: str,
        toot: Toot,
        warning: Optional[str],
        sensitive: bool,
        reply_to: str,
    ) -> str:
        # Select toot visibily -----------------------

        target = toot_visiblity

        if toot_idx == 0:
            target = init_toot_visiblity

        # --------------------------------------------

        status_data = instance.status_post(
            status=str(toot),
            visibility=target,
            spoiler_text=warning,
            in_reply_to_id=reply_to,
            sensitive=sensitive,
        )

        # Parameters for the next toot to send -------

        reply_to = status_data["id"]

        return reply_to

    # Getting application Token ------------------------------------------

    token = settings.folder / f"layrageu_{instance_name}.secret"

    Mastodon.create_app(
        "Layrageu",
        api_base_url=settings.instance_url(instance_name),
        to_file=token,
    )

    instance = Mastodon(
        client_id=token, api_base_url=settings.instance_url(instance_name)
    )

    # Log in the instance ------------------------------------------------

    try:
        instance.log_in(
            settings.instance_user(instance_name), password, to_file=token
        )
    except Mastodon.MastodonIllegalArgumentError:
        print("Unable to log in Mastodon instance.")
        print("You should try again later.")

        return False

    # Toot visibility ------------------------------------------------

    toot_visiblity = settings.instance_tootv(instance_name)
    init_toot_visiblity = settings.instance_init_tootv(instance_name)

    # Unlisted visibility is public, but initial toot is private.
    # If the user selected private for initial toot, there is no point
    # making the following toots public, even if they are unlisted.
    if init_toot_visiblity == "private":
        toot_visiblity = "private"

    # The first toot ID to reply is None, because each toot responds to
    # the previous one.
    reply_to = None

    # Sending toots --------------------------------------------------

    if terminal:
        # perc_update = 100 / len(toots)

        with Progress() as progress:
            print()

            sending = progress.add_task("Sending toots…", total=len(toots))

            for idx, toot in enumerate(toots):
                reply_to = send_toot(
                    idx,
                    instance,
                    toot_visiblity,
                    init_toot_visiblity,
                    toot,
                    warning,
                    sensitive,
                    reply_to,
                )

                progress.update(sending, advance=1)

        return True

    for idx, toot in enumerate(toots):
        reply_to = send_toot(
            idx,
            instance,
            toot_visiblity,
            init_toot_visiblity,
            toot,
            warning,
            reply_to,
        )

    return True


# vim:set shiftwidth=4 softtabstop=4:
