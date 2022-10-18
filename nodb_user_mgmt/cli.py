from os import getenv
from pathlib import Path
from sys import exit

import click
from dotenv import load_dotenv

from nodb_user_mgmt import __version__
from nodb_user_mgmt.userinfo import UserInfoMgr

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
SALT_WARNING = """WARNING: You should provide a secret salt value using environment
variable NODBUSERMGMT_SALT. A default salt value was created and
saved in {}. Be sure to secure this file appropriately.
"""


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


def load_salt(sp, oride=False):
    assert load_dotenv(dotenv_path=sp, override=oride)
    salt = getenv("NODBUSERMGMT_SALT", False)
    if not salt:
        raise KeyError(f"Failed to find NODBUSERMGMT_SALT in environment or {str(sp)}")
    return salt


def get_salt(psalt):
    salt = getenv("NODBUSERMGMT_SALT", False)
    if not salt:
        if psalt.is_file():
            salt = load_salt(psalt, False)
        else:
            from bcrypt import gensalt

            salt = gensalt().decode()
            print(SALT_WARNING.format(str(psalt)))
            with open(psalt, "w") as sf:
                print(f"NODBUSERMGMT_SALT='{salt}'", file=sf)
    return salt


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-f",
    "--file",
    "dest",
    default="./ui.json",
    help="Specify user info file. [default ./ui.json]",
)
@click.option(
    "-s", "--saltfile", help="Specify environment file containing NODBUSERMGMT_SALT"
)
@click.option("-S", "--salt", help="Specify salt value")
@click.option(
    "-v", "--verbose/--no-verbose", default=False, help="Specify verbose flag."
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
def main(ctx, dest, saltfile, salt, verbose):
    """Main function for nodb_user_mgmt module."""
    ctx.ensure_object(dict)
    ctx.obj["dest"] = dest
    ctx.obj["verbose"] = verbose
    if salt is not None:
        ctx.obj["salt"] = salt
    elif saltfile is not None:
        sp = Path(saltfile)
        if not sp.is_file():
            import errno
            import os

            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), saltfile)
        ctx.obj["salt"] = load_salt(sp)
    else:
        dp = Path(dest)
        sp = dp.parent.joinpath(dp.stem + ".salt")
        ctx.obj["salt"] = get_salt(sp)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def adduser(ctx, username, password):
    ctx.ensure_object(dict)
    print(ctx)
    ui = UserInfoMgr(ctx.obj["dest"], ctx.obj["salt"], ctx.obj["verbose"])
    ui.adduser(username, password)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def checkpw(ctx, username, password):
    ui = UserInfoMgr(ctx.obj["dest"], ctx.obj["salt"], ctx.obj["verbose"])
    if ui.checkpw(username, password):
        return 0
    else:
        return 1


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.option("-p", "--password", required=True, help="Specify password.")
@click.pass_context
def upduser(ctx, username, password):
    ui = UserInfoMgr(ctx.obj["dest"], ctx.obj["salt"], ctx.obj["verbose"])
    ui.upduser(username, password)


@click.command()
@click.option("-u", "--username", required=True, help="Specify usernmame.")
@click.pass_context
def deluser(ctx, username):
    ui = UserInfoMgr(ctx.obj["dest"], ctx.obj["salt"], ctx.obj["verbose"])
    ui.deluser(username)


@click.command()
@click.pass_context
def show(ctx):
    ui = UserInfoMgr(ctx.obj["dest"], ctx.obj["salt"], ctx.obj["verbose"])
    ui.show()


main.add_command(adduser)
main.add_command(checkpw)
main.add_command(upduser)
main.add_command(deluser)
main.add_command(show)


if __name__ == "__main__":
    exit(main(obj={}))
