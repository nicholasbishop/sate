

TAG: starts with '[' and ends with ']'

TAGs can CONTAIN a TARGET NAME, VARIABLES, and DIRECTIVES.

TAG contents are SPACE-SEPARATED.

VARIABLES are KEY="VALUE" pairs.

DIRECTIVES are predefined FUNCTIONS, for example: nofail(),
include("..."), ...

---

TARGETS have a NAME, optional VARIABLES, and COMMANDS.

COMMANDS are strings with very few rules. They are shell-interpreted
and can make use of VARIABLES.

Each line in a TARGET is a new command, unless the previous line ends
with a continuation character: `\`.

---

The top level is a SATEFILE, default name `.satefile`. A SATEFILE
contains VARIABLES, TARGETS, and DIRECTIVES.
