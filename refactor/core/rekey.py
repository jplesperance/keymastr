from refactor.core.config import settings
from refactor.core.add import Add
import jinja2
import sqlite3

class Rekey(object):

    key_type = 'RSA'
    key_length = 4096
    admin_users = {}
    eng_users = {}
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

    def run(self, ):
