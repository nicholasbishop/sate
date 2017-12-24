import collections
import logging

import parsy

from sate import types

LOG = logging.getLogger(__name__)


class ParseError(ValueError):
    pass


IDENTIFIER = parsy.regex(r'[^ \t\(\)]+')
WHITESPACE = parsy.regex(r'[ \t]+')


def parse_call():
    open_paren = parsy.string('(')
    close_paren = parsy.string(')')
    arg_list = open_paren >> IDENTIFIER.sep_by(WHITESPACE) << close_paren
    return parsy.seq(IDENTIFIER, arg_list)


def parse_directives(text):
    directive = (parse_call() | IDENTIFIER).combine(types.Directive)
    directive_list = directive.sep_by(WHITESPACE)
    return directive_list.parse(text)


def parse_line(line):
    comment_start = line.find('#')
    LOG.debug('comment_start: %s', comment_start)
    has_comment = comment_start != -1
    LOG.debug('has_comment: %s', has_comment)

    pre_comment_end = comment_start if has_comment else len(line)
    LOG.debug('pre_comment_end: %s', pre_comment_end)
    tag_start = line.find('[', 0, pre_comment_end)
    tag_end = line.find(']', 0, pre_comment_end)
    has_tag = tag_start != -1

    tag_text = None

    # Get tag
    if has_tag and tag_end == -1:
        raise ParseError('missing "]"')
    elif (not has_tag) and tag_end != -1:
        raise ParseError('unexpected "]"')
    elif tag_end < tag_start:
        raise ParseError('unexpected "]"')
    elif has_tag:
        tag_text = line[tag_start + 1:tag_end]

    # Get command text
    post_tag_start = 0 if not has_tag else tag_end + 1
    command_text = line[post_tag_start:pre_comment_end].strip()
    command = types.Command(text=command_text)

    if tag_text and command.text:
        yield command.with_directives(list(parse_directives(tag_text)))
    elif tag_text:
        yield types.Target(tag_text)
    elif command.text:
        yield command

    # Get comment
    if has_comment:
        yield types.Comment(line[comment_start + 1:])


def compose(elements):
    target = None
    for elem in elements:
        LOG.debug('target: %s, elem: %s', target, elem)
        if isinstance(elem, types.Comment):
            yield elem
        elif isinstance(elem, types.Target):
            if target is None:
                target = elem
            else:
                yield target
                target = elem
        elif isinstance(elem, types.Command):
            if target is None:
                raise ParseError('invalid command: outside of target')
            else:
                target = target.add_command(elem)
        else:
            raise TypeError('unexpected element type: {}'.format(elem))
    if target:
        yield target


def parse_file(rfile):
    def gen():
        for line in rfile.readlines():
            parsed = parse_line(line)
            for elem in parsed:
                yield elem

    return compose(gen())


def load_satefile(rfile):
    targets = collections.OrderedDict()
    for elem in parse_file(rfile):
        if isinstance(elem, types.Target):
            name = elem.name
            if name in targets:
                raise KeyError('duplicate target: ' + name)
            else:
                targets[name] = elem
    return types.Satefile(targets=targets)
