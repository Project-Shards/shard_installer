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
from shard_installer.functions.partition import Partition
import logging
import logging.config
import yaml

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)
logger=logging.getLogger("shard_logging")

@click.group()
@click.option('--verbose', is_flag=True, help='Enables verbose mode.', default=False)
def main(verbose):
    """This statement prints Hello, World to your console"""
    #click.echo("Hello, World")
    click.echo("Verbose mode is %s" % ('on' if verbose else 'off'))
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

@main.command()
@click.option('--disk', prompt='Disk to partition', help='Disk to partition')
def partition(disk):
    """This statement prints Hello, World to your console"""
    click.echo(disk)
    logger.info("Partitioning disk %s" % disk)
    partition=Partition(disk)
    partition.start_partition()
