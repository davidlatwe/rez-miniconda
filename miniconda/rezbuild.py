
import os
import sys
import shutil
import platform
import subprocess


url_prefix = "https://repo.anaconda.com/miniconda/"

LNX = "Miniconda3-latest-Linux-x86_64.sh"
MAC = "Miniconda3-latest-MacOSX-x86_64.sh"
WIN = "Miniconda3-latest-Windows-x86_64.exe"


PY3 = sys.version_info[0] == 3


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


log = logger()


def build(source_path, build_path, install_path, targets=None):

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    installers = {
        "Linux": lambda: on_posix(url_prefix + LNX, dst),
        "Darwin": lambda: on_posix(url_prefix + MAC, dst),
        "Windows": lambda: on_nt(url_prefix + WIN, dst),
    }
    try:
        installer = installers[platform.system()]
    except KeyError:
        log.critical("Unknown platform.")
    else:
        installer()


def on_nt(url, dst):
    file_name = url.split("/")[-1]
    download(url, file_name)

    log.info("Installing..")
    subprocess.check_output(["start",
                             "/wait",
                             "\"\"",
                             file_name,
                             "/InstallationType=JustMe",
                             "/RegisterPython=0",
                             "/S",
                             "/D=%s" % dst])


def on_posix(url, dst):
    file_name = url.split("/")[-1]
    download(url, file_name)

    log.info("Installing..")
    subprocess.check_output(["bash", file_name, "-b", "-p", dst])


def download(url, file_name):
    # https://stackoverflow.com/a/22776/14054728
    if PY3:
        import urllib.request as urllib
    else:
        import urllib2 as urllib

    log.info("Downloading installer from %s" % url)

    u = urllib.urlopen(url)
    f = open(file_name, "wb")

    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print(status)

    f.close()


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
