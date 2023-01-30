import argparse

from . import __version__


def build_parser():
    """Build and configure an ArgumentParser object"""
    parser = argparse.ArgumentParser(
        usage="gen_domain_list [option] url")
    parser.add_argument("--target", "-t")
    parser.add_argument("--tag", "-g")
    # parser.add_argument("url", metavar="URL")
    parser.add_argument("-v", "--version", action="version",
                        version="gen-domain-list v"+__version__)
    return parser
