#!/usr/bin/python
#install script for the-questionator
import os
import sys
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


def bootstrap():
    if 'VIRTUAL_ENV' not in os.environ or not len(sys.argv) > 1:
        sys.stderr.write('$VIRTUAL_ENV not found.\n\n')
        parser.print_usage()
        sys.exit(-1)
    
    (options, pos_args) = parser.parse_args()
    virtualenv = os.environ['VIRTUAL_ENV']
    
    if options.clear:
        try:
            subprocess.call(['virtualenv', '--clear', virtualenv])
        except OSError:
            print('virtualenv not found')
    
    pip_args = ['pip', 'install', '-E', virtualenv, '--requirement', 'questionator/config/requirements.txt', '--upgrade']

    if options.install:
        if not os.path.isdir(virtualenv):
            print('creating and installing to virtual environment: %s' % virtualenv)
            try:
                subprocess.call(['mkdir', 'run'])
            except OSError:
                pass

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
        else:
            print('%s already exists. nothing to do.' % virtualenv)


if __name__ == '__main__':
    bootstrap()
