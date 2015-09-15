import sys
import re

#from ansible import runner, inventory

from refactor.core.common import Utility
from refactor.core.config import settings


class List(object):
    @staticmethod
    def check_users(args):
        hosts_file = settings.KEY_MANAGER_HOME + "/hosts.txt"
        host_inventory = inventory.Inventory(hosts_file)
        users = []
        Utility.write_heading('Checking users on each machine')
        # Command to list users by checking the passed file and filtering out users
        # who dont have a home directory
        list_users = "awk -F: '$6 ~ /\/home/ {print $1}' /etc/passwd"

        # Check to see if a	particular environment was passed through
        if args.environment == 'prd':
            hosts_pattern = "Production"
        elif args.environment == 'stg':
            hosts_pattern = "Staging"
        else:
            hosts_pattern = "*"

        # Run ansible command to list non-system users
        results = runner.Runner(
            pattern=hosts_pattern, forks=10, inventory=host_inventory,
            module_name='command', module_args=list_users,
        ).run()

        if results is None:
            print("No hosts found")
            sys.exit(1)

        print("*********** UP ***********")
        for (hostname, result) in results['contacted'].items():
            if 'failed' not in result:
                print("##### %s #####\n%s" % (hostname, result['stdout']))
                # users.append(hostname)
                # users[len(users)-1] = re.sub("[^\w]", "\n",  result['stdout']).split()
                users = users + re.sub("[^\w]", "\n", result['stdout']).split()

        print("*********** FAILED *******")
        for (hostname, result) in results['contacted'].items():
            if 'failed' in result:
                print("%s >>> %s" % (hostname, result['msg']))

        print("*********** DOWN *********")
        for (hostname, result) in results['dark'].items():
            print("%s >>> %s" % (hostname, result))

        # Print all unique users on machines checked
        uniq_users = set(users)
        print("\n*********** UNIQUE USERS *********")
        for user in sorted(uniq_users):
            print(user + "\n")

    def run(self, args):
        Utility.write_hosts_file(args)
        self.check_users(args)
