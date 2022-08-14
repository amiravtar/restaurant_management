#!/bin/python
import sys
import os

if len(sys.argv) > 1:
    apps = sys.argv[1:]
else:
    apps = ["restaurant", "food", "order"]  # deliver user

for i in apps:
    if i == "user":
        os.system("python manage.py loaddata user/fixtures/auth.user.json")
        os.system("python manage.py loaddata user")
    os.system("python manage.py loaddata {0}".format(i))
