
name = "miniconda"

authors = ["Anaconda, Inc."]

description = "A free minimal installer for conda."

version = ""

build_command = False


def commands():
    env.PATH.prepend("path/to/pre-installed/miniconda")


uuid = "repository.miniconda"
