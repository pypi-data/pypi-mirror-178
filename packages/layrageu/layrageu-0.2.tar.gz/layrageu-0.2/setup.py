#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

VERSION = "0.2"
DESCRIPTION = "Send Mastodon threads from Flat OpenDocument files."

REQUIRED = [
    "lxml",
    "rich",
    "docopt",
    "appdirs",
    "slugify",
    "iso639-lang",
    "Mastodon.py",
    "ttkSimpleDialog",
]

setuptools.setup(
    name="layrageu",
    version=VERSION,
    author="Étienne Nadji",
    author_email="etnadji@eml.cc",
    description=DESCRIPTION,
    long_description=long_description,
    packages=setuptools.find_packages(),
    platforms="any",
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    classifiers=[
        "Topic :: Communications",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: XML",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    project_urls={
        "Source Code": "https://framagit.org/etnadji/layrageu",
        "Issue tracker": "https://framagit.org/etnadji/layrageu/-/issues",
        "Documentation": "https://etnadji.fr/rsc/layrageu/doc",
    },
    entry_points={
        "console_scripts": [
            "layrageu=layrageu.tui:main",
            "layrageu-gui=layrageu.gui:main",
        ]
    },
    python_requires=">=3.8",
    install_requires=REQUIRED,
    keywords=["Mastodon", "LibreOffice", "OpenDocument"],
)

# vim:set shiftwidth=4 softtabstop=4 spl=en:
