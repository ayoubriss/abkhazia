# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Schatz, Xuan Nga Cao, Mathieu Bernard
#
# This file is part of abkhazia: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abkhazia is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with abkhazia. If not, see <http://www.gnu.org/licenses/>.
"""This package provides various utilities to abkhazia"""

from .utils import (duplicates, open_utf8, list_directory, merge_dicts,
                    list_files_with_extension, remove, is_empty_file, unique)
from .log2file import get_log
from .config import config, AbkhaziaConfig
from .wav import convert, scan
from .spk2utt import spk2utt

import jobs
import cha
