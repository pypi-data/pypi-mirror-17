# -*- coding: utf-8 -*-
#
# This file was part of lago project.
# This file was part of INSPIRE-SCHEMAS.
# This file is part of autosemver.
# Copyright (C) 2016 CERN.
#
# autosemver is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# autosemver is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autosemver; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import copy
import os
import sys

import argparse

from autosemver.api import (
    get_authors,
    get_changelog,
    get_current_version,
    get_releasenotes,
)
from .packaging import (
    get_current_version as pkg_version,
)

PROJECT_NAME = 'python-autosemver'
__version__ = pkg_version(
    project_name=PROJECT_NAME,
    project_dir=os.path.dirname(__file__),
    repo_dir=os.path.join(os.path.dirname(__file__), '..'),
)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'repo_path', help='Git repo to generate the changelog for'
    )
    subparsers = parser.add_subparsers()
    changelog_parser = subparsers.add_parser('changelog')
    changelog_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the changelog from'
    )
    changelog_parser.set_defaults(func=get_changelog)
    version_parser = subparsers.add_parser('version')
    version_parser.set_defaults(func=get_current_version)
    releasenotes_parser = subparsers.add_parser('releasenotes')
    releasenotes_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the release notes from'
    )
    releasenotes_parser.set_defaults(func=get_releasenotes)
    authors_parser = subparsers.add_parser('authors')
    authors_parser.add_argument(
        '--from-commit',
        default=None,
        help='Commit to start the authors from'
    )
    authors_parser.set_defaults(func=get_authors)
    args = parser.parse_args(args)

    params = copy.deepcopy(vars(args))
    params.pop('func')

    return args.func(**params)
