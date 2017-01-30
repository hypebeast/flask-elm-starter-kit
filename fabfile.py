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
    local('flask run')


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
    require('environment')
    require('app_name')

    info('Creating new app: {}'.format(env.app_name))

    local('heroku create {} --buildpack heroku/python'.format(env.app_name))
    local('heroku buildpacks:add --app {} --index 1 heroku/nodejs'.format(env.app_name, env.environment))


def heroku_configure_app():
    """Configure an app with a basic configuration."""
    require('environment')
    require('project_name')

    info('Configure app: {}'.format(env.app_name))


def set_remotes():
    """Set git remotes for Heroku repositories."""
    require('project_name')
    info('Setting up git remotes for Heroku...')

    local('git remote add ci git@heroku.com:{}-ci.git'.format(env.project_name))
    local('git remote add stage git@heroku.com:{}-stage.git'.format(env.project_name))
    local('git remote add prod git@heroku.com:{}-prod.git'.format(env.project_name))


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
    env.branch = 'master'


def stage():
    """Run fab stage [command]."""
    env.environment = 'stage'
    env.branch = 'master'


def prod():
    """Run fab prod [command]."""
    env.environment = 'prod'
    env.branch = 'master'
