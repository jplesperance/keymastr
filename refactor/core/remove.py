import subprocess
from refactor.core.config import settings
import sqlite3


class Remove(object):
    machines = []
    conn = None
    def __init__(self):
        self.conn = sqlite3.connect(settings.USER_DB)

    def run(self, args):
        user = args.user
        env = args.env
        if self.check_user_admin(user):
            access = "admin"
        else:
            access = "engineer"
        if args.force is True:
            if args.purge is True:
                proc = subprocess.Popen(["salt -G \'environment:"+env+"\' state.sls users.purge."+access+"."+user], stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
            else:
                proc = subprocess.Popen(["salt -G \'environment:"+env+"\' state.sls users.force."+access+"."+user], stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
        else:
            proc = subprocess.Popen(["salt -G \'environment:"+env+"\' state.sls users.remove."+access+"."+user], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

    def check_user_admin(self, user):
        cur = self.conn.cursor()
        cur.execute('select * from admins where uname="'+ user + '" limit 1')
        exist = cur.fetchone()
        if exist is None:
            return False
        else:
            return True

    def check_user_engineer(self, user, access):
        cur = self.conn.cursor()
        cur.execute('select * from engineers where uname="'+ user + '" limit 1')
        exist = cur.fetchone()
        if exist is None:
            return False
        else:
            return True
