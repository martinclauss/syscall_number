#!/usr/bin/env python3

# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# flake8: max-line-length = 120


import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

from collections import OrderedDict
from operator import itemgetter

import click


CONFIG = {
    "syscall_header_file": "/usr/include/bits/syscall.h",
    "cache_file_32bit": "{}/.cache/syscall_number/32bit.json".format(os.environ["HOME"]),
    "cache_file_64bit": "{}/.cache/syscall_number/64bit.json".format(os.environ["HOME"]),
}


BITNESS_32 = "32"
BITNESS_64 = "64"


def read_file_content(file_path):
    try:
        return pathlib.Path(file_path).read_text()
    except (FileNotFoundError, UnicodeDecodeError):
        raise RuntimeError("Error(s) reading from file {}".format(file_path))


def write_file_content(file_path, data):
    try:
        return pathlib.Path(file_path).write_text(data)
    except (FileNotFoundError, UnicodeDecodeError):
        raise RuntimeError("Error(s) writing to file {}".format(file_path))


def parse_syscall_names():
    syscall_names = []

    syscall_name_regex = re.compile(r"^.+SYS_(?P<syscall_name>[^ ]+)")

    try:
        content = read_file_content(CONFIG["syscall_header_file"])
    except RuntimeError as error:
        raise error

    for line in content.split("\n"):
        match = syscall_name_regex.match(line)

        if match:
            syscall_names.append(match.group("syscall_name"))

    return syscall_names


def check_program(program_name):
    try:
        output = subprocess.check_output("which {}".format(program_name).split(), shell=False)
    except OSError:
        output = ""

    return output != ""


def check_sane_integer(syscall_number):
    try:
        syscall_integer = int(syscall_number)

        if not 0 <= syscall_integer <= 999:
            return False

    except ValueError:
        return False

    return True


def get_syscall_number(syscall_name, bitness):
    if bitness == BITNESS_32:
        cflags = "-m32"
    else:
        cflags = ""

    gcc_process = subprocess.Popen(shlex.split("gcc {} -E -".format(cflags)), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    gcc_process.stdin.write(b"#include <sys/syscall.h>\nSYS_%s" % syscall_name.encode())
    stdout, _ = gcc_process.communicate()

    syscall_number_string = stdout.split(b"\n")[-2].decode()

    if not check_sane_integer(syscall_number_string):
        return -1

    return int(syscall_number_string)


def generate_syscalls(syscall_names, bitness):
    syscalls = {}

    for syscall_name in syscall_names:
        syscalls[syscall_name] = get_syscall_number(syscall_name, bitness)

    return OrderedDict(sorted(syscalls.items(), key=itemgetter(1)))


def cache_files_exist():
    return pathlib.Path(CONFIG["cache_file_32bit"]).exists() and pathlib.Path(CONFIG["cache_file_64bit"]).exists()


def check_cache():
    if cache_files_exist():
        syscalls_32bit = json.loads(read_file_content(CONFIG["cache_file_32bit"]))
        syscalls_64bit = json.loads(read_file_content(CONFIG["cache_file_64bit"]))
    else:
        syscall_names = parse_syscall_names()
        syscalls_32bit = generate_syscalls(syscall_names, BITNESS_32)
        syscalls_64bit = generate_syscalls(syscall_names, BITNESS_64)
        write_file_content(CONFIG["cache_file_32bit"], json.dumps(syscalls_32bit))
        write_file_content(CONFIG["cache_file_64bit"], json.dumps(syscalls_64bit))

    return syscalls_32bit, syscalls_64bit


def print_all_syscalls(syscalls):
    for syscall_name, syscall_number in syscalls.items():
        if syscall_number == -1:  # filter out n/a syscall numbers
            continue

        print("{0:3} (0x{0:X}): {1}".format(syscall_number, syscall_name))


def print_single_syscall(syscall_name, syscalls, quiet):
    if syscall_name not in syscalls.keys():
        raise ValueError("The syscall name you provided is not available!")

    if quiet:
        print(syscalls[syscall_name])
    else:
        print("The syscall number for {0} is: {1} (0x{1:X})".format(
            syscall_name,
            syscalls[syscall_name],
        ))


def check_cache_directory():
    directory = "{}/.cache/syscall_number".format(os.environ["HOME"])

    if not pathlib.Path(directory).exists():
        os.mkdir(directory)


def check_syscall_header_file():
    if not pathlib.Path(CONFIG["syscall_header_file"]).exists():
        raise RuntimeError("Install gcc with 32bit support: https://github.com/martinclauss/syscall_number#gcc-with-32bit-support")


def print_man_page_info(syscall_name):
    man_environment_variables = {
        "MANPAGER": "cat",
        "COLUMNS": "80"
    }

    command = "man 2 {}".format(syscall_name)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=man_environment_variables)
    stdout, _ = process.communicate()

    stdout = stdout.decode()
    information_regex = re.compile(r"(NAME(.|\n)+)\n\nDESCRIPTION")

    match = information_regex.search(stdout)

    if match:
        man_text = "\n"
        man_text += match.group(1)
        man_text += "\n\n...for more details run \"{}\"".format(command)
    else:
        man_text = "no man page info available"

    print(man_text)


@click.command()
@click.option("-s", "--syscall-name", "syscall_name", help="The name of the syscall you want the number for.")
@click.option("-b", "--bitness",
              required=True, type=click.Choice([BITNESS_32, BITNESS_64]), help="Bitness, for example, 32 or 64")
@click.option("-a", "--all", "all_syscalls",
              is_flag=True, help="Print the whole system call table for the current machine.")
@click.option("-q", "--quiet", is_flag=True, help="Just output the number in decimal without any additional text.")
@click.option("-m", "--man-page", "man_page", is_flag=True, help="Print a part of the man page for the queried system call.")
def main(syscall_name, bitness, all_syscalls, quiet, man_page):
    try:
        if not check_program("gcc"):
            raise RuntimeError("This script needs gcc to be installed!")

        check_cache_directory()
        check_syscall_header_file()

        syscalls_32bit, syscalls_64bit = check_cache()

        if bitness == BITNESS_32:
            syscalls = syscalls_32bit
        else:
            syscalls = syscalls_64bit

        if all_syscalls:
            print_all_syscalls(syscalls)
        else:
            print_single_syscall(syscall_name, syscalls, quiet)

            if man_page:
                print_man_page_info(syscall_name)

    except (ValueError, RuntimeError) as error:
        print(str(error))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
