#!/usr/local/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'webapptitude==0.0.10','console_scripts','gae_testrunner.py'
__requires__ = 'webapptitude==0.0.10'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('webapptitude==0.0.10', 'console_scripts', 'gae_testrunner.py')()
    )
