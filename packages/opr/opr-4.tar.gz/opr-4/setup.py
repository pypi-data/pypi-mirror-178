# This file is placed in the Public Domain.


"object programming runtime"


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opr",
    version="4",
    author="Bart Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opr",
    description="object programming runtime",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["opr"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
