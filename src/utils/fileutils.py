# fileutils.py
#
# Copyright 2023 axtlos <axtlos@getcryst.al>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0

from shard_installer.utils.command import Command
from os.path import exists
import os.makedirs
import logging

class FileUtils:

    @staticmethod
    def create_file(
        path: str,
    ):
        file = open(path, 'x')
        file.close()

    @staticmethod
    def append_file(
        path: str,
        content: str,
    ):
        if not exists(path):
            logging.warn("File "+path+" doesn't exist! Creating file")
            create_file(path)
        with open(path, 'a') as file:
            file.write(content)

    @staticmethod
    def write_file(
        path: str,
        content: str,
    ):
        if not exists(path):
            logging.warn("File "+path+" doesn't exist! Creatin file")
            create_file(path)
        with open(path, 'w') as file:
            file.write(content)

    @staticmethod
    def create_directory(
        path: str,
    ):
        if not exists(path):
            os.makedirs(path)
        else:
            logging.warn("Directory "+path+" already exists!")
