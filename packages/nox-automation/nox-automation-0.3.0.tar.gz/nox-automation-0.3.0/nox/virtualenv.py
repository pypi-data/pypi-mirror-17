# Copyright 2016 Jon Wayne Parrott
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import platform
import shutil

from nox.command import Command
from nox.logger import logger


class VirtualEnv(object):
    """Virtualenv management class."""

    def __init__(self, location, interpreter=None, reuse_existing=False):
        self.location = os.path.abspath(location)
        self.interpreter = interpreter
        self.reuse_existing = reuse_existing
        self._setup_env()

    def _setup_env(self):
        """Sets environment variables to activate the virtualenv for
        subprocesses."""
        self.env = os.environ.copy()
        self.env['PATH'] = ':'.join([self.bin, self.env.get('PATH')])

    def _clean_location(self):
        """Deletes any existing virtualenv"""
        if os.path.exists(self.location):
            if self.reuse_existing:
                return False
            else:
                shutil.rmtree(self.location)

        return True

    @property
    def bin(self):
        """Returns the location of the virtualenv's bin folder."""
        if platform.system() == 'Windows':
            return os.path.join(self.location, 'Scripts')
        else:
            return os.path.join(self.location, 'bin')

    def create(self):
        """Create the virtualenv."""
        if not self._clean_location():
            logger.debug('Re-using existing virtualenv.')
            return False

        cmd = ['virtualenv', self.location]

        if self.interpreter:
            cmd.extend(['-p', self.interpreter])

        self.run(cmd, in_venv=False)

        return True

    def run(self, args, in_venv=True):
        """Runs a command. By default, the command runs within the
        virtualenv."""
        return Command(
            args=args,
            env=self.env if in_venv else None,
            silent=True,
            path=self.bin if in_venv else None).run()

    def install(self, *args):
        self.run(('pip', 'install', '--upgrade') + args)
