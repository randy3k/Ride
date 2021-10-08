__version__ = '1.0.0.dev0'

__all__ = ["get_app", "main"]


def main():
    import optparse
    import os
    import sys
    import subprocess
    from rchitect.utils import Rhome, rversion

    try:
        # failed to import jedi on demand in some edge cases.
        import jedi  # noqa
    except ImportError:
        pass

    parser = optparse.OptionParser("usage: radian")
    parser.add_option("-v", "--version", action="store_true", dest="version", help="Get version")
    parser.add_option("--r-binary", dest="r", help="Path to R binary")
    parser.add_option("--profile", dest="profile", help="Path to .radian_profile, ignore both global and local profiles")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", help="Don't print startup message")
    parser.add_option("--no-environ", action="store_true", dest="no_environ", help="Don't read the site and user environment files")
    parser.add_option("--no-site-file", action="store_true", dest="no_site_file", help="Don't read the site-wide Rprofile")
    parser.add_option("--no-init-file", action="store_true", dest="no_init_file", help="Don't read the user R profile")
    parser.add_option("--local-history", action="store_true", dest="local_history", help="Force using local history file")
    parser.add_option("--global-history", action="store_true", dest="global_history", help="Force using global history file")
    parser.add_option("--no-history", action="store_true", dest="no_history", help="Don't load any history files")
    parser.add_option("--vanilla", action="store_true", dest="vanilla", help="Combine --no-history --no-environ --no-site-file --no-init-file")
    parser.add_option("--save", action="store_true", dest="save", help="Do save workspace at the end of the session")
    parser.add_option("--ask-save", action="store_true", dest="ask_save", help="Ask to save R data")
    parser.add_option("--restore-data", action="store_true", dest="restore_data", help="Restore previously saved objects")
    parser.add_option("--debug", action="store_true", dest="debug", help="Debug mode")
    parser.add_option("--coverage", action="store_true", dest="coverage", help=optparse.SUPPRESS_HELP)
    parser.add_option("--cprofile", action="store_true", dest="coverage", help=optparse.SUPPRESS_HELP)

    # we accept these options, but never check them
    parser.add_option("--no-save", action="store_true", dest="no_save", help=optparse.SUPPRESS_HELP)
    parser.add_option("--no-restore-data", action="store_true", dest="no_restore_data", help=optparse.SUPPRESS_HELP)
    parser.add_option("--no-restore-history", action="store_true", dest="no_restore_history", help=optparse.SUPPRESS_HELP)
    parser.add_option("--no-restore", action="store_true", dest="no_restore", help=optparse.SUPPRESS_HELP)
    parser.add_option("--no-readline", action="store_true", dest="no_readline", help=optparse.SUPPRESS_HELP)
    parser.add_option("--interactive", action="store_true", dest="interactive", help=optparse.SUPPRESS_HELP)

    options, args = parser.parse_args()

    if options.r:
        os.environ["R_BINARY"] = options.r

    r_home = Rhome()

    if options.version:
        if r_home:
            r_binary = os.path.normpath(os.path.join(r_home, "bin", "R"))
            r_version = rversion(r_home)
        else:
            r_binary = "NA"
            r_version = "NA"
        print("radian version: {}".format(__version__))
        print("r executable: {}".format(r_binary))
        print("r version: {}".format(r_version))
        print("python executable: {}".format(sys.executable))
        print("python version: {:d}.{:d}.{:d}".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro))
        return

    os.environ["RADIAN_VERSION"] = __version__
    os.environ["RADIAN_COMMAND_ARGS"] = " ".join(
        ["--" + k.replace("_", "-") for k, v in options.__dict__.items() if v])

    if not r_home:
        raise RuntimeError("Cannot find R binary. Expose it via the `PATH` variable.")

    if sys.platform.startswith("linux"):
        # respect R_ARCH variable?
        libPath = os.path.join(r_home, "lib")
        ldpaths = os.path.join(r_home, "etc", "ldpaths")
        if "R_LD_LIBRARY_PATH" not in os.environ or libPath not in os.environ["R_LD_LIBRARY_PATH"]:
            if os.path.exists(ldpaths):
                R_LD_LIBRARY_PATH = subprocess.check_output(
                    ". \"{}\"; echo $R_LD_LIBRARY_PATH".format(ldpaths),
                    shell=True
                ).decode("utf-8").strip()
            elif "R_LD_LIBRARY_PATH" in os.environ:
                R_LD_LIBRARY_PATH = os.environ["R_LD_LIBRARY_PATH"]
            else:
                R_LD_LIBRARY_PATH = libPath

            if libPath not in R_LD_LIBRARY_PATH:
                R_LD_LIBRARY_PATH = "{}:{}".format(libPath, R_LD_LIBRARY_PATH)

            os.environ['R_LD_LIBRARY_PATH'] = R_LD_LIBRARY_PATH

            if "LD_LIBRARY_PATH" in os.environ:
                LD_LIBRARY_PATH = "{}:{}".format(R_LD_LIBRARY_PATH, os.environ["LD_LIBRARY_PATH"])
            else:
                LD_LIBRARY_PATH = R_LD_LIBRARY_PATH
            os.environ['LD_LIBRARY_PATH'] = LD_LIBRARY_PATH
            if sys.argv[0].endswith("radian"):
                os.execv(sys.argv[0], sys.argv)
            else:
                os.execv(sys.executable, [sys.executable, "-m", "radian"] + sys.argv[1:])

    from .radianapp import RadianApplication
    RadianApplication(r_home, ver=__version__).run(options)


# cleanup to be injected by __main__.py
main.cleanup = None


def get_app():
    from .radianapp import RadianApplication
    return RadianApplication.instance
