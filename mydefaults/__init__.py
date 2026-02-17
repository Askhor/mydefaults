import logging

from colorama import Fore

from mydefaults.argparse import command, sub_command, add_sub_commands, run_sub_command, MAGIC


def create_logger(name: str):
    log = logging.getLogger(name)
    console = logging.StreamHandler()
    log.addHandler(console)
    log.setLevel(logging.DEBUG)
    console.setFormatter(
        logging.Formatter(
            f"{{asctime}} [{Fore.YELLOW}{{levelname:>5}}{Fore.RESET}] {Fore.BLUE}{{name}}{Fore.RESET}: {{message}}",
            style="{", datefmt="W%W %a %I:%M"))
