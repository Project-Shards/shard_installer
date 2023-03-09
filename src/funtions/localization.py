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
        locales: list=["en_US.UTF-8"]
        main_locale: str=""
    ):
        if main_locale.strip() == "":
            main_locale=locales[0]
        logging.info("Adding locales "+" ".join(locales))
        logging.info("Setting "+main_locale+" main locale")
        for i in range(0, len(locales)):
            locales[i] = locales[i]+" "+locales[i].split(":")[1]
        FileUtils.append_file(
            path="/etc/locale.gen",
            content="\n".join(locales)
        )
        Command.execute_chroot(
            command=[
                "locale-gen"
            ],
            command_description="Generate locales",
            crash=False
        )
        FileUtis.write_file(
            path="/mnt/etc/locale.conf",
            content="LANG="+main_locale
        )
