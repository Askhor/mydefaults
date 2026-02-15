import argparse
import sys
from argparse import ArgumentParser, Namespace
from functools import wraps
from typing import Callable, Generator

from colorama import Fore

type MAGIC = Generator[None, Namespace, None]

all_sub_commands = []


def intercept_interrupts(func):
    @wraps(func)
    def impl(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print(f"{Fore.RED}Program was interrupted by user{Fore.RESET}", file=sys.stderr)

    return impl


def flatten_decorator(deco):
    def impl0(*args, **kwargs):
        def impl1(func):
            return deco(func, *args, **kwargs)

        return impl1

    return impl0


@flatten_decorator
def command(func: Callable[[ArgumentParser], None], version: str):
    @wraps(func)
    @intercept_interrupts
    def impl():
        name = func.__name__.replace("_", "-")
        description = func.__doc__
        parser = ArgumentParser(prog=name, description=description, add_help=True)
        parser.add_argument('-v', '--verbose', action='store_true', help="Show more output")
        parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

        func(parser)

    return impl


def sub_command(func: Callable[[ArgumentParser], MAGIC]):
    def send_to_generator(args: Namespace, generator: MAGIC):
        try:
            generator.send(args)
        except StopIteration:
            pass

    @wraps(func)
    def impl(subparsers) -> None:
        parser = subparsers.add_parser(func.__name__, description=func.__doc__, help=func.__doc__)
        generator: MAGIC = func(parser)
        next(generator)
        parser.set_defaults(sub_command=lambda args: send_to_generator(args, generator))

    all_sub_commands.append(impl)

    return impl


def add_sub_commands(subparsers):
    for cmd in all_sub_commands:
        cmd(subparsers)


def run_sub_command(args: argparse.Namespace):
    if hasattr(args, "sub_command"):
        args.sub_command(args)
        exit(0)
