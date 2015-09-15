import argparse


def build_arg_parser():
    parser = argparse.ArgumentParser(add_help=True, usage='key_manager <command> [<args>]')
    subparsers = parser.add_subparsers()
    # Completed #
    parser_add = subparsers.add_parser('add' ,help='add a new user')
    parser_add.add_argument('user', help='user to add')
    parser_add.add_argument('access', choices=['admin', 'engineer'], help='access level for user')
    # End Complete #
    parser_remove = subparsers.add_parser('remove', help='delete a user')
    parser_remove.add_argument('user', help='user to remove')
    parser_remove.add_argument('env', help='environment to remove access from')
    parser_remove.add_argument('--purge', action='store_true', help='Remove user dir and account from servers')
    parser_remove.add_argument('--force', action='store_true')
    # todo: have a param to allow removal of user account/key or access to a system(prod)
    # Completed #
    parser_temp = subparsers.add_parser('temp', help='grant temp access to a production component')
    parser_temp.add_argument('user', help='user to grant access to')
    parser_temp.add_argument('env', choices=['stg','prod','ops'], help='the environment to grant access to')
    parser_temp.add_argument('--comp', help='the component to grant access to')
    parser_update = subparsers.add_parser('update', help='sync all user accounts for admin and engineering')
    parser_update.add_argument('env', choices=['stg','prod','ops','all'])
    # End Complete #
    parser_list = subparsers.add_parser('list', help='list all users/components')
    parser_list.add_argument('user')
    parser_list.add_argument('comp')
    parser_rekey = subparsers.add_parser('rekey', help='generate a new key for a user')
    parser_rekey.add_argument('user', help='the user to rekey')

    return parser









