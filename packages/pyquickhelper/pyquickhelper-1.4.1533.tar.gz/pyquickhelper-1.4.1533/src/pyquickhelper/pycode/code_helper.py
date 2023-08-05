"""
@file
@brief Various function to clean the code.
"""

import os
import autopep8
from ..filehelper.synchelper import explore_folder


def remove_extra_spaces_and_pep8(filename, apply_pep8=True):
    """
    removes extra spaces in a filename, replace the file in place

    @param      filename        file name
    @param      apply_pep8      if True, calls ``autopep8`` on the file
    @return                     number of removed extra spaces

    .. versionchanged:: 1.0
        Parameter *apply_pep8* was added.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except PermissionError as e:
        raise PermissionError(filename) from e
    except UnicodeDecodeError as e:
        raise Exception(
            "unable to load file {} due to unicode errors".format(filename)) from e

    if len(lines) > 0 and "#-*-coding:utf-8-*-" in lines[0].replace(" ", ""):
        with open(filename, "r", encoding="utf8") as f:
            try:
                lines = f.readlines()
            except UnicodeDecodeError as e:
                raise Exception("unable to read: " + filename) from e
        encoding = "utf8"
    else:
        encoding = None

    def cdiff(lines):
        lines2 = [_.rstrip(" \r\n") for _ in lines]
        last = len(lines2) - 1
        while last >= 0 and len(lines2[last]) == 0:
            last -= 1
        last += 1
        lines2 = lines2[:last]

        diff = len("".join(lines)) - len("\n".join(lines2)) + len(lines)
        return diff, lines2

    diff, lines2 = cdiff(lines)

    if os.path.splitext(filename)[-1] == ".py":
        r = autopep8.fix_lines(
            lines2,
            options=autopep8.parse_args(['']))

        if encoding is None:
            with open(filename, "w") as f:
                f.write(r)
        else:
            with open(filename, "w", encoding="utf8") as f:
                f.write(r)
        if r != "".join(lines):
            diff, lines2 = cdiff(r.split("\n"))
        else:
            diff = 0

    elif diff != 0:
        if encoding is None:
            with open(filename, "w") as f:
                f.write("\n".join(lines2))
        else:
            with open(filename, "w", encoding="utf8") as f:
                f.write("\n".join(lines2))

    if not os.path.exists(filename):
        raise FileNotFoundError(
            "issue when applying autopep8 with filename: {0}".format(filename))
    return diff


def remove_extra_spaces_folder(
        folder, extensions=(".py", ".rst"), apply_pep8=True):
    """
    removes extra files in a folder for specific file extensions

    @param      folder      folder to explore
    @param      extensions  list of file extensions to process
    @param      apply_pep8      if True, calls ``autopep8`` on the file
    @return                 the list of modified files

    The function does not check files having
    ``/build/`` or ``/dist/`` or ``temp_``
    or ``/build2/`` or ``/build3/``
    in their name.

    .. versionchanged:: 1.0
        Parameter *apply_pep8* was added.
    """
    neg_pattern = "|".join("[/\\\\]{0}[/\\\\]".format(_) for _ in ["build", "build2", "build3",
                                                                   "dist", "_venv", "_todo", "dist_module27", "_virtualenv"])
    files = explore_folder(folder, neg_pattern=neg_pattern, fullname=True)[1]
    mod = []
    for f in files:
        fl = f.lower().replace("\\", "/")
        if "/temp_" not in fl and "/build/" not in fl \
                and "/dist/" not in fl \
                and "/build2/" not in fl \
                and "/build3/" not in fl \
                and "/_virtualenv/" not in fl \
                and ".egg/" not in fl \
                and "/_venv/" not in fl \
                and "/_todo/" not in fl \
                and "/dist_module27" not in fl \
                and os.stat(f).st_size < 200000:
            ext = os.path.splitext(f)[-1]
            if ext in extensions:
                d = remove_extra_spaces_and_pep8(f, apply_pep8=apply_pep8)
                if d != 0:
                    mod.append(f)
    return mod
