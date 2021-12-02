"""Setup Vinted discord bot Package."""
from setuptools import setup, find_packages

setup(
    name="discord-vinted",
    version="1.0.0",
    packages=find_packages(),
    scripts=[],
    install_requires=[
        "requests",
        "discord.py"
    ],
    author="Melchior Prugniaud",
    author_email="melchior.prugniaud@gmail.com",
    description="A bot for discord and vinted.",)
