from os import getenv
from sys import exit

import click

from nodb_user_mgmt import __version__
from nodb_user_mgmt.userinfo import UserInfoMgr

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
SALT_WARNING = """WARNING: You should provide a secret salt value using
environment variable NODBUSERMGMT_SALT"""


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


def get_salt():
    default_salt = "3E^svy6dn^35"
    salt = getenv("NODBUSERMGMT_SALT", default_salt)
    if default_salt == salt:
        print(SALT_WARNING)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-f",
    "--file",
    "dest",
    default="./user-info.json",
    help="Specify user info file. [default ./user-info.json]",
)
@click.option(
    "-s", "--saltfile", help="Specify environment file containing NODBUSERMGMT_SALT"
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="show version and exit",
)
@click.pass_context
def main(ctx, dest):
    """Main function for nodb_user_mgmt module."""
    ctx.ensure_object(dict)
    ctx.obj["dest"] = dest
    # ctx.obj["output"] = output
    # ctx.obj["quiet"] = quiet
    # ctx.obj["refresh"] = refresh
    # ctx.obj["test"] = test
    # ctx.obj["verbose"] = verbose


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def adduser(ctx, username, password):
    ctx.ensure_object(dict)
    print(ctx)
    ui = UserInfoMgr(ctx.obj["dest"])
    ui.adduser(username, password)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def checkpw(ctx, username, password):
    ui = UserInfoMgr(ctx.obj["dest"])
    ui.checkpw(username, password)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def upduser(ctx, username, password):
    ui = UserInfoMgr(ctx.obj["dest"])
    ui.upduser(username, password)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.pass_context
def deluser(ctx, username):
    ui = UserInfoMgr(ctx.obj["dest"])
    ui.deluser(username)


@click.command()
@click.pass_context
def show(ctx):
    ui = UserInfoMgr(ctx.obj["dest"])
    ui.show()


main.add_command(adduser)
main.add_command(checkpw)
main.add_command(upduser)
main.add_command(deluser)
main.add_command(show)


if __name__ == "__main__":
    exit(main(obj={}))
