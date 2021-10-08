import os


def test_shell(terminal):
    terminal.current_line().assert_startswith("r$>")
    terminal.write(";")
    terminal.current_line().assert_startswith("#!>")
    terminal.write("git --version\n")
    terminal.previous_line(2).assert_startswith("git version")
    terminal.current_line().assert_startswith("#!>")
    terminal.write("\b")
    terminal.current_line().assert_startswith("r$>")


def test_cd(terminal):
    terminal.current_line().assert_startswith("r$>")
    terminal.write(";")
    d = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "radi"))
    terminal.write("cd {}".format(d))
    terminal.current_line().strip().assert_endswith(os.sep + "radi")
    try:
        terminal.write("\t")
        terminal.current_line().strip().assert_endswith(os.sep + "radian")
    except Exception:
        terminal.write("\t")
        terminal.current_line().strip().assert_endswith(os.sep + "radian")
    terminal.write("\n")
    terminal.previous_line(2).strip().assert_endswith(os.sep + "radian")
    terminal.write("cd -\n")
    terminal.previous_line(2).strip().assert_equal(os.getcwd())
    terminal.current_line().assert_startswith("#!>")


def test_cd2(terminal):
    terminal.current_line().assert_startswith("r$>")
    terminal.write(";")
    d = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "radi"))
    terminal.write("cd \"{}".format(d))
    terminal.current_line().strip().assert_endswith(os.sep + "radi")
    try:
        terminal.write("\t")
        terminal.current_line().strip().assert_endswith(os.sep + "radian")
    except Exception:
        terminal.write("\t")
        terminal.current_line().strip().assert_endswith(os.sep + "radian")
    terminal.write("\"\n")
    terminal.previous_line(2).strip().assert_endswith(os.sep + "radian")
    terminal.write("cd -\n")
    terminal.previous_line(2).strip().assert_equal(os.getcwd())
    terminal.current_line().assert_startswith("#!>")
