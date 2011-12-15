#!/usr/bin/python
#install script for the-questionator
import os
import sys
import subprocess
from optparse import OptionParser


usage = 'usage: %prog [options]'
parser = OptionParser(usage=usage)
parser.add_option('-c', '--clear', dest='clear', action='store_true',
                help='Clear VIRTUAL_ENV')
parser.add_option('-i', '--install', dest='install', action='store_true',
                help='Install VIRTUAL_ENV')


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

            if not os.path.isdir('run'):
                try:
                    subprocess.call(['mkdir', 'run'])
                except OSError:
                    print('unable to create run directory')

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
                    print('pip not found')
        else:
            print('%s already exists. nothing to do.' % virtualenv)


if __name__ == '__main__':
    bootstrap()
