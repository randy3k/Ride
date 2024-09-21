import sys
import pytest


def test_readline(terminal):
    # issue #106
    terminal.current_line().assert_startswith("r$>")
    terminal.write("cat('hello'); readline('> ')\n")
    terminal.previous_line(1).assert_startswith("hello")
    terminal.current_line().assert_startswith("> ")


def test_askpass(terminal):
    # issue #359
    terminal.current_line().assert_startswith("r$>")
    terminal.write("askpass::askpass('askpass> ')\n")
    terminal.current_line().assert_startswith("askpass>")
    terminal.write("answer\n")
    terminal.previous_line(2).assert_contain("\"answer\"")


def test_strings(terminal):
    # issue #377
    terminal.current_line().assert_startswith("r$>")
    terminal.write("x <- 'a'\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(x)\n")
    terminal.previous_line(2).assert_startswith("[1] 1")


@pytest.mark.skipif(sys.platform.startswith("win"), reason="windows doesn't support bpm.")
def test_strings_bracketed(terminal):
    terminal.current_line().assert_startswith("r$>")
    terminal.write("\x1b[200~x <- '" + 'a'*10 + "'\x1b[201~\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(x)\n")
    terminal.previous_line(2).assert_startswith("[1] 10")

    terminal.write("\x1b[200~x <- '" + 'a'*5000 + "'\x1b[201~\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(x)\n")
    terminal.previous_line(2).assert_startswith("[1] 5000")

    terminal.write("\x1b[200~x <- '" + 'a'*2000 + '\n' + 'b'*2000 + "'\x1b[201~\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(x)\n")
    terminal.previous_line(2).assert_startswith("[1] 4001")

    s = '中'*1000 + '\n' + '文'*1000 + '\n' + '中'*1000 + '\n' + '文'*1000

    terminal.write("\x1b[200~x <- '" + s + "'\x1b[201~\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(x)\n")
    terminal.previous_line(2).assert_startswith("[1] 4003")

    # different padding
    terminal.write("\x1b[200~xy <- '" + s + "'\x1b[201~\n")
    terminal.current_line().strip().assert_equal("r$>")
    terminal.write("nchar(xy)\n")
    terminal.previous_line(2).assert_startswith("[1] 4003")


def test_early_termination(terminal):
    terminal.current_line().assert_startswith("r$>")
    terminal.write("Sys.setlocale(category = 'LC_MESSAGES', locale = 'en_US.UTF8'); stop('!')\x1b\rd = 1\n")
    terminal.previous_line(2).assert_startswith("Error")
    terminal.write("d\n")
    terminal.previous_line(2).assert_startswith("Error: object 'd' not found")
