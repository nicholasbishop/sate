# sate

`sate` is a simple replacement for some of what`make` can do. `sate`
focuses on task automation rather than building. By default `sate`
looks for a file called `.satefile` (and searches upwards through
parent directories).

This repository contains dueling Python and Rust implementations.

* https://github.com/nicholasbishop/sate
* https://pypi.python.org/pypi/sate/
* https://crates.io/crates/sate

## A very simple example

`.satefile`:
```
[lint]
pylint *.py
```

This defines a target called `lint`. Running `sate lint` calls `pylint
*.py`.

## Usage

To install `sate`, just run `cargo install sate`. You can also
download the [latest release
build](https://github.com/nicholasbishop/sate/releases) directly from
Github.

To use a target, run `sate <target-name>`.

To list targets, run `sate --list` or `sate -l`.

## Syntax

A target begins with a bracketed name on its own line, for example
`[lint]`. Everything after a target name is a command. A command is
just a subprocess executed in a shell (so you can use shell syntax
such as pipes in the command). There can be any number of commands in
a target. Commands are run in the order they are defined. Execution
stops if any command exits with a non-zero value.

Each command can optionally begin with a directive, which is a
bracketed list of calls. Example: `[nofail()] mkdir test`. This
defines a `mkdir` command that never fails, i.e. a non-zero exit code
is ignored.

Unlike Makefiles, a target is `sate` doesn't check for a file of that
name, so there's no need for a `.PHONY` equivalent.

## TODO

- Variables
- Other tags such as `[nofail]`
- Line continuations (`\`)
- Comments (`#`)
