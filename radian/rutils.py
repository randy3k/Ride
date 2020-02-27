from __future__ import unicode_literals
import os
import sys
from rchitect import rcopy, rcall, reval
from rchitect._cffi import ffi, lib
from rchitect.interface import roption, protected, rstring_p
from .key_bindings import map_key


def prase_text_complete(text):
    status = ffi.new("ParseStatus[1]")
    s = rstring_p(text)
    orig_stderr = sys.stderr
    sys.stderr = None
    with protected(s):
        lib.R_ParseVector(s, -1, status, lib.R_NilValue)
        sys.stderr = orig_stderr
    return status[0] != 2


def package_is_loaded(pkg):
    return pkg in rcopy(rcall(("base", "loadedNamespaces")))


def package_is_installed(pkg):
    return pkg in rcopy(reval(".packages(TRUE)"))


def installed_packages():
    return rcopy(
        list,
        reval(
            """
            tryCatch(
                base::.packages(TRUE),
                error = function(e) character(0)
            )
            """
            )
        )


def source_file(path):
    rcall(("base", "source"), path, rcall(("base", "new.env")))


def user_path(*args):
    return os.path.join(rcopy(rcall(("base", "path.expand"), "~")), *args)


def source_radian_profile(path):
    if not path:
        if os.path.exists(".radian_profile"):
            path = ".radian_profile"
        else:
            path = user_path(".radian_profile")
    path = os.path.expanduser(path)
    if os.path.exists(path):
        source_file(path)


def load_custom_key_bindings(*args):
    esc_keymap = roption("radian.escape_key_map", [])
    for m in esc_keymap:
        map_key(("escape", m["key"]), m["value"], mode=m["mode"] if "mode" in m else "r")


def register_cleanup(cleanup):
    rcall(("base", "reg.finalizer"),
          rcall(("base", "getOption"), "rchitect.py_tools"),
          cleanup,
          onexit=True)


def run_on_load_hooks():
    hooks = roption("radian.on_load_hooks", [])
    for hook in hooks:
        hook()
