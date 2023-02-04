# shards.py
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
import logging

class Shards:

    @staticmethod
    def setupRoot(
        mountpoint: str,
        disks: list,
    ):
        Command.execute(command=["pacstrap", "-K", "base"], command_description="Setup base package on Root", crash=True)
        FileUtils.create_file("/mnt/init")
        FileUtils.write_file("/mnt/init", "#!/bin/bash")
        init = '''
        echo -e "\\x1b[35;1m --STARTING PROJECT SHARD STAGE 1-- \\x1b[39m"
        echo "Mounting Shards"
        mount {partition2} /Shards/Data -t btrfs -o rw,{ssd},relatime,space_cache=v2,compress,subvol=/Data
        mount {partition2} /Shards/Desktop -t btrfs -o ro,{ssd},relatime,space_cache=v2,compress,subvol=/Desktop
        mount {partition2} /Shards/System -t btrfs -o ro,{ssd},relatime,space_cache=v2,compress,subvol=/System
        mount {partition2} /Shards/Users -t btrfs -o rw,{ssd},relatime,space_cache=v2,compress,subvol=/Users
        echo "Creating overlays"
        mount -t overlay overlay -o lowerdir=/Shards/System/opt:/Shards/Desktop/opt,upperdir=/Shards/Data/opt,workdir=/Shards/Data/tmp/opt /opt
        mount -t overlay overlay -o lowerdir=/Shards/System/usr:/Shards/Desktop/usr,upperdir=/Shards/Data/usr,workdir=/Shards/Data/tmp/usr /usr
        mount -t overlay overlay -o lowerdir=/Shards/System/var:/Shards/Desktop/var,upperdir=/Shards/Data/var,workdir=/Shards/Data/tmp/var /var
        mount -t overlay overlay -o lowerdir=/Shards/System/etc:/Shards/Desktop/etc,upperdir=/Shards/Data/etc,workdir=/Shards/Data/tmp/etc /etc
        echo "Mounting bind mounts"
        mount --bind /Shards/System/boot /boot
        mount --bind /Shards/Users /home
        echo -e "\\x1b[35;1m --STARTING PROJECT SHARD STAGE 2-- \\x1b[39m"
        exec /Shards/System/sbin/init
        '''.format(partition2=disks[1], ssd="ssd" if )


        # System shard packages:
        # base linux linux-firmware intel-ucode networkmanager grub
        # base shard packages:
        # base
