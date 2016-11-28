#!/usr/bin/env python3
"""
Usage:
    jobbieget.py <key> [<default>]

Get a single value or values from the jobbie config file. Print values separated
by NUL bytes to standard output.

"""
import sys

from docopt import docopt
import yaml

def main(opts):
    config = yaml.load(sys.stdin)
    default = opts.get('<default>') or []
    values = config.get(opts['<key>'], default)
    if isinstance(values, str):
        values = [values]
    for v in values:
        sys.stdout.write(v)
        sys.stdout.write('\0')

if __name__ == '__main__':
    main(docopt(__doc__))
