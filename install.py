#!/usr/bin/python3
import os
import shutil

site_packages_path = os.path.join(os.path.dirname(os.__file__), 'site-packages')
install_path = os.path.join(site_packages_path, 'catutils')

if os.path.exists(install_path):
    print('catutils has been installed on your computer. Please run uninstall.py script to delete it first.')
    exit(1)

shutil.copytree('./catutils', install_path)
print('catutils has been installed to ' + install_path)
