#!/bin/python
import sys
import os

apps = sys.argv[1:]
for i in apps:
    if not os.path.exists("{0}/fixtures".format(i)):
        os.mkdir("{0}/fixtures".format(i))
    if i == "user":
        os.system("python manage.py dumpdata user -o user/fixtures/user.json")
        os.system("python manage.py dumpdata auth.user -o user/fixtures/auth.user.json")
    os.system("python manage.py dumpdata {0} -o {0}/fixtures/{0}.json".format(i))
