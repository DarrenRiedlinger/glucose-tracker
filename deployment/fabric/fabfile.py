from fabric.api import local, env, cd, sudo


env.hosts = ['www.glucosetracker.net']

# The user account that owns the application files and folders.
owner = 'glucosetracker'

app_name = 'glucosetracker'
app_directory = '/webapps/glucosetracker/glucose-tracker'
settings_file = 'settings.production'


def run_tests():
    local('cd ../../glucosetracker && coverage run manage.py test -v 2 --settings=settings.test')


def deploy():
    """
    Deploy the app to the remote host.

    Steps:
        1. Change to the app's directory.
        2. Stash and clear any changes in the local git repo.
        3. Pull changes from the remote master branch in git.
        4. Activate virtualenv and run the postactivate script.
        5. Run pip install using the requirements.txt file.
        6. Run South migrations.
        7. Restart gunicorn WSGI server using supervisor.
    """
    with cd(app_directory):

        sudo('git fetch', user=owner)
        sudo('git reset --hard origin/master', user=owner)

        venv_command = 'source ../bin/activate && source ../bin/postactivate'

        pip_command = 'pip install -r requirements.txt'
        sudo('%s && %s' % (venv_command, pip_command), user=owner)

        south_command = 'python glucosetracker/manage.py migrate --all ' \
                        '--settings=%s' % settings_file
        sudo('%s && %s' % (venv_command, south_command), user=owner)

        collectstatic_command = 'python glucosetracker/manage.py collectstatic --noinput ' \
                                '--settings=%s' % settings_file
        sudo('%s && %s' % (venv_command, collectstatic_command), user=owner)

        sudo('supervisorctl restart glucosetracker')
