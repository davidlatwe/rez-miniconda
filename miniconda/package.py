
name = "miniconda"

authors = ["Anaconda, Inc."]

description = "A free minimal installer for conda."

version = "latest"

variants = [
    ["platform-*"],
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env.PATH.prepend("{root}/payload/bin")


uuid = "repository.miniconda"
