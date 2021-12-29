"""A CLI for vinted tools."""
import logging
from pathlib import Path

import git
import click

logger = logging.getLogger(__name__)

DIRECTORY = Path(__file__).parent.parent.parent
SETUP_FILE = DIRECTORY.resolve() / "setup.py"

@click.group()
def cli():
    """Vinted CLI"""
    logger.setLevel(logging.INFO)

@cli.command()
@click.argument("release_type")
def release(release_type):

    # Check if repo is master
    repo = git.Repo(".", search_parent_directories=True)
    if not repo.active_branch.name == "master":
        click.echo(f"""
            Your actual branch is {repo.active_branch.name} you must be in master.
        """)
        raise click.Abort()
    
    # Read setup.py to increment with the correct version
    with open(SETUP_FILE, "r") as r:
        setup = r.read()
        version = [line[13:-2] for line in setup.splitlines() if line.startswith('    version="')][0]
        setup = "\n".join(setup.splitlines())
        r.close()

    # Current version
    v = version.split(".")
    major = int(v[0])
    minor = int(v[1])
    fix = int(v[2])
    click.echo(f"Current version is: {v}")

    # Check release type
    if release_type == "major":
        next_version = f"{major + 1}.0.0"
    elif release_type == "minor":
        next_version = f"{major}.{minor + 1}.0"
    elif release_type == "fix":
        next_version = f"{major}.{minor}.{fix + 1}"
    else:
        click.echo("Release type must be in ['major', 'minor', 'fix']")
        raise click.Abort()

    click.confirm(f"You are going to release {next_version}, are you sure ?", abort=True)
    # Write to setup.py
    with open(SETUP_FILE, "w") as w:
        w.write(setup.replace(version, f'{next_version}'))
        w.close()

    # Push setup.py new version to master
    repo.git.add(update=True)
    repo.index.commit("Increment version of discord-vinted")
    repo.git.push()

    # Push to heroku master
    repo.git.push("heroku", "master")
