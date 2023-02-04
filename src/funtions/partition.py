# partition.py
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
from shard_installer.utils.diskutils import DiskUtils
import logging

partitions=[]

def start_partition(str: disk):
    partition_disk(disk)
    if "nvme" in disk:
        partitions=[disk+"p1", disk+"p2"]
        partition_nvme(disk)
    else:
        partitions=[disk+"1", disk+"2"]
        partition_disk(disk)

def partition_disk(str: disk):
    logging.debug("Using "+disk)
    Command.execute_command(command=["parted", "-s", disk, "mklabel", "gpt"], command_description="Create gpg label on "+disk, crash=True)
    Command.execute_command(command=["parted", "-s", disk, "mkpart", "fat32", "0", "512M"], command_description="Create fat32 EFI partition on "+disk, crash=True)
    Command.execute_command(command=["parted", "-s", disk, "mkpart", "btrfs", "512M", "100%"], command_description="Create Shard Linux Root partition on "+disk, crash=True)

def part_nvme(str: disk):
    logging.debug("Partitioning "+disk+" as nvme device")
    Command.execute_command(command=["mkfs.vfat", "-F32", partitions[0]], command_description="Format "+partitions[0]+" as fat32", crash=True)
    Command.execute_command(command=["mkfs.btrfs", "-f", partitions[1]], command_description="Format "+partitions[1]+" as btrfs", crash=True)
    setup_volumes(disk=disk)

def part_disk(str: disk):
    logging.debug("Partitioning "+disk+" as non nvme block device")
    Command.execute_command(command=["mkfs.vfat", "-F32", partitions[0]], command_description="Format "+partitions[0]+" as fat32", crash=True)
    Command.execute_command(command=["mkfs.btrfs", "-f", partitions[1]], command_description="Format "+partitions[1]+" as btrfs", crash=True)
    setup_volumes(disk=disk)


def setup_volumes(str: disk):
    logging.debug("Setting up shards on"+disk)
    DiskUtils.mount(source=partitions[1], destination="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "Root"], command_description="Create Root shard", crash=True, workdir="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "System"], command_description="Create System shard", crash=True, workdir="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "Data"], command_description="Create Data shard", crash=True, workdir="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "Recovery"], command_description="Create Recovery shard", crash=True, workdir="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "Desktop"], command_description="Create Desktop shard", crash=True, workdir="/mnt")
    Command.execute_command(command=["btrfs", "subvol", "create", "Users"], command_description="Create Users shard", crash=True, workdir="/mnt")
    DiskUtils.unmount("/mnt")
    DiskUtils.mount(source=partitions[1], destination="/mnt", options="subvol=Root")
    logging.debug("Installing base Root shard")
