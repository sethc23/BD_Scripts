#!/usr/bin/env python
import os
from sys import argv
from os import path as os_path
from os import environ as os_environ
from uuid import getnode as get_mac

if __name__ == "__main__":


    macs = {'Macbook':'105773427819682',
            'MacBookPro':'117637351435',}

    this_mac = get_mac()
    if str(this_mac)==macs['Macbook']:
        os_path.join('/Users/admin/SERVER2/BD_Scripts/django/Dropbox/aprinto/ENV/lib/python2.7/site-packages')
    elif str(this_mac)==macs['MacBookPro']:
        os_path.join('/Users/admin/django/Dropbox/aprinto/ENV/lib/python2.7/site-packages')

    os_environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(argv)


