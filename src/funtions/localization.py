# localization.py
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
from shard_installer.utils.fileutils import FileUtils
from shard_installer.utils.log import setup_logging
logger=setup_logging()

class Localization:

    @staticmethod
    def set_timezone(
        timezone: str,
    ):
        Command.execute_chroot(
            command=[
                "ln",
                "-s",
                "/usr/share/zoneinfo/"+timezone,
                "/etc/localtime"
            ],
            command_description="set timezone to "+timezone,
            crash=False
        )
        Command.execute_chroot(
            command=[
                "hwclock",
                "--systohc"
            ],
            command_description="run hwclock",
            crash=False
        )

    @staticmethod
    def enable_locales(
        locales: list=["en_US.UTF-8"],
        main_locale: str = ""
    ):
        if main_locale.strip() == "":
            main_locale=locales[0].split(":")[0]
        logger.info("Adding locales "+" ".join(locales))
        logger.info("Setting "+main_locale+" main locale")
        locale=""
        for i in locales[0].split(":"): # For some reason click puts the whole args into the first area of a tuple and seperates them with a :
            locale=locale+i+" "+i.split(".")[1]+"\n"
        logger.info(locales)
        FileUtils.append_file(
            path="/etc/locale.gen",
            content=locale
        )
        Command.execute_chroot(
            command=[
                "locale-gen"
            ],
            command_description="Generate locales",
            crash=False
        )
        FileUtils.write_file(
            path="/mnt/etc/locale.conf",
            content="LANG="+main_locale
        )
