#!/usr/bin/env python
# bootstrap.py
# Bootstrap and setup a virtualenv with the specified requirements.txt
import os
import sys
import shutil
import subprocess
from optparse import OptionParser


usage = 'usage: %prog [options]'
parser = OptionParser(usage=usage)
parser.add_option('-c', '--clear', dest='clear', action='store_true',
                help='clear out existing virtualenv')
parser.add_option('-i', '--init', dest='init', action='store_true',
                help='Initialize virtual env')
parser.add_option('-u', '--upgrade', dest='upgrade', action='store_true',
                help='Upgrade')

def main():
    if 'VIRTUAL_ENV' not in os.environ or not len(sys.argv) > 1:
        sys.stderr.write('$VIRTUAL_ENV not found.\n\n')
        parser.print_usage()
        sys.exit(-1)
    
    (options, pos_args) = parser.parse_args()
    virtualenv = os.environ['VIRTUAL_ENV']

    if options.init:
        try:
            subprocess.call(['virtualenv', virtualenv])
        except OSError:
            print('virtualenv not found')
    
    if options.clear:
        try:
            subprocess.call(['virtualenv', '--clear', virtualenv])
        except OSError:
            print('virtualenv not found')
    
    pip_args = ['pip', 'install', '-E', virtualenv, '--requirement', 'questionator/config/requirements.txt', '--upgrade']

    if options.upgrade:
        if not os.path.isdir(virtualenv):
            print('virtual environment not initialized. initializing...')
            try:
                subprocess.call(['virtualenv', virtualenv])
            except OSError:
                print('virtualenv not found')
        try:
            subprocess.call(pip_args)
        except OSError:
            pip_args[0] = 'pip-python'
            try:
                subprocess.call(pip_args)
            except OSError:
                print('pip is needed to be installed')


if __name__ == '__main__':
    main()
    sys.exit(0)
