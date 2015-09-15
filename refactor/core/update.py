import subprocess
import json

class Update(object):

    @staticmethod
    def run(args):
        if args.env == 'prod':
            proc = subprocess.Popen(["salt --out=json -G \'environment:prod\' state.sls users.admins"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

        elif args.env == 'ops':
            proc = subprocess.Popen(["salt --out=json -G \'environment:ops\' state.sls users.admins"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

        elif args.env == 'stg':
            proc = subprocess.Popen(["salt -G \'environment:stg\' state.sls users.engineers"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

        elif args.env == 'all':
            proc = subprocess.Popen(["salt -C \'G@environment:prod and G@environment:ops\' state.sls users.admins"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

            proc = subprocess.Popen(["salt -G \'environment:stg\' state.sls users.engineers"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

