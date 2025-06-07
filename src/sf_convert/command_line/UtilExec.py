"""Script to provide utilities support sftool-server."""

import argparse
import os
import json

from sf_convert.sffile.guess_sf_format import guess_sf_format


def checkfmts(args):

    # Determine output - default json
    out_json = args.json or not args.text
    out_text = args.text

    result = []
    for sf in args.sf:
        if os.path.isfile(sf):
            res = guess_sf_format(sf)
        else:
            res = "Could not open file"
        result.append([sf, res])

    if out_text:
        for line in result:
            print(line[0], line[1])
    if out_json:
        print(json.dumps(result))

    return 0


def create_parser():
    # Need to be local for parameters
    def usagecallback(args):  # pylint: disable=unused-argument
        parser.print_help()

    parser = argparse.ArgumentParser(description="Some utilities for support sf-tool server")
    parser.set_defaults(func=usagecallback)

    # group = parser.add_mutually_exclusive_group(required=True)
    subparsers = parser.add_subparsers(help="subcommand help")

    parser_fmt = subparsers.add_parser("checkfmts",
                                       help="Checks the format of SF files")
    parser_fmt.add_argument("--sf", type=str, nargs="+", required=True,
                            help="Structure factor files")

    group_fmt = parser_fmt.add_mutually_exclusive_group()
    group_fmt.add_argument('--json', action='store_true',
                           help="Output json format")
    group_fmt.add_argument('--text', action='store_true',
                           help="Output text format")

    parser_fmt.set_defaults(func=checkfmts)

    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    main()
