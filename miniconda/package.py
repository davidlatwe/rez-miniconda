
name = "miniconda"

authors = ["Anaconda, Inc."]

description = "A free minimal installer for conda."

version = "latest"

variants = [
    ["platform-*"],
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    system = globals()["system"]
    env = globals()["env"]

    if system.platform == "windows":
        env.PATH.prepend("{root}/payload/Library/bin")
        env.PATH.prepend("{root}/payload/Scripts")
        env.PATH.prepend("{root}/payload")
    else:
        env.PATH.prepend("{root}/payload/bin")


uuid = "repository.miniconda"
