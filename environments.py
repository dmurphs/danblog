from os.path import dirname, realpath, expanduser, join

from fabric.api import env, task


def common():
    env.project_name = "danblog"


@task
def dev():
    common()
    env.debug = True
    # local virtualenv setup, adjust accordingly
    env.virtualenv_dir = join(
        expanduser("~"), ".virtualenvs/%s" % env.project_name)
    env.project_dir = join(
        dirname(realpath(__file__)), 'src')


@task
def prod():
    common()
    # host or a list of hosts
    env.hosts = ['0.0.0.0']
    # user under which the app will run. if different from this, also change
    # in /deploy/supervisor.conf
    env.user = 'dan'
    env.project_dir = join(
        '/home/%s' % env.user, env.project_name)
    # backup directory ex. "backup"
    env.backup_dir = "backup"
    # default packages to install
    env.pip_packages = ['fig']
    env.apt_packages = ['supervisor']
    # github url, ex. "https://github.com/user/repo.git"
    env.remote_url = "https://github.com/dmurphs/danblog.git"
