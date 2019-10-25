import os
import importlib
import subprocess
import sys
from copy import deepcopy

from debugging_utils import lprint, spaced_lprint
from grabbing_utils import index_alt_return

def get_version(module):
    """ wrapper to extract version using different possible version handlers

    args:
        module: module

    returns:
        v: string, contains module version number,
            empty string if version is not found
    """
    try:
        v = module.__version__
    except AttributeError:
        try:
            v = module.__ver__
        except AttributeError:
            return 0

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def install_from_gh(url, required_module_version):
    """ Installs module from github url

    TODO: specify required module evrsion installation
     --> how does this even work?
    """
    subprocess.call([sys.executable, "-m", "pip", "install", "git+"+url])

SPECIAL_CASES = {"cv2":"opencv-python"}
GITHUB_CASES = set(["personal_util"])


def relevant_import_line(line):
    if line[:6] == "import":
        return True
    elif line[:4] == "from":
        return True
    return False

def scan_for_imports(filename):
    with open(filename, 'r') as f:
        lines = [line[:-1] for line in f.readlines() if relevant_import_line(line)]
        libs = [line.split(" ")[1] for line in lines]
        libs = [lib[:index_alt_return(lib, ".", len, target='iterable')] for lib in libs]
        libs = [lib for lib in libs if lib not in exception_libs]
    return libs

def categorize_imports(importlist, known_github_sourced):
    """ takes a list of modules and categorizes them for different

    install types.
    returns:
        lists formatted for isntallation type, see example files:
            manual_install: examples/ex_man_inst.txt
            github_install: examples/ex_gh_inst.txt
            to_reqs:        examples/reqs_inst.txt

    TODO: make example files
    """

    exception_libs = ["os", "sys", "math", "importlib", "my_stuff"]
    manual_install = []
    github_install = []
    to_reqs = []

    for lib in importlist:
        if lib in known_github_sourced:
            module = importlib.import_module(lib, package=None)
            github_install.append(lib + "==" + get_version(module) +","+module.url)
            continue
        libname = SPECIAL_CASES.get(lib, lib)
        module = importlib.import_module(lib, package=None)
        version = get_version(module)
        if version:
            to_reqs.append(libname + "==" + version)
        else:
            manual_install.append(lib+","+libname)
    return manual_install, github_install, to_reqs


def make_requirements(known_github_sourced, exclude=[], use_gitignore=True,
    reqfile="requirements.txt",
    manual_reqfile="manual_requirements.txt",
    gh_reqfile="github_requirements.txt"):
    """ Creates a requirements.txt for easy installation with pip;

    differs from "pip freeze" such that not all installed libraries are
        taken up in the requirements file, just the ones used in the
        project directory.
    args:
        exclude: List, files and directories to not be scanned
        use_gitignore: Bool, determines wheter the files in the gitignore are
            left out in scanning, similar pupose as the exclude argument.
        reqfile: String, destination file for the libraries easily installed with pip
        manual_reqfile: String, destination file for not easily installable libraries
        gh_reqfile: String, destination file for the libraries easily installed
            using this packages function "install_github_sources()"
    """
    exclude = set(exclude)
    if use_gitignore:
        f = open(".gitignore", "r")
        exclude.update(set([line[:-1] for line in f.readlines()] + [".git"]))
        f.close()
    print("is the selection of exclusions alright?\nto be excluded:\n")
    lprint(exclude)
    print("#"*10)
    exclude = set(exclude)
    libs = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude]

        path = root.split(os.sep)
        for file in files:
            if file[-3:] == ".py":
                libs.extend(scan_for_imports(file))
    libs = list(set(libs))
    manual_install, github_install, pip_list = categorize_imports(list(set(libs)), known_github_sourced)

    with open(reqfile, "w+") as rqf:
        rqf.write("\n".join(pip_list))
    with open(manual_reqfile, "w+") as mrqf:
        mrqf.write("\n".join(manual_install))
    with open(gh_reqfile, "w+") as ghrqf:
        ghrqf.write("\n".join(github_install))


def install_reqs(reqfile="requirements.txt",
               man_install="manual_requirements.txt",
               gh_reqfile="github_requirements.txt"):
    """ Checks whether all requirements are ready to use, per defined from

    above files. for each module not in the catagory of manual installation it
        installs it, so long as the reqfiles have appropriate format.
        refer to the README.md for these formats
    returns: modules which are not installed and have to be installed manually

    """
    failures = []
    check_pip = []
    check_gh = []
    check_man = []
    failures.extend(process_install(reqfile, reqtype='pip'))
    failures.extend(process_install(gh_reqfile, reqtype='github'))
    if failures:
        print("\n\nErrors:")
        spaced_lprint(failures, add_spacing=True)
        raise RuntimeError("Encountered errors during installation process")
    else:
        with open(man_install, "r") as manf:
            check_man = [line[:-1] for lie in manf.readlines()]
        print("user should install the following modules manually:")
        lprint(check_man)


def process_install(file, reqtype=None):
    """ Walks through the specified requirements file.

    Handles installs based on reqtype, which describes different file formats

    return:
        failures: list --> elems: (failed module, specific error)
    """

    failures = []
    if not (reqtype in ['github', 'pip']):
        raise ValueError("argument reqtype is not a recognized string, got ", reqtype,
            " expected either 'github' or 'pip'")
    with open(file, "r") as f:
        for line in ghreqf.readlines():
            line = line[:-1] + ","
            linedata = line.split(",")
            package_info, url = linedata[0], linedata[1]
            module_name, required_module_version = package_info.split("==")
            if required_module_version == installed_version:
                continue
            else:
                try:
                    if reqtype == 'pip':
                        install(package_info)
                    elif reqtype == 'github':
                        install_from_gh(url, required_module_version)
                except Exception as e:
                    failures.append((module_name, type(e).__name__, e))
    return failures

if __name__ == "__main__":
    lprint([[1,2,3],4,[5,1]], header=[2, "r", []])
    print(eval("123x4".replace('x', '*')))
    make_requirements(exclude=['__pycache__', '.git', 'amv'])
