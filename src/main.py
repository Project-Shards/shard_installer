# main.py
#
# Copyright 2023 axtlos <axtlos@tar.black>
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

import click
from shard_installer.functions.localization import Localization
from shard_installer.functions.partition import Partition
from shard_installer.functions.user import User
from shard_installer.functions.shards import Shards
from shard_installer.functions.bootloader import Bootloader
from shard_installer.functions.hostname import Hostname
from shard_installer.utils.log import setup_logging
logger=setup_logging()


@click.group()
@click.option('--verbose', is_flag=True, help='Enables verbose mode.', default=False)
def main(verbose):
    click.echo("Verbose mode is %s" % ('on' if verbose else 'off'))
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

@main.command()
@click.option('--disk', prompt='Disk to partition', help='Disk to partition')
def install(disk):
    """Install Project Shards, includes partitioning"""
    click.echo(disk)
    logger.info("Partitioning disk %s" % disk)
    partition=Partition(disk)
    partition.start_partition()
    Shards.install_shards(partition)

@main.command()
@click.option('--efidir', help='EFI directory in installation', default="/boot/efi")
def bootloader(efidir):
    """Install bootloader"""
    logger.info("Installing bootloader")
    Bootloader.install_bootloader(efidir)

@main.command()
@click.option('--username', prompt='Username', help='Username of the new user')
@click.option('--password', prompt='Password', help='Password of the new user', hide_input=True, confirmation_prompt=True)
@click.option('--sudoer', is_flag=True, help='Make the user a sudoer')
def addUser(username, password, sudoer):
    """Add a new user"""
    logger.info("Creating user "+username)
    logger.info(username+" is sudoer" if username else "is not sudoer")
    User.create_user(
        username=username,
        password=password,
        hasWheel=sudoer
    )

@main.command()
@click.option('--password', prompt='Password', help='Password of the root user', hide_input=True, confirmation_prompt=True)
def setRootPass(password):
    """Set the root password"""
    logger.info("Setting root password")
    User.set_root_password(
        password=password
    )

@main.command()
@click.option('--locales', help='Locales to enable sepearted with \':\'', multiple=True, default=["en_US.UTF-8"])
@click.option('--mainLocale', help='Main locale', required=False, default="")
def setLocales(locales, mainlocale):
    """Set the locales"""
    Localization.enable_locales(
        locales=locales,
        main_locale=mainlocale
    )

@main.command()
@click.option('--timezone', prompt=True, help='Timezone to use')
def setTimezone(timezone):
    """Set the timezone"""
    Localization.set_timezone(
        timezone=timezone
    )

@main.command()
@click.option('--hostname', prompt=True, help='Hostname to use', default="projectshards")
def setHostname(hostname):
    """Set the hostname"""
    Hostname.set_hostname(
        hostname=hostname
    )
