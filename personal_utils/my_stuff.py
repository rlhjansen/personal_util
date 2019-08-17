import os
import importlib


SPECIAL_CASES = {"cv2":"opencv-python"}

def index_alwaysret(iterable, required_value):
    try:
        ind = iterable.index(required_value)
        return ind
    except ValueError:
        return len(iterable)

def relevant_import_line(line):
    if line[:6] == "import":
        return True
    elif line[:4] == "from":
        return True
    return False

def scan_for_imports(filename):
    exception_libs = ["os", "sys", "math", "importlib", "my_stuff"]
    manual_install = []
    to_reqs = []
    with open(filename, 'r') as f:
        lines = [line[:-1] for line in f.readlines() if relevant_import_line(line)]
        libs = [line.split(" ")[1] for line in lines]
        libs = [lib[:index_alwaysret(lib, ".")] for lib in libs]
        libs = [lib for lib in libs if lib not in exception_libs]
        for lib in libs:
            libname = SPECIAL_CASES.get(lib, lib)
            exec("import " + lib)
            module = importlib.import_module(lib, package=None)
            try:
                to_reqs.append(libname + "==" + module.__version__)
            except AttributeError:
                try:
                    print(lib, module.__ver__)
                    to_reqs.append(libname + "==" + module.__ver__)
                except AttributeError:
                    manual_install.append(libname)
    return manual_install, to_reqs


def make_requirements(exclude=[], use_gitignore=True, reqfile="requirements.txt", manual_reqfile="manual_requirements.txt"):
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
    pip_list = []
    manual_list = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude]

        path = root.split(os.sep)
        for file in files:
            if file[-3:] == ".py":
                manual_additions, pip_additions = scan_for_imports(file)
                manual_list.extend(manual_additions)
                pip_list.extend(pip_additions)
    lprint(pip_list)
    with open(reqfile, "w+") as rqf:
        rqf.write("\n".join(sorted(list(set(pip_list)))))
    with open(manual_reqfile, "w+") as mrqf:
        mrqf.write("\n".join(manual_list))


def lprint(iterable, header=None):
    if header:
        print("\t".join([str(elem) for elem in header]))
    for elem in iterable:
        if type(elem) == list:
            print("\t".join([str(e) for e in elem]))
        else:
            print(str(elem))



if __name__ == "__main__":
    lprint([[1,2,3],4,[5,1]], header=[2, "r", []])
    print(eval("123x4".replace('x', '*')))
    make_requirements(exclude=['__pycache__', '.git', 'amv'])
