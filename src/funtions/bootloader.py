# bootloader.py
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

class Bootloader:

    @staticmethod
    def install_bootloader(
        efidir: str,
    ):
        logger.info("Installing bootloader on efidir "+efidir)
        Command.execute_chroot(
            command=[
                "grub-install",
                "--target=x86_64-efi",
                "--efi-directory="+efidir,
                "--bootloader-id=SHARDS_SYSTEM",

            ],
            command_description="Install grub bootloader",
            crash=True,
        )
        Command.execute_chroot(
            command=[
                "grub-install",
                "--target=x86_64-efi",
                "--efi-directory="+efidir,
                "--bootloader-id=SHARDS_SYSTEM",
                "--removable",
            ],
            command_description="Install grub bootloader as removable",
            crash=True,
        )
        FileUtils.replace_file(
            path="/mnt/etc/default/grub",
            search="quiet",
            replace="quiet init=/init",
        )
        Command.execute_chroot(
            command=[
                "grub-mkconfig",
                "-o",
                "/boot/grub/grub.cfg",
            ],
            command_description="Generate grub config",
            crash=True,
        )
