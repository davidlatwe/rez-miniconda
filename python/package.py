
name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language.(Ship via Miniconda)"


@early()
def version():
    """Define Python version from command line option
    """
    import argparse
    import subprocess

    parser = argparse.ArgumentParser()

    with open("./parse_build_args.py", "r") as add_args:
        exec(add_args.read(), {"parser": parser})

    args, unknown = parser.parse_known_args()  # parse `sys.argv`
    python_version = args.python

    # raise `subprocess.CalledProcessError` if no matched version found
    subprocess.check_output(["conda",
                             "search",
                             "python=%s" % python_version])

    return python_version


variants = [
    ["platform-*"],
]


build_command = "python {root}/rezbuild.py {install}"


def commands():
    env.PATH.prepend("{root}/payload/bin")


uuid = "repository.python"
