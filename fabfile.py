import time
from os.path import exists
from functools import wraps

from fabric.api import *
from fabric.colors import red, green, blue, yellow
from fabric.utils import indent
from fabric.operations import prompt

from fabtools import user
from fabtools import require
from fabtools import supervisor

from fabric.context_managers import hide, settings


from environments import *

# status messages


def _success(message):
    print green(indent(message, spaces=4))


def _error(message):
    print red(indent(message, spaces=4))


def _info(message):
    print blue(indent(message, spaces=4))


def _option(message):
    print yellow(indent(message, spaces=4))
# decorators


def no_output(warn_only=False):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            with settings(hide('stdout', 'warnings'), warn_only=warn_only):
                return method(*args, **kwargs)
        return wrapper
    return decorator


def activate(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        with prefix('. /usr/local/bin/virtualenvwrapper.sh'):
            with prefix('workon %s' % env.project_name):
                return method(*args, **kwargs)
    return wrapper

# development initialization functions


@no_output()
def check_virtual_environment(dir):
    # check if virtualenv exists, and if not, create one
    if exists(dir):
        _info("Virtual environment for %s already exists." % env.project_name)
    else:
        with prefix('. /usr/local/bin/virtualenvwrapper.sh'):
            local('mkvirtualenv --no-site-packages %s' % env.project_name)
            # append debug to postactivate script
            with lcd('%s/bin' % env.virtualenv_dir):
                local('echo export DEBUG=%s >> postactivate' % env.debug)
            _success("Virtual environment for %s created." %
                     env.project_name)


@activate
@no_output()
def install_requirements():
    # install application requirements via pip
    environment = "development" if env.debug else "production"
    local('pip install -r %s/requirements/%s.txt' %
          (env.project_dir, environment))
    _info("Requirements for %s installed or updated successfully." %
          env.project_name)


@no_output(warn_only=True)
def check_database(name):
    # check if the database exits, and if not, create one
    if local('''psql -d %(name)s -c ""''' % locals()).succeeded:
        _info("Database for %s already exists." % env.project_name)
    else:
        local('createdb %s' % env.project_name)
        _success("Database for %s created." % env.project_name)


@task
def init_development():
    check_virtual_environment(env.virtualenv_dir)
    install_requirements()
    check_database(env.project_name)


# deployment hooks
# check is user exists
@no_output()
def check_user():
    new_user = env.user
    with settings(user='root'):
        if not user.exists(new_user):
            password = prompt("Password for the new user: ")
            user.create(
                new_user, group='sudo', extra_groups=['docker'],
                password=password, shell="/bin/bash")
            _success("User %s created" % new_user)
        else:
            _info("User %s already exists." % new_user)


@task
def add_ssh_key():
    home_dir = expanduser("~")
    user.add_ssh_public_key(env.user, '%s/.ssh/id_rsa.pub' % home_dir)


@no_output()
def check_backup():
    dirs = [
        '/home/%s/%s/media' % (env.user, env.backup_dir),
        '/home/%s/%s/database' % (env.user, env.backup_dir),
    ]

    require.files.directories(dirs, owner=env.user, use_sudo=True)


@no_output()
def check_system():
    require.deb.packages(env.apt_packages)
    require.python.packages(env.pip_packages, use_sudo=True)
    _info("System set up.")


@task
def update_code():
    require.git.working_copy(env.remote_url)


@task
def init_production():
    check_user()
    check_system()
    add_ssh_key()
    check_backup()
    update_code()

# returns backups sorted in decreasing order by date made


def list_backups(dir):
    output = run('ls -lA %(dir)s' % locals())
    files = output.replace('\r', '').split('\n')[1:]
    backups = []
    for file in files:
        info = file.split()
        filename = info[-1]
        filesize = info[-5]
        backups.append([filename, filesize])
    return sorted(backups, key=lambda x: x[0], reverse=True)


def bytestomegabytes(bytes):
    return (bytes / 1024) / 1024


def get_options(dir):
    list = list_backups(dir)
    options = {i: [list[i][0], list[i][1]] for i in range(len(list))}
    _info("Choose a media backup")
    for key, value in options.items():
        _option("%s: %s %smb" %
                (key, value[0], bytestomegabytes(float(value[1]))))
    choice = int(prompt("Your choice (-1 to quit): "))
    while choice < -1 or choice > len(list):
        choice = int(prompt("Try again (-1 to quit): "))

    return choice, options


@task
def backup_database():
    run('docker exec %s_db_1 \
         pg_dump -U postgres postgres -F c > ~/%s/database/%s.dump'
        % (env.project_name.replace('_', ''),
           env.backup_dir,
           time.strftime("%Y%m%d-%H%M%S")))


@task
def restore_database():
    choice, options = get_options("~/%s/database/" % env.backup_dir)

    if choice == -1:
        return

    filename = options[choice][0]

    run('docker exec %s_db_1 \
         pg_restore /%s/database/%s -U postgres -d postgres'
        % (env.project_name.replace('_', ''),
           env.backup_dir,
           filename))


@task
def backup_media():
    run('docker exec %s_web_1 \
         tar cvf /%s/media/%s.tar /home/docker/code/src/media'
        % (env.project_name.replace('_', ''),
           env.backup_dir,
           time.strftime("%Y%m%d-%H%M%S")))


@task
def restore_media():
    choice, options = get_options("~/%s/media/" % env.backup_dir)

    if choice == -1:
        return

    filename = options[choice][0]

    run('docker exec %s_web_1 \
         tar xvf /%s/media/%s -C /'
        % (env.project_name.replace('_', ''),
           env.backup_dir,
           filename))


@task
def backup():
    backup_database()
    backup_media()


# only use when containers are running
@task
def restore():
    restore_database()
    restore_media()


@task
def collect_and_migrate():
    with cd(env.project_dir):
        run('fig run web python manage.py collectstatic --noinput')
        run('fig run web python manage.py migrate')


def rebuild():
    _info("Rebuild image.")
    with cd(env.project_dir):
        run('fig build web')


@task
def start():
    _info("Starting app.")
    with cd(env.project_dir):
        run('fig up -d')
        collect_and_migrate()
    _success("Started successfully.")


@task
def stop():
    _info("Stopping app.")
    with cd(env.project_dir):
        run('fig stop')
        _success("Stopped successfully.")


@task
def update():
    stop()
    update_code()
    start()
    _info("updated")


@task
def update_hard():
    stop()
    update_code()
    rebuild()
    start()
    _info("updated")
