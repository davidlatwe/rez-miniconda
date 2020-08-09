
name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language.(Ship via Miniconda)"


@early()
def version():
    """Define Python version from command line option
    """
    import sys
    import argparse
    import subprocess

    if any(help_ in sys.argv[1:] for help_ in ["-h", "--help"]):
        # Skip parsing version string if user is asking for help,
        # or the following parser will print out it's own help
        # message without rez-build's.
        return ""

    parser = argparse.ArgumentParser()

    with open("./parse_build_args.py", "r") as add_args:
        exec(add_args.read(), {"parser": parser})

    args, unknown = parser.parse_known_args()  # parse `sys.argv`
    python_version = args.version

    # raise `subprocess.CalledProcessError` if no matched version found
    subprocess.check_output(["conda",
                             "search",
                             "python=%s" % python_version])

    return python_version


variants = [
    ["platform-*"],
]


build_requires = [
    "miniconda",
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


uuid = "repository.python"
