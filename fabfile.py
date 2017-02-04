"""Fabfile for deploying the app on Heroku."""
from __future__ import print_function

import os
import random
import string

from fabric.api import env, local, require
from fabric.colors import cyan


current_dir = os.getcwd()
env.project_name = 'flaskelm'
env.branch = 'master'
env.environments = ['ci', 'stage', 'prod']


#######################################
# Helpers
#######################################

def info(message):
    """Print info message."""
    print(cyan(message))


def create_secret_key():
    """Create a random string of letters and numbers."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))


#######################################
# Local
#######################################

def serve():
    """Run development server."""
    local('FLASK_APP={} FLASK_DEBUG=1 flask run'.format(os.path.join(current_dir, 'server', 'app.py')))


#######################################
# Heroku
#######################################

def heroku_bootstrap():
    """Create an app for every environment on Heroku."""
    require('project_name')
    require('environments')

    info('Initializing Heroku apps...')

    set_remotes()

    for environment in env.environments:
        env.environment = environment
        env.app_name = '{}-{}'.format(env.project_name, env.environment)
        heroku_initialize_app()


def heroku_initialize_app():
    """Initialize a new Heroku app."""
    heroku_create_app()
    heroku_configure_app()
    push()


def heroku_create_app():
    """Create a new app on Heroku."""
    require('app_name')

    info('Creating new app: {}'.format(env.app_name))

    local('heroku create {} --buildpack heroku/python'.format(env.app_name))
    local('heroku buildpacks:add --app {} --index 1 heroku/nodejs'.format(env.app_name))


def heroku_destroy_app():
    require('environment')
    require('project_name')

    app_name = '{}-{}'.format(env.project_name, env.environment)
    info('Deleting app: {}'.format(app_name))

    local('heroku apps:destroy -c {} --app {}'.format(app_name, app_name))


def heroku_configure_app():
    """Configure an app with a basic configuration."""
    require('app_name')

    info('Configure app: {}'.format(env.app_name))

    local('heroku config:set NPM_CONFIG_PRODUCTION=false --app {}'.format(env.app_name))


def set_remotes():
    """Set git remotes for Heroku repositories."""
    require('project_name')
    require('environments')
    info('Setting up git remotes for Heroku...')

    for environment in env.environments:
        local('git remote add {} git@heroku.com:{}-{}.git'.format(environment, env.project_name, environment))


def delete_remotes():
    """Delete git remotes for Heroku repositories."""
    require('environments')
    info('Deleting git remotes for Heroku...')

    for environment in env.environments:
        local('git remote remove {}'.format(environment))


def push():
    """Push to Heroku remote."""
    require('environment')
    require('branch')

    info('Pushing branch "{}" to "{}"'.format(env.branch, env.environment))

    local('git push {} {}:master'.format(env.environment, env.branch))


def open():
    """Open app."""
    require('environment')
    local('heroku open --remote {}'.format(env.environment))


def logs():
    """Show logs."""
    require('environment')
    local('heroku logs -t --remote {}'.format(env.environment))


def init():
    """Bootstrap Heroku apps."""
    heroku_bootstrap()


def ci():
    """Run fab ci [command]."""
    env.environment = 'ci'
    env.app_name = '{}-{}'.format(env.project_name, env.environment)
    env.branch = 'master'


def stage():
    """Run fab stage [command]."""
    env.environment = 'stage'
    env.app_name = '{}-{}'.format(env.project_name, env.environment)
    env.branch = 'master'


def prod():
    """Run fab prod [command]."""
    env.environment = 'prod'
    env.app_name = '{}-{}'.format(env.project_name, env.environment)
    env.branch = 'master'
