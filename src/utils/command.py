# command.py
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

import subprocess
import os
import logging
import logging.config
import yaml

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)
logger=logging.getLogger("shard_logging")

class Command:
    @staticmethod
    def execute_command(
        command: list,
        command_description: str = "",
        crash: bool = False,
        workdir: str = "",
    ) -> [str, str, str]:
        if os.environ.get("DEBUG") == "true":
            logger.debug("Command: " + " ".join(command))
            return [0, "", ""]

        out = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            cwd=workdir if workdir.strip() != "" else None
        )
        if out.returncode != 0 and command_description.strip() != "":
            logger.error(command_description+" failed with returncode "+out.returncode)
            if crash:
                return out.returncode
        elif out.returncode != 0:
            logger.error(command+" failed with returncode "+out.returncode)
            if crash:
                return out.returncode

        return [out.returncode, out.stdout, out.stderr]
