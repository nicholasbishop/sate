from parsy import regex, seq, string

from sate import types

# pylint: disable=invalid-name

OpenParen = string('(')
CloseParen = string(')')

OpenBrack = string('[')
CloseBrack = string(']')

Whitespace = regex(r'[ \t]+')
Ident = regex(r'[^ \t\(\)\[\]]+')

ArgList = OpenParen >> Ident.sep_by(Whitespace) << CloseParen
Call = seq(Ident, ArgList).combine(types.Call) | Ident.map(types.Call)

CallList = Call.sep_by(Whitespace)

CommandTag = OpenBrack >> CallList << CloseBrack


def _make_target(name, _, directives):
    """Make a Target from name and directives."""
    return types.Target(name=name, directives=directives)


TargetTagContentWithCalls = (seq(Ident, Whitespace, CallList)
                             .combine(_make_target))
TargetTagContentSimple = Ident.map(types.Target)

TargetTagContent = TargetTagContentWithCalls | TargetTagContentSimple
TargetTag = OpenBrack >> TargetTagContent << CloseBrack
