from __future__ import absolute_import

import click

from realms import cli_group
from realms.lib.util import random_string
from realms.lib.util import green, red, yellow
from .models import User


@cli_group(short_help="Auth Module")
def cli():
    pass


@cli.command()
@click.argument('username')
@click.argument('email')
@click.option('--password', help='Leave blank for random password')
def create_user(username, email, password):
    """ Create a new user
    """
    show_pass = not password

    if not password:
        password = random_string(12)

    if User.get_by_username(username):
        red("Username %s already exists" % username)
        return

    if User.get_by_email(email):
        red("Email %s already exists" % email)
        return

    User.create(username, email, password)
    green("User %s created" % username)

    if show_pass:
        yellow("Password: %s" % password)
