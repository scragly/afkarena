import asyncio
import functools
import sys

import click

import afkarena
from afkarena import errors


start_of_line = "\033[F"


def _run_as_async(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.argument("codes", required=True, nargs=-1)
@click.option("--uid", "-u", type=int, required=True, prompt="Your In-Game User ID")
@click.option("--auth", "-a", type=int, required=True, prompt="Your Verification Code")
@_run_as_async
async def redeem(codes, uid: int, auth: int):
    """Redeem a gift code."""
    player = afkarena.Player(uid)
    try:
        click.secho("Verifying...", fg="blue")
        await player.verify(auth)
        click.secho(f"{start_of_line}Fetching user data...", fg="blue")
        await player.fetch_users()
        c_str = ", ".join(codes)
        click.secho(f"{start_of_line}Redeeming codes:      \n  {c_str}", fg="blue")
        results = await player.redeem_codes(*codes)
        await player.close()
    except errors.RequestError as e:
        click.secho(f"Error encountered: {e.__class__.__name__}", fg="red", bold=True)
        await player.close()
        sys.exit(2)

    invalid = results["invalid"]
    expired = results["expired"]
    used = results["used"]
    success = results["success"]
    if success:
        click.secho("These users have successfully redeemed codes:", fg="green", bold=True)
        for user, codes in success.items():
            codes = ", ".join(codes)
            click.secho(f"  {user.name}: {codes}", fg="green")
    elif used:
        click.secho("These users have already redeemed these codes:", fg="yellow", bold=True)
        for user, codes in used.items():
            codes = ", ".join(codes)
            click.secho(f"  {user.name}: {codes}", fg="yellow")
    if expired:
        codes = ", ".join(set(expired))
        click.secho(f"The following codes were expired:", fg="red", bold=True)
        click.secho(f"  {codes}", fg="red")
    if invalid:
        codes = ", ".join(set(invalid))
        click.secho(f"The following codes were invalid:", fg="red", bold=True)
        click.secho(f"  {codes}", fg="red")

if __name__ == "__main__":
    redeem(auto_envvar_prefix="AFKARENA")
