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
Layrageu : settings.
"""

# Imports ===============================================================#

# Standard library ------------------------------

import configparser

import re
import unicodedata

from pathlib import Path
from typing import Literal, NoReturn, List
from collections import OrderedDict

# Third parties ---------------------------------

from slugify import slugify

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

TootVisibility = Literal["private", "unlisted", "public"]

# Functions =============================================================#


def slugify_instance_url(url: str) -> str:
    """
    Slugify an instance URL. Used as a better default name for a new
    instance.

    `https://mastodon.social` ⇒ `mastodon-social`

    :type url: str
    :param url: Instance URL
    :rtype: str
    """
    unprotocoled = url.split("//")[1:]
    slug_base = "/".join(unprotocoled)

    try:
        slug = slugify(slug_base)
    except NameError:
        # Fallback to slugify use of unicode()
        slug = slug_base.replace("/", "-")
        slug = slug.replace(".", "-")

    return slug


# Classes ===============================================================#


class MastodonInstance:
    """
    Mastodon instance class.
    """

    def __init__(
        self,
        name: str,
        url: str,
        usermail: str,
        first_tootv: TootVisibility = "private",
        other_tootv: TootVisibility = "private",
    ):
        self.name = name
        self.url = url
        self.usermail = usermail
        self.first_tootv = first_tootv
        self.other_tootv = other_tootv

    def slugifyed_url(self) -> str:
        """
        Return a slug of this instance URL.

        :rtype: str
        """
        return slugify_instance_url(self.url)

    def as_dict(self) -> dict:
        """
        Returns self as a dictionnary.
        """

        return {
            "url": self.url,
            "user": self.usermail,
            "tootv": self.other_tootv,
            "init_tootv": self.first_tootv,
        }

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other) -> bool:
        if not isinstance(other, MastodonInstance):
            raise TypeError("Comparing self with a MastodonInstance instance.")

        return self.__repr__() == other.__repr__()


class Settings:
    """
    Layrageu's settings file class.
    """

    def __init__(self, folder: Path):
        self.apps = OrderedDict()
        self.instances = OrderedDict()

        # Create the settings folder if it doesn't exists ----------------

        self.folder = Path(folder).resolve(False)
        self.folder.mkdir(exist_ok=True)

        # Transition from legacy settings file ---------------------------

        legacy = self.folder / "settings.ini"

        if legacy.exists():
            legacy.rename(self.folder / "instances.ini")

        # ----------------------------------------------------------------

        self.files = {
            "apps": self.folder / "apps.ini",
            "instances": self.folder / "instances.ini",
        }

        as_new = not self.files["instances"].exists()

        # ----------------------------------------------------------------

        if as_new:
            self.create()
        else:
            self.load()

    def instances_count(self) -> int:
        """
        Returns count of known instances.

        :rtype: int
        """
        return len(self.instances)

    def instances_names(self) -> List[str]:
        """
        Returns names of known instances.

        :rtype: List[str]
        """
        return list(self.instances.keys())

    def needs_first_user_action(self) -> bool:
        """
        Returns True if there is only one access configured, which is the
        default (and unusable) access.

        :rtype: bool
        """

        if self.instances_count() > 1:
            return False

        default = MastodonInstance(
            "default",
            "https://example.com",
            "user@mail.example.com",
            "public",
            "unlisted",
        )

        return [v for v in self.instances.values()][0] == default

    def add_instance(
        self,
        name: str,
        url: str,
        usermail: str,
        first_tootv: TootVisibility = "private",
        other_tootv: TootVisibility = "private",
    ) -> NoReturn:
        """
        Add a new Mastodon instance access.

        :type name: str
        :type url: str
        :type usermail: str
        :type first_tootv: Literal["private", "unlisted", "public"]
        :type other_tootv: Literal["private", "unlisted", "public"]
        """

        new_instance = MastodonInstance(
            name,
            url,
            usermail,
            first_tootv,
            other_tootv,
        )

        self.instances[name] = new_instance

    def save(self) -> bool:
        """
        Save the settings.

        :rtype: bool
        """

        # Instances settings ---------------------------------------------

        parser = configparser.ConfigParser()

        for name, instance in self.instances.items():
            for option_name, option_value in instance.as_dict().items():
                if option_name != "name":

                    if name not in parser:
                        parser[name] = {}

                    parser[name][option_name] = option_value

        with open(self.files["instances"], "w", encoding="utf8") as stfile:
            parser.write(stfile)

        # ----------------------------------------------------------------

        return True

    def load(self) -> bool:
        """
        Load settings.

        :rtype: bool
        """

        # Instances settings ---------------------------------------------

        parser = configparser.ConfigParser()
        parser.read(self.files["instances"])

        for instance in parser.sections():
            instance_name = instance

            new_instance = MastodonInstance(
                instance_name,
                None,
                None,
                "private",
                "private",
            )

            for option, value in parser[instance].items():
                if option == "url":
                    new_instance.url = value

                if option == "user":
                    new_instance.usermail = value

                if option == "init_tootv":
                    if value in ["private", "unlisted", "public"]:
                        new_instance.first_tootv = value
                    else:
                        new_instance.first_tootv = "private"

                if option == "tootv":
                    if value in ["private", "unlisted", "public"]:
                        new_instance.other_tootv = value
                    else:
                        new_instance.other_tootv = "private"

            self.instances[instance_name] = new_instance

        # ----------------------------------------------------------------

        return True

    def create(self) -> NoReturn:
        """
        Creates a new settings folder with default datas.
        """
        self.__add_default_instance()
        self.save()

    def __add_default_instance(self) -> NoReturn:
        """
        Add a default and unusable Mastodon instance access.
        """

        self.add_instance(
            name="default",
            url="https://example.com",
            usermail="user@mail.example.com",
            first_tootv="public",
            other_tootv="unlisted",
        )

    def delete_instance(self, instance_name: str) -> NoReturn:
        """
        Delete a Mastodon instance access.
        """

        self.instances.pop(instance_name)

        if not self.instances:
            self.__add_default_instance()

        self.save()

    def has_instance(self, instance_name: str) -> bool:
        """
        Does settings has an instance named `instance_name` ?

        :type instance_name: str
        :param instance_name: Name of the instance to check.
        :rtype: bool
        """

        instance = self.instances.get(instance_name)
        return instance is not None

    def instance_url(self, instance_name: str) -> str:
        """
        Returns the URL of the instance called `instance_name`

        :type instance_name: str
        :param instance_name: Name of the instance.
        :rtype: str
        :returns: Instance's URL
        """
        value = self.instances[instance_name].url
        return value

    def instance_user(self, instance_name: str) -> str:
        """
        Returns the user mail of the instance called `instance_name`

        :type instance_name: str
        :param instance_name: Name of the instance.
        :rtype: str
        :returns: Instance's user mail
        """
        value = self.instances[instance_name].usermail
        return value

    def instance_init_tootv(self, instance_name: str) -> str:
        """
        Returns the visibility of the first toot of a thread posted on the
        instance called `instance_name`

        :type instance_name: str
        :param instance_name: Name of the instance.
        :rtype: str
        :returns: First toot visibility
        """
        value = self.instances[instance_name].first_tootv
        return value

    def instance_tootv(self, instance_name: str) -> str:
        """
        Returns the visibility of the non-first toots of a thread posted on
        the instance called `instance_name`

        :type instance_name: str
        :param instance_name: Name of the instance.
        :rtype: str
        :returns: Non-first toot visibility
        """
        value = self.instances[instance_name].other_tootv
        return value


# vim:set shiftwidth=4 softtabstop=4:
