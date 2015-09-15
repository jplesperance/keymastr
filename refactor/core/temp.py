import os


class Temp(object):

    @staticmethod
    def run(args):
        env = args.env
        user = args.user
        component = args.comp


        if not os.path.isfile('/srv/salt/keys/user/' + user):
            print("User does not exist and must be added first!")
            quit()
        if not component or component == None:
            if not os.path.isfile('/srv/salt/users/add/admin/' + user+'.sls'):
                print('A component must be specified for all non-admin users!')
                quit()
            else:
                os.system('salt -G \'environment:'+env+'\' state.sls users/add/admin/' + user)

        else:
            os.system('salt -C \'G@component:' + component + '  and G@environment:'+env+'\' state.sls users/add/engineer/' + user)


