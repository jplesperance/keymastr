#!/usr/bin/env python

from os.path import abspath, dirname, join, realpath

import sys
from refactor.core import cli
from refactor.core.add import Add
from refactor.core.remove import Remove
from refactor.core.list import List
from refactor.core.temp import Temp
from refactor.core.update import Update
from refactor.core.rekey import Rekey
from refactor.core import config


def _load_settings():
    app_home = abspath(realpath(dirname(__file__)))
    settings_file = join(app_home, 'settings', 'settings.yml')
    config.load_yaml(settings_file)
    setattr(config.settings, 'KEY_MANAGER_HOME', app_home)
    user_db = join(app_home, 'db', 'users.db')
    setattr(config.settings, 'USER_DB', user_db)
    salt_home = abspath(realpath(dirname(__file__)+'../../salt'))
    setattr(config.settings, 'SALT_HOME', salt_home)


def main():
    _load_settings()
    parser = cli.build_arg_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    args.action = sys.argv[1]
    if args.action == 'add':
        km = Add()
    elif args.action == 'remove':
        km = Remove()
    elif args.action == 'list':
        km = List()
    elif args.action == 'temp':
        km = Temp()
    elif args.action == 'rekey':
        km = Rekey()
    elif args.action == 'update':
        km = Update()
    else:
        raise Exception
    km.run(args)


if __name__ == '__main__':
    main()