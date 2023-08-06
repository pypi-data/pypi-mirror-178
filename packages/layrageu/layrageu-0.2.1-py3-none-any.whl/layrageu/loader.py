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
Layrageu : FODT → Mastodon toots converter.
"""

# Imports ===============================================================#

# Standard library ------------------------------

from __future__ import annotations

import textwrap

from pathlib import Path
from typing import List, Union, Optional

# Third parties ---------------------------------

import lxml.etree as ET

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

# Layrageu --------------------------------------

from layrageu.fodt2text import FODT_TO_TEXT_XML

# Variables globales 2 / 2 ==============================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

StringOrPath = Union[str, Path]

# Classes ===============================================================#


class Toot:
    """
    Mastodon toot.

    Handles paragraphs and maximum length.
    """

    def __init__(self, paras: Optional[List[Paragraph]] = None):
        self.paras = []

        if paras is not None:
            for para in paras:
                self.paras.append(para)

    def as_markdown(self) -> Markdown:
        """
        Return toot as rich Markdown object.
        """

        paras_md = [para.as_markdown() for para in self.paras]
        source = "\n\n".join(paras_md)

        return Markdown(source)

    def as_html(self) -> str:
        """
        Return toot as HTML string (<p> elements).
        """

        paras_md = [para.as_html() for para in self.paras]
        source = "\n".join(paras_md)

        return source

    def __eq__(self, other):
        if len(self.paras) != len(other.paras):
            return False

        for idx, own_para in enumerate(self.paras):
            if str(own_para) != str(other.paras[idx]):
                return False

        return True

    def add_para(
        self, para: Paragraph, toot_length: int = 500
    ) -> Union[bool, List[Toot]]:
        """
        Add paragraph. Returns a list of toots if the maximum tooth length
        is execeded.

        :type para: Paragraph
        :type toot_length: int
        """

        def create_next_toots(ref_toot, toot_length=500):
            nexts = ref_toot.add_para(para, toot_length)
            return [ref_toot] + nexts

        following_toots = []

        current_length = len(self)

        # This toot length is already maximum toot length. Don't add the
        # paragraph and return the following new toots
        if current_length == toot_length:
            next_toots = create_next_toots(self, toot_length)
            return next_toots

        if current_length < toot_length:
            # Get the length of this toot if we add the full paragraph to
            # it.
            tmp_toot = Toot([para])
            with_full_next_para = current_length + len(tmp_toot)

            # If toot + paragraph >= maximum toot_length
            # => add the paragraph, returns nothing
            if with_full_next_para <= toot_length:
                self.paras.append(para)
                return False

            remaining_length = toot_length - current_length

            if len(para.lines) > 1:
                # The paragraph is too long and has multiple lines ----------

                new_paragraph = Paragraph()
                nexts_line_index = 0

                for idx, line in enumerate(para.lines):

                    remaining_length -= len(new_paragraph)

                    if len(line) <= remaining_length - 2:
                        new_paragraph.lines.append(line)
                        nexts_line_index = idx + 1
                        break

                self.paras.append(new_paragraph)

                next_lines = para.lines[nexts_line_index:]

                if next_lines:
                    new_toot = Toot()
                    merge_paragraph = Paragraph(next_lines)

                    nexts = new_toot.add_para(merge_paragraph, toot_length)

                    following_toots.append(new_toot)

                    if nexts:
                        following_toots += nexts

                    return following_toots

                return False

            # The paragraph is too long and has only one line -----------

            # Split the line nicely

            splited_line = textwrap.wrap(
                # para.lines[0], remaining_length - len("\n\n")
                para.lines[0],
                remaining_length - 2,
                replace_whitespace=False,
            )

            # Add the part of the line that can be merged without
            # exceding maximum toot length
            merge_paragraph = Paragraph([splited_line[0]])
            self.paras.append(merge_paragraph)

            # Create a new paragraph with the remaining part of the line,
            # add it to a new toot and add it to the following toots
            # returned.
            new_paragraph = Paragraph([" ".join(splited_line[1:])])

            new_toot = Toot()
            nexts = new_toot.add_para(new_paragraph, toot_length)

            following_toots.append(new_toot)

            if not nexts:
                return following_toots

            following_toots += nexts

        return following_toots

    def __len__(self) -> int:
        return len(str(self))

    def __str__(self) -> str:
        return "\n\n".join([str(para) for para in self.paras])


class Paragraph:
    """
    Paragraph in a Mastodon toot.
    """

    def __init__(self, lines: Optional[List[str]] = None):
        self.lines = []

        if lines is not None:
            self.lines = lines

    def __repr__(self) -> str:
        return f"{len(self.lines)}|" + "{lb}".join(self.lines)

    def __len__(self) -> int:
        return len(str(self))

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def as_markdown(self) -> str:
        """
        Returns paragraph as a Markdown string.
        Handles line breaks.
        """
        return "\\\n".join(self.lines)

    def as_html(self) -> str:
        """
        Returns paragraph as an HTML paragraph string.
        """
        lines = "<br/>".join(self.lines)
        return f"<p>{lines}</p>"


# Fonctions =============================================================#


def thread_to_toots(
    raw_thread: List[List[str]],
    toot_length=500,
) -> List[Toot]:
    """
    Converts a raw thread into a sequence of Toots.

    :type raw_thread: List[List[str]]
    :type toot_length: int
    :rtype: List[Toot]
    """

    def is_raw_toot_break(data):
        return data == ["--"]

    sequence = []

    for thread_item in raw_thread:

        if not sequence:

            if is_raw_toot_break(thread_item):
                continue

            toot = Toot()
            para = Paragraph(thread_item)

            following_toots = toot.add_para(para, toot_length)

            sequence.append(toot)

            if following_toots:
                for next_toot in following_toots:
                    sequence.append(next_toot)

            continue

        if is_raw_toot_break(thread_item):
            toot = Toot()
            sequence.append(toot)

            continue

        para = Paragraph(thread_item)
        following_toots = sequence[-1].add_para(para, toot_length)

        if following_toots:
            for next_toot in following_toots:
                sequence.append(next_toot)

    return sequence


def raw_thread(thread_input: str) -> List[List[str]]:
    """
    Converts raw text document into a list of elements.

    - Paragraphs are transformed into a List[str].
    - Toots breaks (`--` paragraph) become ["--"]

    :rtype: List[List[str]]
    """
    # First, spliting paragraphs

    thread_input = thread_input.split("\n")

    paras = []

    for text in thread_input:
        # No line break in that paragraph

        if "{lb}" not in text:
            paras.append([text])
            continue

        # Line break found in that paragraph

        text = text.replace("{lb}", "\n")
        paras += [[part for part in text.split("\n") if part != [""]]]

    # At this point the thread is a List[List[str]], strings are joined with
    # line breaks.

    return [part for part in paras if part != [""]]


def load_fodt_converter() -> ET.XSLT:
    """
    Returns Layrageu FODT ⇒ text XSLT converter.
    """

    # stylesheet_path = Path(__file__).resolve(True).parent
    # stylesheet_path = stylesheet_path / "fodt2text.xsl"

    return ET.XSLT(ET.fromstring(FODT_TO_TEXT_XML))


def convert(document_path: StringOrPath, debug: bool = False) -> List[Toot]:
    if debug:
        console = Console()

    # Get document path ----------------------------------------

    if isinstance(document_path, str):
        document_path = Path(document_path)

    document_path = str(document_path.resolve(True))

    # Parse and convert document -------------------------------

    document = ET.parse(document_path)
    converter = load_fodt_converter()
    thread_input = str(converter(document)).rstrip()

    if debug:
        console.print(Panel(thread_input, title="XSLT output"))

    # Transforms document into individual toots ----------------

    splitted = raw_thread(thread_input)

    sequence = unduplicate(thread_to_toots(splitted))

    if debug:
        console.print(
            Panel(
                "\n\n".join(
                    [
                        f"SEQUENCE ITEM {idx} | {len(element)}\n{element}"
                        for idx, element in enumerate(sequence)
                    ]
                ),
                title="Toot sequence",
            )
        )

    # ----------------------------------------------------------

    return sequence


def unduplicate(sequence: List[Toot]) -> List[Toot]:
    """
    Remove possible duplicates in `sequence`.
    """

    new_sequence = []

    for item in sequence:
        add = True

        for old_item in new_sequence:
            if item == old_item:
                add = False
                break

        if add:
            new_sequence.append(item)

    return new_sequence


# vim:set shiftwidth=4 softtabstop=4:
