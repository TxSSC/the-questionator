from fabric.api import run, cd, settings


APP_DIR = '~/projects'
VIRTUAL_ENV = 'venv'


def deploy():
    with settings(warn_only=True):
        if run('test -d %s' % APP_DIR).failed:
            run('git clone git@github.com:/TxSSC/the-questionator.git %s' % APP_DIR)
    with cd(APP_DIR):
        run('git pull')
        run('export VIRTUAL_ENV="%s"' % VIRTUAL_ENV)
        run('python bootstrap.py --install')


def clean_env():
    with cd(APP_DIR):
        run('python bootstrap.py --clean')
        run('find . -name "*.pyc" -delete')


def reload():
    with cd(APP_DIR):
        run('kill -HUP `find . -name "questionator.pid" -exec cat {} \;`')


def stop():
    with cd(APP_DIR):
        run('kill -SIGINT `find . -name "questionator.pid" -exec cat {} \;`')


def start():
    with cd(APP_DIR):
        run('%s/bin/gunicorn -c questionator/config/gunicorn.conf engine:app &' % VIRTUAL_ENV)
