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
from shard_installer.utils.diskutils import DiskUtils
from shard_installer.functions.user import User
from shard_installer.functions.partition import Partition
from shard_installer.utils.log import setup_logging
logger=setup_logging()

class Shards:
    @staticmethod
    def install_shards(partition: Partition):
        partitions=partition.partitions

        logger.debug("Installing Recovery")
        Shards.setupRecovery(mountpoint="/mnt", disks=partitions, crash=True)

        logger.debug("Installing base Root shard")
        Shards.setupRoot(mountpoint="/mnt", disks=partitions, crash=True)

        logger.debug("Installing Data shard")
        Shards.setupData(mountpoint="/mnt/Shards/Data", crash=True)

        logger.debug("Installing System shard")
        Shards.setupSystem(mountpoint="/mnt/Shards/System", disks=partitions, crash=True)

        logger.debug("Installing Desktop shard")
        Shards.setupDesktop(mountpoint="/mnt", disk=partitions, crash=True)



    @staticmethod
    def setupRoot(
        mountpoint: str,
        disks: list,
        crash: bool = True,
    ):
        def pre_install():
            DiskUtils.mount(source=disks[1], destination="/mnt", options=["subvol=Root"], crash=crash)

        def install():
            Command.execute_command(command=["pacstrap", "-K", mountpoint, "base"], command_description="Setup base package on Root", crash=crash)
            FileUtils.create_file("/mnt/init")
            FileUtils.write_file("/mnt/init", "#!/bin/bash")
            init = '''
echo -e "\\x1b[35;1m --STARTING PROJECT SHARD STAGE 1-- \\x1b[39m"
echo "Mounting Shards"
mount {partition2} /Shards/Data -t btrfs -o rw{ssd},relatime,space_cache=v2,compress,subvol=/Data
mount {partition2} /Shards/Desktop -t btrfs -o ro{ssd},relatime,space_cache=v2,compress,subvol=/Desktop
mount {partition2} /Shards/System -t btrfs -o ro{ssd},relatime,space_cache=v2,compress,subvol=/System
mount {partition2} /Shards/Users -t btrfs -o rw{ssd},relatime,space_cache=v2,compress,subvol=/Users
echo "Creating overlays"
mount -t overlay overlay -o lowerdir=/Shards/System/opt:/Shards/Desktop/opt,upperdir=/Shards/Data/opt,workdir=/Shards/Data/tmp/opt /opt
mount -t overlay overlay -o lowerdir=/Shards/System/usr:/Shards/Desktop/usr,upperdir=/Shards/Data/usr,workdir=/Shards/Data/tmp/usr /usr
mount -t overlay overlay -o lowerdir=/Shards/System/var:/Shards/Desktop/var,upperdir=/Shards/Data/var,workdir=/Shards/Data/tmp/var /var
echo "Mounting bind mounts"
mount --bind /Shards/System/boot /boot
mount --bind /Shards/Users /home
mount --bind /Shards/Data/etc /etc
echo -e "\\x1b[35;1m --STARTING PROJECT SHARD STAGE 2-- \\x1b[39m"
exec /Shards/System/sbin/init
            '''.format(partition2=disks[1], ssd=",ssd" if DiskUtils.is_ssd(disks[0]) else "")
            FileUtils.append_file("/mnt/init", init)
            Command.execute_command(command=["chmod", "+x", "/mnt/init"], command_description="Making init executable", crash=crash)

        def post_install():
            logger.debug("Mounting Shards")
            FileUtils.create_directory("/mnt/Shards")
            FileUtils.create_directory("/mnt/Shards/Users")
            FileUtils.create_directory("/mnt/Shards/System")
            FileUtils.create_directory("/mnt/Shards/Data")
            FileUtils.create_directory("/mnt/Shards/Recovery")
            FileUtils.create_directory("/mnt/Shards/System")
            DiskUtils.mount(source=disks[1], destination="/mnt/Shards/Users", options=["subvol=Users"], crash=crash)
            DiskUtils.mount(source=disks[1], destination="/mnt/Shards/System", options=["subvol=System"], crash=crash)
            DiskUtils.mount(source=disks[1], destination="/mnt/Shards/Data", options=["subvol=Data"], crash=crash)
            DiskUtils.mount(source=disks[1], destination="/mnt/Shards/Desktop", options=["subvol=Desktop"], crash=crash)
            DiskUtils.mount(source=disks[1], destination="/mnt/Shards/Recovery", options=["subvol=Recovery"], crash=crash)

        pre_install()
        install()
        post_install()

    @staticmethod
    def setupRecovery(
        mountpoint: str,
        disks: list,
        crash: bool = True,
    ):
        def pre_install():
            DiskUtils.mount(source=disks[1], destination="/mnt", options=["subvol=Recovery"], crash=crash)
            FileUtils.create_directory("/mnt/boot/efi")
            DiskUtils.mount(source=disks[0], destination="/mnt/boot/efi", crash=crash)

        def install():
            Command.execute_command(
                command=[
                    "pacstrap",
                    "-K",
                    mountpoint,
                    "linux",
                    "linux-firmware",
                    "networkmanager",
                    "btrfs-progs",
                    "grub",
                    "efibootmgr",
                    "systemd-sysvcompat",
                    "man-db",
                    "man-pages",
                    "texinfo",
                    "nano",
                    "sudo",
                    "curl",
                    "archlinux-keyring",
                    "which",
                    "base-devel",
                    "bash-completion",
                    "zsh-completions",
                    "gparted",
                    "ntfs-3g",
                    "dosfstools",
                    "exfat-utils",
                    "openssh"
                ],
                command_description="Install packages for recovery shard",
                crash=crash,
            )
            Command.execute_command(command=["genfstab", "-U", mountpoint, ">>", "/mnt/etc/fstab"], command_description="Generate fstab", crash=crash)
            Command.execute_command(command=["arch-chroot", mountpoint, "systemctl", "enable", "NetworkManager"], command_description="Enable NetworkManager", crash=crash)
            Command.execute_command(command=["arch-chroot", mountpoint, "systemctl", "enable", "sshd"], command_description="Enable sshd", crash=crash)
            User.create_user(password="recovery", username="recovery", hasWheel=True)
            User.set_root_password(password="recovery")
            Command.execute_chroot(
                command=[
                    "grub-install",
                    "--target=x86_64-efi",
                    "--efi-directory=/boot/efi",
                    "--bootloader-id=SHARDS_RECOVERY",

                ],
                command_description="Install grub bootloader",
                crash=crash,
            )
            Command.execute_chroot(
                command=[
                    "grub-install",
                    "--target=x86_64-efi",
                    "--efi-directory=/boot/efi",
                    "--bootloader-id=SHARDS_RECOVERY",
                    "--removable",
                ],
                command_description="Install grub bootloader as removable",
                crash=crash,
            )
            Command.execute_chroot(
                command=[
                    "grub-mkconfig",
                    "-o",
                    "/boot/grub/grub.cfg",
                ],
                command_description="Generate grub config",
                crash=crash,
            )
        def post_install():
            DiskUtils.unmount("/mnt/boot/efi", crash=crash)
            DiskUtils.unmount("/mnt", crash=crash)

        pre_install()
        install()
        post_install()

    @staticmethod
    def setupSystem(
        mountpoint: str,
        crash: bool = True,
    ):
        def pre_install():
            logger.debug("Mounting Data etc at System etc")
            FileUtils.create_directory("/mnt/Shards/System/etc")
            DiskUtils.mount(source="/mnt/Shards/Data/etc", destination="/mnt/Shards/System/etc", bindmount=True, crash=crash)

        def install():
            Command.execute_command(
                command=[
                    "pacstrap",
                    "-K",
                    mountpoint,
                    "base",
                    "linux",
                    "linux-firmware",
                    "networkmanager",
                    "btrfs-progs",
                    "grub",
                    "efibootmgr",
                    "systemd-sysvcompat",
                    "man-db",
                    "man-pages",
                    "texinfo",
                    "nano",
                    "sudo",
                    "curl",
                    "archlinux-keyring",
                    "which",
                    "base-devel",
                    "bash-completion",
                    "zsh-completions",
                    "bluez",
                    "podman",
                ],
                command_description="Setup install packages on System",
                crash=crash,
            )

            Command.execute_chroot(
                command=[
                    "systemctl",
                    "enable",
                    "NetworkManager",
                ],
                command_description="Enable NetworkManager",
                crash=False,
            )

            Command.execute_chroot(
                command=[
                    "systemctl",
                    "enable",
                    "bluetooth",
                ],
                command_description="Enable bluetooth",
                crash=False,
            )
            FileUtils.replace_file(
                file="/etc/mkinitcpio.conf",
                search="MODULES=()",
                replace="MODULES=(overlay)",
                crash=crash
            )

        def post_install():
            logger.debug("Unmounting Data etc from System etc")
            DiskUtils.unmount("/mnt/Shards/System/etc")

        pre_install()
        install()
        post_install()

    @staticmethod
    def setupDesktop(
        mountpoint: str,
        disks: str,
        crash: bool = True,
    ):
        def pre_install(self):
            logger.debug("Creating Overlay mount for System and Desktop")
            FileUtils.create_directory("/mnt/Shards/Desktop/usr")
            FileUtils.create_directory("/mnt/Shards/Desktop/var")
            FileUtils.create_directory("/mnt/Shards/Desktop/opt")
            FileUtils.create_directory("/mnt/Shards/Desktop/tmp")
            FileUtils.create_directory("/mnt/Shards/Desktop/tmp/usr")
            FileUtils.create_directory("/mnt/Shards/Desktop/tmp/var")
            FileUtils.create_directory("/mnt/Shards/Desktop/tmp/opt")
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/usr"], upperdir="/mnt/Shards/Desktop/usr", destination="/mnt/usr", workdir="/mnt/Shards/Desktop/tmp/usr", crash=crash)
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/var"], upperdir="/mnt/Shards/Desktop/var", destination="/mnt/var", workdir="/mnt/Shards/Desktop/tmp/var", crash=crash)
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/opt"], upperdir="/mnt/Shards/Desktop/opt", destination="/mnt/opt", workdir="/mnt/Shards/Desktop/tmp/opt", crash=crash)

            logger.debug("Mounting Data etc to root etc")
            DiskUtils.mount(source="/mnt/Shards/Data/etc", destination="/mnt/etc", bindmount=True, crash=crash)

            logger.debug("Mounting System boot to root boot")
            DiskUtils.mount(source="/mnt/Shards/System/boot", destination="/mnt/boot", bindmount=True, crash=crash)

            logger.debug("Mount efi partition to root")
            FileUtils.create_directory("/mnt/boot/efi")
            DiskUtils.mount(source=disks[0], destination="/mnt/boot/efi", crash=crash)

        def install():
            Command.execute_command(
                command=[
                    "pacstrap",
                    "-K",
                    mountpoint,
                    "xorg",
                    "gnome",
                    "sushi",
                    "pipewire",
                    "pipewire-pulse",
                    "pipewire-alsa",
                    "pipewire-jack",
                    "wireplumber",
                    "noto-fonts",
                    "noto-fonts-cjk",
                    "noto-fonts-emoji",
                    "noto-fonts-extra",
                    "ttf-nerd-fonts-symbols-common",
                    "power-profiles-daemon",
                    "cups",
                    "cups-pdf",

                ],
            )
            Command.execute_chroot(
                command=[
                    "systemctl",
                    "enable",
                    "gdm",
                ],
                crash=False
            )

        def post_install():
            logger.debug("Unmounting overlays")
            DiskUtils.unmount(mountpoint="/mnt/usr", crash=crash)
            DiskUtils.unmount(mountpoint="/mnt/var", crash=crash)
            DiskUtils.unmount(mountpoint="/mnt/opt", crash=crash)
            logger.debug("Creating Overlay mounts with System, Desktop and Data")
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/usr", "/mnt/Shards/Desktop/usr"], upperdir="/mnt/Shards/Data/usr", destination="/mnt/usr", workdir="/mnt/Shards/Data/tmp/usr", crash=crash)
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/var", "/mnt/Shards/Desktop/var"], upperdir="/mnt/Shards/Data/var", destination="/mnt/var", workdir="/mnt/Shards/Data/tmp/var", crash=crash)
            DiskUtils.overlay_mount(lowerdirs=["/mnt/Shards/System/opt", "/mnt/Shards/Desktop/opt"], upperdir="/mnt/Shards/Data/opt", destination="/mnt/opt", workdir="/mnt/Shards/Data/tmp/opt", crash=crash)
            DiskUtils.mount(source="/mnt/Shards/Users", destination="/mnt/home", bindmount=True, crash=crash)

        pre_install()
        install()
        post_install()

    @staticmethod
    def setupData(
        mountpoint: str,
        crash: bool = True,
    ):
        def pre_install():
            pass

        def install():
            FileUtils.create_directory(mountpoint + "/etc")
            FileUtils.create_directory(mountpoint + "/opt")
            FileUtils.create_directory(mountpoint + "/usr")
            FileUtils.create_directory(mountpoint + "/var")
            FileUtils.create_directory(mountpoint + "/tmp")
            FileUtils.create_directory(mountpoint + "/tmp/opt")
            FileUtils.create_directory(mountpoint + "/tmp/usr")
            FileUtils.create_directory(mountpoint + "/tmp/var")

        def post_install():
            pass

        install()
        post_install()
        # System shard packages:
        # base linux linux-firmware intel-ucode networkmanager grub
        # base shard packages:
        # base
