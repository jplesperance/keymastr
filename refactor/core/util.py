from os.path import join
import re

from refactor.core.config import settings


def app_relative(path):
    return join(settings.CELLTOOL_HOME, path)


def is_ipv4_host(ip):
    """True if [ip] matches a /32 IPV4 address like Amazon expects:
        1.2.3.4/32
    Groups of hosts should always be defined with EC2 security groups, so this
    function should reject all IP ranges with size > 1.
    """
    return re.match(r'(\d{1,3}\.){3}\d{1,3}/32', ip) is not None
