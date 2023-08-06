# Copyright (c) 2016 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pkgutil

from os.path import expanduser, join


__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
antlr_default_path = join(expanduser('~'), '.generinator_rats', 'antlr4.jar')
