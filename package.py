
name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language."

# $ conda search python
version = "2.7.18"

variants = [
    ["platform-osx"],
]

build_command = "conda create --prefix $REZ_BUILD_INSTALL_PATH python=2.7.18 --yes"


def commands():
    env.PATH.prepend("{root}/bin")


uuid = "repository.python"
