#!/usr/bin/python3
import os
import shutil

site_packages_path = os.path.join(os.path.dirname(os.__file__), 'site-packages')
install_path = os.path.join(site_packages_path, 'catutils')

if not os.path.exists(install_path):
    print('catutils has not been installed!')
    exit(1)

shutil.rmtree(install_path)
print('catutils has been uninstalled!')
