# radian: A 21 century R console

[![Main](https://github.com/randy3k/radian/actions/workflows/main.yml/badge.svg)](https://github.com/randy3k/radian/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/randy3k/radian/branch/master/graph/badge.svg)](https://codecov.io/gh/randy3k/radian)
[![](https://img.shields.io/pypi/v/radian.svg)](https://pypi.org/project/radian/)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/radian.svg)](https://anaconda.org/conda-forge/radian)
<a href="https://www.paypal.me/randy3k/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg" /></a>


<img src="radian.png"></img>

_radian_ is an alternative console for the R program with multiline editing and rich syntax highlight.
One would consider _radian_ as a [ipython](https://github.com/ipython/ipython) clone for R, though its design is more aligned to [julia](https://julialang.org).

<img width="600px" src="https://user-images.githubusercontent.com/1690993/30728530-b5e9eb5c-9f26-11e7-8453-73a2e880c9de.png"></img>


## Features

- cross platform, runs on Windows, macOS and Linux
- shell mode: hit `;` to enter and `<backspace>` to leave
- reticulate python repl mode: hit `~` to enter
- improved R prompt and reticulate python prompt
    - multiline editing
    - syntax highlight
    - auto completion (reticulate autocompletion depends on `jedi`)
- unicode support
- latex completion
- auto matching parens/quotes.
- bracketed paste mode
- emacs/vi editing mode
- automatically adjust to terminal width
- read more than 4096 bytes per line


## Installation

Requirements:

- An installation of R (version 3.4.0 or above) is required to use _radian_, an R installation binary for your system can be downloaded from https://cran.r-project.org.
- `python` (version 3.7 or above) is also required to install _radian_. If your system doesn't come with a python distribution, it can be downloaded from https://www.python.org/downloads/ or https://conda.io/en/latest/miniconda.html.
- `pip` is optional but it makes the installation a bit easier.

```sh
# install released version
pip3 install -U radian
# to run radian
radian
```

```sh
# or the development version
pip3 install -U git+https://github.com/randy3k/radian
```

If you encounter an error `command not found: radian` when trying to run _radian_, you probably need to add the installation location to your PATH. This location should have been flagged for you during the pip3 install process. But the common installation point on Linux and Mac, for example, would require the following: 

```sh
# below assumes zsh is your default shell; change ".zshrc" to ".bashrc" for vanilla bash shell
echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.zshrc
source $HOME/.zshrc
```

Alternatively, if you use conda or miniconda,
```sh
conda install -c conda-forge radian
```
In this case, it is recommended to install R via conda to ensure consistency in C runtime libraries.

## Alias on unix system

You could alias `r` to _radian_ by putting

```bash
alias r="radian"
```
in `~/.bash_profile` such that `r` would open _radian_ and `R` would still open the traditional R console.
(`R` is still useful, e.g, running `R CMD BUILD`.)


## Settings

_radian_ can be customized by specifying the below options in various locations

- `$XDG_CONFIG_HOME/radian/profile` or `$HOME/.config/radian/profile` (Unix)
- `%USERPROFILE%/radian/profile` (Windows)
- `$HOME/.radian_profile` (Unix)
- `%USERPROFILE%/.radian_profile` (Windows)
- `.radian_profile` in the working directory

The options could be also specified in the `.Rprofile` files, however,
it is not recommended because 

1. the settings are not persistent when vanilla mode is used;
2. it doesn't work well with `packrat` or `renv`.


```r
# Do not copy the whole configuration, just specify what you need!
# see https://pygments.org/styles
# for a list of supported color schemes, default scheme is "native"
options(radian.color_scheme = "native")

# either  `"emacs"` (default) or `"vi"`.
options(radian.editing_mode = "emacs")
# enable various emacs bindings in vi insert mode
options(radian.emacs_bindings_in_vi_insert_mode = FALSE)
# show vi mode state when radian.editing_mode is `vi`
options(radian.show_vi_mode_prompt = TRUE)
options(radian.vi_mode_prompt = "\033[0;34m[{}]\033[0m ")

# indent continuation lines
# turn this off if you want to copy code without the extra indentation;
# but it leads to less elegent layout
options(radian.indent_lines = TRUE)

# auto match brackets and quotes
options(radian.auto_match = TRUE)

# enable the [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/index.html) [`auto_suggest` feature](https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html#auto-suggestion)
# this option is experimental and is known to break python prompt, use it with caution
options(radian.auto_suggest = FALSE)

# highlight matching bracket
options(radian.highlight_matching_bracket = FALSE)

# auto indentation for new line and curly braces
options(radian.auto_indentation = TRUE)
options(radian.tab_size = 4)

# pop up completion while typing
options(radian.complete_while_typing = TRUE)
# the minimum length of prefix to trigger auto completions
options(radian.completion_prefix_length = 2)
# timeout in seconds to cancel completion if it takes too long
# set it to 0 to disable it
options(radian.completion_timeout = 0.05)
# add spaces around equals in function argument completion
options(radian.completion_adding_spaces_around_equals = TRUE)

# automatically adjust R buffer size based on terminal width
options(radian.auto_width = TRUE)

# insert new line between prompts
options(radian.insert_new_line = TRUE)

# max number of history records
options(radian.history_size = 20000)
# where the global history is stored, environmental variables will be expanded
# note that "~" is expanded to %USERPROFILE% or %HOME% in Windows
options(radian.global_history_file = "~/.radian_history")
# the filename that local history is stored, this file would be used instead of
# `radian.global_history_file` if it exists in the current working directory
options(radian.local_history_file = ".radian_history")
# when using history search (ctrl-r/ctrl-s in emacs mode), do not show duplicate results
options(radian.history_search_no_duplicates = FALSE)
# ignore case in history search
options(radian.history_search_ignore_case = FALSE)
# do not save debug browser commands such as `Q` in history
options(radian.history_ignore_browser_commands = TRUE)

# custom prompt for different modes
options(radian.prompt = "\033[0;34mr$>\033[0m ")
options(radian.shell_prompt = "\033[0;31m#!>\033[0m ")
options(radian.browse_prompt = "\033[0;33mBrowse[{}]>\033[0m ")

# stderr color format
options(radian.stderr_format = "\033[0;31m{}\033[0m")

# enable reticulate prompt and trigger `~`
options(radian.enable_reticulate_prompt = TRUE)
```

### Custom key bindings

```r
# allows user defined shortcuts, these keys should be escaped when send through the terminal.
# In the following example, `esc` + `-` sends `<-` and `ctrl` + `right` sends `%>%`.
# Note that in some terminals, you could mark `alt` as `escape` so you could use `alt` + `-` instead.
# Also, note that some ctrl mappings are reserved. You cannot remap m, i, h, d, or c
options(
    radian.escape_key_map = list(
        list(key = "-", value = " <- "),
    ),
    radian.ctrl_key_map = list(
        list(key = "right", value = " %>% ")
    )
)
```

## FAQ

#### Unicode doesn't work in Windows and R 4.2+.

The latest version of R supports Unicode codepage directly. However, radian relies on Python and Python doesn't support Unicode in the way that R supports it. A workaround could be found here: https://github.com/randy3k/radian/issues/269#issuecomment-1169663251. Though it may break the ploting device (running `plot()` will kill radian).


#### I can't specify python runtime in reticulate.

It is expected. `radian` runs on python and the python runtime used by radian is forced in 
reticulate. `reticulate::py_config()` gives the note:
```
NOTE: Python version was forced by the current process
```

In order to use radian with another python runtime, you will need to install `radian` on
that python environment.


#### How to switch to a different R or specify the version of R.

There are serveral options.

- The easiest option is to pass the path to the R binary with `--r-binary`, i.e., `radian --r-binary=/path/to/R`
- Also, one could expose the path to the R binary in the `PATH` variable
- The environment variable `R_BINARY` could also be used to specify the path to R.
- The environment variable `R_HOME` could also be used to specify R home directory. Note that it is should be set as the result of `R.home()`, not the directory where `R` is located. For example, in Unix
```sh
$ env R_HOME=/usr/local/lib/R radian
```

#### Cannot find shared library

Please also make sure that R was installed with the R shared library `libR.so` or `libR.dylib` or `libR.dll`. On Linux, the configure flag `./configure --enable-R-shlib` may be needed to install R from the source. Do not forget to `make clean` to force the recompilation of the files with the correct compiler options.


#### Outdated setuptools

If you encounter

> The package setup script has attempted to modify files on your system that are not within the EasyInstall build area.

Please update your setuptools by

```
pip install -U setuptools

```


#### How to use local history file

_radian_ maintains its own history file `.radian_history` and doesn't use the `.Rhistory` file. A local `.radian_history` is used if it is found in the launch directory. Otherwise, the global history file `~/.radian_history` would be used. To override the default behavior, you could launch _radian_ with the options: `radian --local-history`, `radian --global-history` or `radian --no-history`.


#### Does it slow down my R program?

_radian_ only provides a frontend to the R program, the actual running eventloop is the same as that of the traditional R console. There is no performance sacrifice (or gain) while using this modern command line interface. 

However, it was reported that radian may be slower when using parallel computation, specifially when using forking. User should take extra care in those cases.

#### Nvim-R support

Put
```vim
let R_app = "radian"
let R_cmd = "R"
let R_hl_term = 0
let R_args = []  " if you had set any
let R_bracketed_paste = 1
```
in your vim config. 


#### `reticulate` Auto Completions

To enable reticulate prompt completions, make sure that `jedi` is installed.

```sh
pip install jedi
```

Alternatively, if you use conda,
```sh
conda install -c conda-forge jedi
```


#### Prompt not shown inside a docker container

It maybe caused by the invalid terminal size, try running `stty size` in your terminal
to see if it returns a correct size. You could change the values of it from the environmental variables
`$COLUMNS` and `$LINES` when you log-in the docker container.

```
docker exec -it <container> bash -c "stty cols $COLUMNS rows $LINES && bash"
```

## Why called _radian_?

_radian_ is powered by (π)thon.

## Credits

_radian_ wouldn't be possible without the creative work [prompt_toolkit](https://github.com/jonathanslenders/python-prompt-toolkit/) by Jonathan Slenders.
