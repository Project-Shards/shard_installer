# hostname.py
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

class Hostname:
    @staticmethod
    def set_hostname(hostname: str="projectsharxds"):
        logger.info("Setting hostname to "+hostname)
        FileUtils.write_file("/etc/hostname", hostname)
        FileUtils.write_file("/etc/hosts", """
127.0.0.1        localhost
::1              localhost
        """)
