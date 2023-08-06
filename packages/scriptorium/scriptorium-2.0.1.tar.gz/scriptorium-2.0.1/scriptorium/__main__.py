#!/usr/bin/env python
#Script to build a scriptorium paper in a cross-platform friendly fashion

import argparse
import shutil
import sys
import os
import os.path

import scriptorium

def build_cmd(args):
    """Creates PDF from paper in the requested location."""
    pdf = scriptorium.to_pdf(args.paper, use_shell_escape=args.shell_escape)

    if args.output and pdf != args.output:
        shutil.move(pdf, args.output)

def info(args):
    """Function to attempt to extract useful information from a specified paper."""
    fname = scriptorium.paper_root(args.paper)

    if not fname:
        raise IOError('{0} does not contain a valid root document.'.format(args.paper))

    if not fname:
        print('Could not find the root of the paper.')
        sys.exit(1)

    if args.template:
        template = scriptorium.get_template(os.path.join(args.paper, fname))
        if not template:
            print('Could not find footer indicating template name.')
            sys.exit(2)
        print(template)

def template_cmd(args):
    """Prints out all installed templates."""

    if args.update:
        scriptorium.update_template(args.update)

    if args.list:
        templates = scriptorium.all_templates(args.template_dir)
        for template in templates:
            print('{0}'.format(template))

    if args.readme:
        template = scriptorium.find_template(args.readme)
        template_readme = os.path.join(template, 'README.md')
        if template and os.path.exists(template_readme):
            with open(template_readme, 'r') as readme:
                print(readme.read())

    if args.install:
        scriptorium.install_template(args.install)

def create(args):
    """Creates a new paper given flags."""
    if not scriptorium.create(args.output, args.template, force=args.force, config=args.config):
        sys.exit(3)

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # Build Command
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("paper", default=".", nargs='?', help="Directory containing paper to build")
    build_parser.add_argument('-o', '--output', help='Destination of PDF')
    build_parser.add_argument('-s', '--shell-escape', action='store_true', default=False, help='Flag indicating shell-escape should be used')
    build_parser.set_defaults(func=build_cmd)

    # Info Command
    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("paper", default=".", help="Directory containing paper to make")
    info_parser.add_argument('-t', '--template', action="store_true", help="Flag to extract template")
    info_parser.set_defaults(func=info)

    # New Command
    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("output", help="Directory to create paper in.")
    new_parser.add_argument("-f", "--force", action="store_true", help="Overwrite files in paper creation.")
    new_parser.add_argument("-t", "--template", help="Template to use in paper.")
    new_parser.add_argument("-c", "--config", nargs=2, action='append', default=[],
                            help='Flag to provide options for filling out variables in new papers, in the form key value')
    new_parser.set_defaults(func=create)

    # Template Command
    template_parser = subparsers.add_parser("template")
    template_parser.add_argument('-l', '--list', action='store_true', default=False, help='List available templates')
    template_parser.add_argument('-u', '--update', default=None, help='Update the given template to the latest version')
    template_parser.add_argument('-r', '--readme', help='Print README for the specified template')
    template_parser.add_argument("-t", "--template_dir", default=None, help="Overrides template directory used for listing templates")
    template_parser.add_argument('-i', '--install', help='Install repository at given URL in template directory')
    template_parser.set_defaults(func=template_cmd)

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()