# sate

`sate` is a simple replacement for some of what`make` can do. `sate`
focuses on task automation rather than building. By default `sate`
looks for a file called `.satefile`.

## A very simple example

`.satefile`:
```
[lint]
pylint *.py
```

This defines a target called `lint`. Running `sate lint` calls `pylint
*.py`.

## Syntax

All of sate's syntax sits inside brackets. Everything outside the
brackets is either a comment or a command. Comments start with a `#`
and last through the end of the line.

### Targets
A line containing only `[name]` defines a new target. Each line after
a target is a new command.

## TODO

- Variables
- Other tags such as `[nofail]`
- Line continuations (`\`)
- Comments (`#`)
