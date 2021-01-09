import os

from . import options
from .convert import convert


def main():
    parser = options.build_parser()
    args = parser.parse_args()
    if args.target not in ["quantumult-x", "clash"] and args.target != "all":
        print("wrong parameter!")
        return
    convert(args.target)


if __name__ == "__main__":
    main()
