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
Call = seq(Ident, ArgList)

Directive = (Call | Ident).combine(types.Directive)
DirectiveList = Directive.sep_by(Whitespace)

CommandTag = OpenBrack >> DirectiveList << CloseBrack

def _make_target(name, _, directives):
    """Make a Target from name and directives."""
    return types.Target(name=name, directives=directives)

TargetTagContentWithDirectives = (seq(Ident, Whitespace, DirectiveList)
                                  .combine(_make_target))
TargetTagContentSimple = Ident.combine(types.Target)

TargetTagContent = TargetTagContentWithDirectives | TargetTagContentSimple
TargetTag = OpenBrack >> TargetTagContent << CloseBrack
