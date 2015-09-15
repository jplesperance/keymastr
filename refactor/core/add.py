import sqlite3
import random
import os
import jinja2

from refactor.core.config import settings


class Add(object):
    machines = []
    conn = None
    templateEnv = None
    addTemplate = 'add.jinja'
    removeTemplate = 'remove.jinja'
    forceTemplate = 'force.jinja'
    purgeTemplate = 'purge.jinja'
    adminTemplate = 'admin.jinja'
    engineerTemplate = 'engineer.jinja'


    def __init__(self):
        self.conn = sqlite3.connect(settings.USER_DB)
        templateLoader = jinja2.FileSystemLoader(searchpath=settings.KEY_MANAGER_HOME + '/templates/')
        self.templateEnv = jinja2.Environment(loader=templateLoader)

    def run(self, args):
        if self.check_user(args.user, args.access) is True:
            print("The user already exists")
            return
        password = self.generate_key_pass()
        self.generate_key(args.user, args.access, password)
        self.add_user(args.user, args.access, password)
        self.create_state_files(args.user, args.access)
        self.add_to_group_state(args.access)
        return

    def check_user(self, user, access):
        cur = self.conn.cursor()
        cur.execute('select * from ' + access + 's where uname="'+ user + '" limit 1')
        exist = cur.fetchone()
        if exist is None:
            return False
        else:
            return True

    def generate_key(self, user, access, password):
        os.system("/usr/bin/ssh-keygen -f /srv/salt/keys/user/"+user+" -b 4096 -N '"+password+"'")

    def add_user(self, user, access, password):
        cur = self.conn.cursor()
        cur.execute("insert INTO " + access + "s (uname, active, password) VALUES('"+ user + "', 1, '"+password+"')")
        self.conn.commit()
        return

    def generate_key_pass(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        pw_length = 12
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]

        # replace 1 or 2 characters with a number
        for i in range(random.randrange(1,3)):
            replace_index = random.randrange(len(mypw)//2)
            mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index+1:]

        # replace 1 or 2 letters with an uppercase letter
        for i in range(random.randrange(1,3)):
            replace_index = random.randrange(len(mypw)//2,len(mypw))
            mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index+1:]
        return mypw

    def create_state_files(self, user, access):
        add_template = self.templateEnv.get_template(self.addTemplate)
        remove_template = self.templateEnv.get_template(self.removeTemplate)
        force_template = self.templateEnv.get_template(self.forceTemplate)
        purge_template = self.templateEnv.get_template(self.purgeTemplate)
        cur = self.conn.cursor()
        cur.execute("select * from "+access+"s where uname='"+user+"' limit 1")
        userData = cur.fetchone()
        uid = self.get_uid(userData[0])
        userInfo = { "user": user, "uid":uid, "gid":uid}
        addstatefile = add_template.render(userInfo)
        removestatefile = remove_template.render(userInfo)
        forcestatefile = force_template.render(userInfo)
        purgestatefile = purge_template.render(userInfo)
        with open('/srv/salt/users/add/'+access+'/'+user+'.sls', 'w') as fh:
            fh.write(addstatefile)
        with open('/srv/salt/users/remove/'+access+'/'+user+'.sls', 'w') as fh:
            fh.write(removestatefile)
        with open('/srv/salt/users/force/'+access+'/'+user+'.sls', 'w') as fh:
            fh.write(forcestatefile)
        with open('/srv/salt/users/purge/'+access+'/'+user+'.sls', 'w') as fh:
            fh.write(purgestatefile)
        return True

    def add_to_group_state(self, access):
        template = self.templateEnv.get_template(self.adminTemplate)
        template2 = self.templateEnv.get_template(self.engineerTemplate)
        cur = self.conn.cursor()
        cur.execute("select * from admins where active=1")
        userData = cur.fetchall()
        userInfo = {}
        for row in userData:
            userInfo[row[1]] = {"user": row[1], "uid":self.get_uid(row[0],access), "gid":self.get_uid(row[0],access)}
        cur = self.conn.cursor()
        cur.execute("select * from engineers where active=1")
        userData = cur.fetchall()
        engInfo = {}
        for row in userData:
            engInfo[row[1]] = {"user": row[1],"uid":self.get_uid(row[0],access),"gid":self.get_uid(row[0],access)}
        statefile = template.render({'admins': userInfo, 'engineers': engInfo})
        statefile2 = template2.render({'admins':userInfo, 'engineers': engInfo})
        with open('/srv/salt/users/admins.sls', 'w') as fh:
            fh.write(statefile)
        with open('/srv/salt/users/engineers.sls', 'w') as fh:
            fh.write(statefile2)
        return True

    def get_uid(self, id, access):
        if len(str(id)) == 1:
            if access.equals('prod'):
                uid = '600' + str(id)
            else:
                uid = '500' + str(id)
        elif len(str(id)) == 2:
            if access.equals('prod'):
                uid = '60' + str(id)
            else:
                uid = '50' + str(id)
        elif len(str(id)) == 3:
            if access.equals('prod'):
                uid = '6' + str(id)
            else:
                uid = '5' + str(id)
        return uid
