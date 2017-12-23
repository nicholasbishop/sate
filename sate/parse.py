import attr
import logging

LOG = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class Command(object):
    text = attr.ib()
    directives = attr.ib(default=attr.Factory(list))

    def with_directives(self, directives):
        return Command(text=self.text, directives=directives)


@attr.s(frozen=True, slots=True)
class Comment(object):
    text = attr.ib()


@attr.s(frozen=True, slots=True)
class Target(object):
    name = attr.ib()
    commands = attr.ib(default=attr.Factory(list))


class ParseError(ValueError):
    pass


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
    command = Command(text=line[post_tag_start:pre_comment_end].strip())

    if tag_text and command.text:
        yield command.with_directives(tag_text)
    elif tag_text:
        yield Target(tag_text)
    elif command.text:
        yield command
    
    # Get comment
    if has_comment:
        yield Comment(line[comment_start + 1:])


def compose(elements):
    target = None
    for elem in elements:
        # Throw out comments for now
        if isinstance(elem, Comment):
            yield elem
        elif isinstance(elem, Target):
            if target is None:
                target = elem
            else:
                yield target
                target = elem
        else:
            if target is None:
                raise ParseError('invalid command: outside of target')
            else:
                yield target.add_command(elem)
    if target:
        yield target
