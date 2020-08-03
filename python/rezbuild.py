
import os
import sys
import shutil
import subprocess


def logger():
    import logging

    package_name = os.environ["REZ_BUILD_PROJECT_NAME"]
    log_name = package_name + ".build"

    # (TODO) Add formatter

    log_handler = logging.StreamHandler()
    log = logging.getLogger(log_name)
    log.addHandler(log_handler)
    log.setLevel(logging.INFO)

    return log


def build(source_path, build_path, install_path, targets=None):
    log = logger()
    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    # Create with `--prefix`
    python_version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    subprocess.check_output(["conda",
                             "create",
                             "--prefix",
                             dst,
                             "python=%s" % python_version,
                             "--yes"])

    # Unregister env location from `~/.conda/environment.txt`
    #   see `../miniconda3/..Lib../site-packages/conda/core/envs_manager.py`
    #   for conda environment registering implementation detail.
    #
    home = os.path.expanduser("~")
    registry = os.path.join(home, ".conda", "environments.txt")

    if not os.path.isfile(registry):
        log.warning("Conda environment.txt not found: %s\n"
                    "Skip location unregistering." % registry)
        return

    # make sure that we are excluding the right location
    locations = []
    with open(registry, "r") as f:
        for loc in f.readlines():
            if dst != os.path.normpath(loc).strip():
                locations.append(loc)

    # re-write without the location we just created
    with open(registry, "w") as f:
        f.writelines(locations)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
