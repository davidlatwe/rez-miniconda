
name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language."

# $ conda search python
version = "2.7.18"

build_command = "conda create --prefix $REZ_BUILD_INSTALL_PATH --yes"


def commands():
    env.PATH.prepend("{root}/bin")


uuid = "repository.python"
