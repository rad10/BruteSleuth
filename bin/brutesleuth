#!/usr/bin/python3
# @author: Nick Cottrell
# @version: 1.0
# @date: 04/21/2020

import argparse
from sys import stdin
import re
from brutesleuth import convert_to_mask, init_formatting, print_random
from brutesleuth import set_position, BruteListChain

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This program is a string combination creator. You
        give it a string and place unknowns in python string format using {}.
        For more capabilties with the formatting, look at pythons official
        string documentation for more formatting functionallity.""")

    parser.add_argument(
        "fstring", type=str, metavar="format_string", help="The main string \
            that you use for your wildcard bruteforce string")

    parser.add_argument(
        "-r", nargs="?", default="", type=str, metavar="exclusive_regex",
        help="This arguement takes all the values returned by the program and \
        only prints values that perfectly match the regular expression given.")

    parser.add_argument(
        "-l", "--limit", type=int, metavar="limitNum", default=None,
        help="Add a limit to the number of passwords printed out. Will only \
            print up to X passwords.")

    parser.add_argument(
        "-s", default=None, type=str, nargs="?", metavar="start_value",
        help="Set where the password generator starts rather than its initial \
            position")
    parser.add_argument(
        "--random", action="store_true", help="Creates a random password \
            based on the rulseset given. This can be useful for randomly \
            guessing passwords beforehand or for generating a random password \
            itself. Can be used with -l to generate multiple random passwords")

    wordlistHeader = parser.add_argument_group(
        title="Wordlists", description="These commands are for adding entire \
wordlists to the commandchain")
    wordlistGroup = wordlistHeader.add_mutually_exclusive_group()
    wordlistGroup.add_help = True
    wordlistGroup.add_argument(
        "-w", type=str, nargs=argparse.REMAINDER, metavar="wordlist",
        default=None, help="This is used if you want to iterate with a list \
            of custom words")
    wordlistGroup.add_argument(
        "--wordlist", metavar="wordlists.txt", nargs="?",
        type=argparse.FileType("r"), default=None, const=stdin, help="Allows \
            you to provide a file instead of adding your words to the end of \
            the program. Separate them with newlines")

    maskHeader = parser.add_argument_group(
        title="Masks", description="These commands change the program \
entirely. Instead of generating every instance of a password based on an \
fstring, it creates a mask used by many hash cracking programs to make them \
generate every possible change. This can be extremely useful, especially if \
haveing to consider memory/storage constraints with larger password groups.")
    maskHeader.add_argument(
        "--mask", action="store_true", help="Makes a mask based on the \
            fstring given. All characters that work with the default mode \
            will work with the mask given. The default is a universal mask \
            that works with both John and Hashcat.")
    parser.epilog = """
Description of Formatting:
    This script works with official python formatting. For more information on
    proper python formatting, see the official documentation[1]. This program
    also works with custom formatting of its own design. This was implemented
    so that iteration using multiple unique character sets would be possible.

Pythonic Formatting:
    As stated, this program works with the majority of formatting that can be
    done in python. What this means is that you can input almost any string
    into the programs formatter that will work in a python f-string or
    string.format function. As such, "{0:4d}" will use the first generator to
    iterate through 4 base 10 digits in the chain. Currently only digit based
    filters work (though they are for the most part the only bits that will
    make sense) but this means that "{2x}" for 2 hex characters will work, as
    well as "{0:08b}" and "{0:3o}" and other formats that can be iterated may
    be added in the near future.

Custom Formatting:
    An example of a unique character set would be "{4a}", which is a custom
    combo of an iterator of 4 characters long using lowercase letters. {5aAd}
    is a 5 character long iterator using lowercase, uppercase, and number
    characters for iteration. As of right now, the current custom formats
    available are:

    a: Lowercase Alphabet
    A: Uppercase Alphabet
    d: decimal numbers
    s: Special Characters (!,@,#,$)
    w: Custom Wordlist. This format is only available with the -w argument

    More are on the way, but the custom iterators allow any combination of each
    other for more unique bruteforcing.

ID Tags:
    in official python formatting, these are the numbers before a colon that
    tell the format function which parameter to use per format tag. Examples
    such as {0:04d}, which to python says that the first argument will go into
    the format. Custom formats also work with ID Tags, but in a unique way to
    help the program differentiate the two. an example of a custom format with
    an id is {0+4aA}. This says that the first argument is expected to be an
    iterator of length 4 with uppercase and lowercase letters. The advantages
    of using ID's are two fold: if you have a bruteforce string that you know
    repeats in another portion of the password, then you can call the iterative
    number twice, meaning less false positives and less passwords to generate,
    which means it runs faster. The other advantage is you can prioritize
    portions of the unknown password. formats with smaller ID's will change
    value far less often than a format with a higher value. This can make life
    easier as the password list continues to grow in size.

Links:
    [1] https://docs.python.org/3.4/library/string.html#format-string-syntax

Authoring:
    This program was built by Nicholas Cottrell (Rad10Logic)
    April 4th, 2020"""

    args = parser.parse_args()

    # Checking if wanting a mask instead
    if args.mask:
        print(convert_to_mask(args.fstring))
        exit()

    if args.wordlist:
        if not args.w:
            args.w = list()
        args.w.extend(args.wordlist.read().split("\n"))
    format_string, generators = init_formatting(args.fstring, args.w)

    # Checking if random
    if args.random:
        # checking if wanting to make multiple random passwords
        if args.limit:
            for i in range(args.limit):
                print(print_random(format_string, generators))
        else:
            print(print_random(format_string, generators))
        exit()
    if args.s:
        generators = set_position(format_string, args.s, generators)

    if args.r:
        reg_filter = re.compile(args.r)
    if args.limit:
        count = 0

    for line in BruteListChain(format_string, generators):
        if (args.r and bool(re.match(reg_filter, line))) or args.r == "":
            print(line)
            if args.limit:
                if count < args.limit:
                    count += 1
                if count >= args.limit:
                    break
