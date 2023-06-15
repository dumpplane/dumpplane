#!/usr/bin/env python

from crossplane import parse

from argparse import ArgumentParser, RawDescriptionHelpFormatter

#from . import __version__

__version__ = '0.1'

class _SubparserHelpFormatter(RawDescriptionHelpFormatter):
    def _format_action(self, action):
        line = super(RawDescriptionHelpFormatter, self)._format_action(action)

        if action.nargs == 'A...':
            line = line.split('\n', 1)[-1]

        if line.startswith('    ') and line[4] != ' ':
            parts = filter(len, line.lstrip().partition(' '))
            line = '  ' + ' '.join(parts)

        return line

def parse_args(args=None):
    parser = ArgumentParser(
        formatter_class=_SubparserHelpFormatter,
        description='various operations for nginx config files',
        usage='%(prog)s <command> [options]'
    )
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title='commands')

    def create_subparser(function, help):
        name = function.__name__
        prog = 'crossplane ' + name
        p = subparsers.add_parser(name, prog=prog, help=help, description=help)
        p.set_defaults(_subcommand=function)
        return p

    p = create_subparser(parse, 'parses a json payload for an nginx config')
    p.add_argument('filename', help='the nginx config file')
    p.add_argument('-o', '--out', type=str, help='write output to a file')
    p.add_argument('-i', '--indent', type=int, metavar='NUM', help='number of spaces to indent output')
    p.add_argument('--ignore', metavar='DIRECTIVES', default='', help='ignore directives (comma-separated)')
    p.add_argument('--no-catch', action='store_false', dest='catch', help='only collect first error in file')
    p.add_argument('--tb-onerror', action='store_true', help='include tracebacks in config errors')
    p.add_argument('--combine', action='store_true', help='use includes to create one single file')
    p.add_argument('--single-file', action='store_true', dest='single', help='do not include other config files')
    p.add_argument('--include-comments', action='store_true', dest='comments', help='include comments in json')
    p.add_argument('--strict', action='store_true', help='raise errors for unknown directives')

    def help(command):
        if command not in parser._actions[-1].choices:
            parser.error('unknown command %r' % command)
        else:
            parser._actions[-1].choices[command].print_help()

    p = create_subparser(help, 'show help for commands')
    p.add_argument('command', help='command to show help for')

    parsed = parser.parse_args(args=args)

    print(parsed.__dict__)

    # this addresses a bug that was added to argparse in Python 3.3
    if not parsed.__dict__:
        parser.error('too few arguments')

    return parsed



def main():
    kwargs = parse_args().__dict__
    func = kwargs.pop('_subcommand')
    func(**kwargs)


if __name__ == '__main__':
    main()
