from fabric.api import run, cd, settings


def deploy():
    app_dir = 'home/Vanetix/Documents/projects/testing/'
    with settings(warn_only=True):
        if run("test -d %s" % app_dir).failed:
            run("git clone git@github.com:/TxSSC/the-questionator.git %s" % app_dir)
    with cd(app_dir):
        run("git pull")
        run("python bootstrap.py -i")
