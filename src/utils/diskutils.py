# diskutils.py
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
from shard_installer.utils.log import setup_logging
logger=setup_logging()

class DiskUtils:

    @staticmethod
    def mount(
        source: str,
        destination: str,
        bindmount: bool = False,
        options: list = [],
    ):
        if not bindmount and options == []:
            logger.info("mounting "+source+" at "+destination)
            Command.execute_command(command=["mount", source, destination], command_description="Mount "+source+" at "+destination, crash=True)
        elif not bindmount and not options == []:
            logger.info("mounting "+source+" at "+destination+" with options "+" ".join(options))
            command = ["mount", source, destination, "-o"]
            command.extend(options)
            Command.execute_command(command=command, command_description="Mount "+source+" at "+destination+" with options "+" ".join(options), crash=True)
        elif bindmount and options == []:
            logger.info("bind mounting "+source+" to "+destination)
            Command.execute_command(command=["mount", "--bind", source, destination])
        else:
            logger.info("bind mounting "+source+" to "+destination+" with options "+" ".join(options))
            command = ["mount", "--bind", source, destination, "-o"]
            command.extend(options)
            Command.execute_command(command=command, command_description="Bind mount "+source+" at "+destination+" with options "+" ".join(options), crash=True)

    @staticmethod
    def unmount(
        mountpoint: str,
    ):
        Command.execute_command(command=["umount", mountpoint], command_description="Unmount "+mountpoint, crash=True)


    @staticmethod
    def overlay_mount(
        lowerdirs: list,
        upperdir: str,
        destination: str,
        workdir: str,
        options: list = [],
    ):
        command = ["mount", "-t", "overlay", "overlay"]
        if len(options) > 0:
            command.extend(["-o",",".join(options)])
        command.extend(["-o", "lowerdir="+":".join(lowerdirs)+",upperdir="+upperdir+",workdir="+workdir+","+destination])
        Command.execute_command(command=command, command_description="Mount overlay at "+destination, crash=True)

    @staticmethod
    def is_ssd(
        disk: str,
    ):
        output = Command.execute_command(command=["lsblk", "-d", "-o", "rota", disk], command_description="Check if "+disk+" is an SSD")
        output = output[1].split()
        output = [x for x in output if "ROTA" not in x]

        if len(output) > 0:
            if output[0] == "0":
                return True
            else:
                return False
        logger.warn("Could not determine disk type of "+disk+" assuming HDD")
        return False
