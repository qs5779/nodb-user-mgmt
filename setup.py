"""Python setup.py for nodb_user_mgmt package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("nodb_user_mgmt", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="nodb_user_mgmt",
    version=read("nodb_user_mgmt", "VERSION"),
    description="Awesome nodb_user_mgmt created by qs5779",
    url="https://github.com/qs5779/nodb-user-mgmt/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="qs5779",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["nodb_user_mgmt = nodb_user_mgmt.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
