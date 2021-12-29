"""Setup Vinted discord bot Package."""
from setuptools import setup, find_packages

setup(
    name="discord-vinted",
    version="1.1.0",
    packages=find_packages(),
    scripts=[],
    entry_points={
        "console_scripts": [
            "vinted = vinted.cli.cli:cli"
        ]
    },
    install_requires=[
        "requests",
        "discord.py",
        "discord-components",
        "click",
        "GitPython"
    ],
    author="Melchior Prugniaud",
    author_email="melchior.prugniaud@gmail.com",
    description="A bot for discord and vinted.",
)