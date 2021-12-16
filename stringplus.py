#!/usr/bin/python3
# @author: Nick Cottrell
# @version: 1.0
# @date: 04/21/2020

import argparse
import re
from itertools import product
from sys import stdin
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
from string import punctuation as symbols
from string import digits as digit


class BruteChain:
    """ Bruteforce Chain is an iterative class that provides every permutative
    combo of a given list and length.\n
    @param length the number of bits to the iterator\n
    @param data a list of lists. This is setup so that the iterator can internally
    combine the lists into a bigger, more refined set of characters to permutate\n
    @return an iterator that goes through every possible combination of values given
    in the dataset of given length\n
    \n
    @author Nick Cottrell\n
    @version: 2.1\n
    @date 04/21/2020
    """
    modulus: list = None
    length: int = None
    value: list = None

    def __init__(self, length: int, *data: list):
        self.length = length
        self.modulus = list()
        for dictionary in data:
            self.modulus.extend(dictionary)
        # making sure no non characters exist
        for i in range(len(self.modulus)):
            self.modulus[i] = str(self.modulus[i])
        # pruning list to only be unique values
        self.modulus = list(set(self.modulus))
        self.modulus.sort()
        self.value = [0 for a in range(length)]

    def __iter__(self):
        return self

    def __next__(self) -> str:
        # Check to see if at end
        if (self.value[0] >= len(self.modulus)):
            self.value = [0 for a in range(self.length)]
            raise StopIteration
        # Building current string
        curr: str = str()
        for i in self.value:
            curr += self.modulus[i]
        # Increment chain
        self.value[-1] += 1
        # modulus chain
        for i in range(self.length - 1, 0, -1):
            if (self.value[i] >= len(self.modulus)):
                self.value[i - 1] += 1
                self.value[i] = 0
            else:  # The idea here is that if the current bit doesnt need to be reset
                break  # Then theres no need to continue as nothing else has changed
        # Finished
        return curr

    def __len__(self):
        return len(self.modulus) ** self.length


class BaseChain:
    """ Base Chain is an iterative class that provides every permutative
    combo of a number system up to a given length.\n
    @param base the number thats 1 larger than the largest bit value possible. Allows
    Cheap and easy permutations for octal, binary, decimal, and many others (not hex sadly)\n
    @param length the number of bits to the iterator\n
    @return an iterator that goes through every possible combination of values given
    from the base and the length. the iterator has base^length values in total\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 04/21/2020\n
    """
    base: int = int()
    length: int = int()
    value: int = int()

    def __init__(self, base: int, length: int):
        self.base = base
        self.length = length

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if (self.value >= self.base ** self.length):
            self.value = 0
            raise StopIteration
        self.value += 1
        return self.value - 1

    def __len__(self):
        return self.base ** self.length


class DecimalChain(BaseChain):
    """ Decimal Chain is an iterative class that provides every permutative
    combo of decimal numbers up to a given length.\n
    @param length the number of bits to the iterator\n
    @return an iterator that goes through every possible combination of values given
    from the base and the length. the iterator has 10^length values in total\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 09/09/2021\n
    """

    def __init__(self, length: int):
        super().__init__(10, length)

    def __next__(self) -> str:
        return f"{super().__next__():0{self.length}d}"


class HexadecimalChain(BaseChain):
    """ Hexadecimal Chain is an iterative class that provides every permutative
    combo of hexadecimal numbers up to a given length.\n
    @param length the number of bits to the iterator\n
    @return an iterator that goes through every possible combination of values given
    from the base and the length. the iterator has 16^length values in total\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 09/09/2021\n
    """

    def __init__(self, length: int):
        super().__init__(16, length)

    def __next__(self) -> str:
        return f"{super().__next__():0{self.length}x}"


class OctalChain(BaseChain):
    """ Octal Chain is an iterative class that provides every permutative
    combo of octal numbers up to a given length.\n
    @param length the number of bits to the iterator\n
    @return an iterator that goes through every possible combination of values given
    from the base and the length. the iterator has 8^length values in total\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 09/09/2021\n
    """

    def __init__(self, length: int):
        super().__init__(8, length)

    def __next__(self) -> str:
        return f"{super().__next__():0{self.length}d}"


class BinaryChain(BaseChain):
    """ Binary Chain is an iterative class that provides every permutative
    combo of 1 and 0 up to a given length.\n
    @param length the number of bits to the iterator\n
    @return an iterator that goes through every possible combination of values given
    from the base and the length. the iterator has 2^length values in total\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 09/09/2021\n
    """

    def __init__(self, length: int):
        super().__init__(2, length)

    def __next__(self) -> str:
        return f"{super().__next__():0{self.length}d}"


def init_formatting(format_string: str, Wordlist: [str] = None) -> (str, list):
    """Init Formatting is the function that takes apart the given string and
    converts it into a legal string while also understanding what permutations
    it will need to print every possible string desired.\n
    @param format_string the formatted string that gets dissected and corrected\n
    @param Wordlist a list of custom words inserted from commandline or as additional
    args\n
    @return the function returns a tuple with the first object being the corrected
    string, and the second object being a list containing all iteration generators
    in order of which ones will be needed.\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 04/21/2020\n
    """

    # Checking if formatting uses id
    use_id: bool = True

    # Now properly formatting string
    custom: list = list()
    proper: list = list()
    formatList: list = list()
    # {\d*:[\s\d\w\.\-\_]*\w} # get officially formatted
    # {[\w\d\s]{0,1}\d+\w+} # string for autoGen
    custom = re.findall(
        r'({(?:(\d+)\+)?([\w\d\s]*)(\d+)(\w+)})', format_string)
    proper = re.findall(r'({(\d*):([\s\d\w\.\-\_]*)(\d+)(\w)})', format_string)
    # Args are setup as such: full format, id num, filler char, length, format

    # This regex grabs every format tag in order of appearance
    formatList = re.findall(
        r'((?:{(?:\d+\+)?[\w\d\s]*\d+\w+})|(?:{\d*:[\s\d\w\.\-\_]*\d+\w}))', format_string)

    # determining use of id
    temp: list = custom.copy()
    temp.extend(proper)
    for i in temp:  # use id if no first groups are blank
        use_id *= not i[1] == ""

    # Building generator list
    if not use_id:
        gen_list = [None for a in range(len(custom) + len(proper))]
    else:
        temp_list = set()
        for i in temp:
            temp_list.add(int(i[1]))
        gen_list = [None for a in range(max(temp_list) + 1)]

    dict_box = list()
    if use_id:
        for i in custom:
            dict_box.clear()
            for symbol in list(i[4]):
                if (symbol == "a"):
                    dict_box.append(lowercase)
                elif (symbol == "A"):
                    dict_box.append(uppercase)
                elif (symbol == "d"):
                    dict_box.append(digit)
                elif (symbol == "s"):
                    dict_box.append(symbols)
                elif (symbol == "w" and Wordlist != None):
                    dict_box.append(Wordlist)
            gen_list[int(i[1])] = BruteChain(int(i[3]), *dict_box.copy())
            dict_box.clear()
            # formatting custom formats to pythonic formatting
            format_string = format_string.replace(
                i[0], "{{{0[1]}:{0[2]}{0[3]}s}}".format(i), 1)
            formatList[int(i[1])] = ""

        for i in proper:
            if i[4] == "s":
                continue  # skip strings since they should be custom
            elif (i[4] == "d" or i[4] == "n"):
                gen_list[int(i[1])] = BaseChain(10, int(i[3]))
            elif (i[4] == "x" or i[4] == "X"):
                gen_list[int(i[1])] = BaseChain(16, int(i[3]))
            elif (i[4] == "o"):
                gen_list[int(i[1])] = BaseChain(8, int(i[3]))
            elif (i[4] == "b"):
                gen_list[int(i[1])] = BaseChain(2, int(i[3]))
            formatList[int(i[1])] = ""
    else:
        index: int = int()

        for i in custom:
            dict_box.clear()
            index = formatList.index(i[0])
            for symbol in list(i[4]):
                if (symbol == "a"):
                    dict_box.append(lowercase)
                elif (symbol == "A"):
                    dict_box.append(uppercase)
                elif (symbol == "d"):
                    dict_box.append(digit)
                elif (symbol == "s"):
                    dict_box.append(symbols)
                elif (symbol == "w" and Wordlist != None):
                    dict_box.append(Wordlist)
            gen_list[index] = BruteChain(int(i[3]), *dict_box.copy())
            dict_box.clear()
            # formatting custom formats to pythonic formatting
            format_string = format_string.replace(
                i[0], "{{:{0[2]}{0[3]}s}}".format(i), 1)
            # replace in list incase similar formats exist
            formatList[index] = ""

        for i in proper:
            index = formatList.index(i[0])
            if i[4] == "s":
                continue  # skip strings since they should be custom
            elif (i[4] == "d" or i[4] == "n"):
                gen_list[index] = BaseChain(10, int(i[3]))
            elif (i[4] == "x" or i[4] == "X"):
                gen_list[index] = BaseChain(16, int(i[3]))
            elif (i[4] == "o"):
                gen_list[index] = BaseChain(8, int(i[3]))
            elif (i[4] == "b"):
                gen_list[index] = BaseChain(2, int(i[3]))
            formatList[index] = ""

    return (format_string, gen_list)


def iterative_printer(format_string: str, generators: list, regex: str = ""):
    """Iterative Printer is a function that takes the products from the last function
    and systematically prints out every combination of the desired string.\n
    @param format_string the correct string that will be the basis of the bruteforce combo\n
    @param generators a list of iterators that are used for the format string\n
    @param regex a regex string that can be used to filter through the string combos
    so that the user can only grab their desired strings is the formatted string isnt
    specific enough.\n
    \n
    @author Nick Cottrell\n
    @version: 1.0\n
    @date 04/21/2020\n
    """
    if regex != "":
        reg_filter = re.compile(regex)

        for i in product(*generators):
        if (regex != "" and bool(re.match(reg_filter, format_string.format(*i)))) or regex == "":
                print(format_string.format(*i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This program is a string combination creator. You
        give it a string and place unknowns in python string format using {}.
        For more capabilties with the formatting, look at pythons official
        string documentation for more formatting functionallity.""")

    parser.add_argument(
        "fstring", type=str, metavar="format_string",
        help="The main string that you use for your wildcard bruteforce string")
    parser.add_argument(
        "-r", nargs="?", default="", type=str, metavar="exclusive_regex",
        help="""This arguement takes all the values returned by the program and
        only prints values that perfectly match the regular expression given.""")

    wordlistHeader = parser.add_argument_group(
        "Wordlists", "These commands are for adding entire wordlists to the commandchain")
    wordlistGroup = wordlistHeader.add_mutually_exclusive_group()
    wordlistGroup.add_help = True
    wordlistGroup.add_argument(
        "-w", type=str, nargs=argparse.REMAINDER, metavar="wordlist", default=None,
        help="This is used if you want to iterate with a list of custom words")
    wordlistGroup.add_argument("--wordlist", metavar="wordlists.txt",
                               nargs="?", type=argparse.FileType("r"), default=None, const=stdin, help="Allows you to provide a file instead of adding your words to the end of the program. Separate them with newlines")
    parser.epilog = """
        Description of Formatting
        This script works with official python formatting. For more information on proper python
        formatting, see the official documentation[1].
        This program also works with custom formatting of its own design. This was implemented so
        that iteration using multiple unique character sets was possible.

        Pythonic Formatting
        As stated, this program works with the majority of formatting that can be done in python.
        What this means is that you can input almost any string into the programs formatter that
        will work in a python f-string or string.format function. As such, "{0:4d}" will use the
        first generator to iterate through 4 base 10 digits in the chain. Currently only digit
        based filters work (though they are for the most part the only bits that will make sense)
        but this means that "{2x}" for 2 hex characters will work, as well as "{0:08b}" and "{0:3o}"
        and other formats that can be iterated may be added in the near future.

        Custom Formatting
        An example of a unique character set would be "{4a}", which is a custom combo of an iterator
        of 4 characters long using lowercase letters. {5aAd} is a 5 character long iterator using
        lowercase, uppercase, and number characters for iteration. As of right now, the current custom
        formats available are:

        a: Lowercase Alphabet
        A: Uppercase Alphabet
        d: decimal numbers
        s: Special Characters (!,@,#,$)
        w: Custom Wordlist. This format is only available with the -w argument

        More are on the way, but the custom iterators allow any combonation of each other for more unique
        bruteforcing.

        ID Tags
        in official python formatting, these are the numbers before a colon that tell the format function
        which parameter to use per format tag. Examples such as {0:04d}, which to python says that the first
        argument will go into the format. Custom formats also work with ID Tags, but in a unique way to help
        the program differentiate the two. an example of a custom format with an id is {0+4aA}. This says
        that the first argument is expected to be an iterator of length 4 with uppercase and lowercase letters.
        The advantages of using ID's are two fold: if you have a bruteforce string that you know repeats in
        another portion of the password, then you can call the iterative number twice, meaning less false
        positives and less passwords to generate, which means it runs faster. The other advantage is you can
        prioritize portions of the unknown password. formats with smaller ID's will change value far less often
        than a format with a higher value. This can make life easier as the password list continues to grow in size.

        Links:
        [1] https://docs.python.org/3.4/library/string.html#format-string-syntax

        Authoring:
        This program was built by Nicholas Cottrell (Rad10Logic)
        April 4th, 2020"""

    args = parser.parse_args()
    if (args.wordlist != None):
        if args.w == None:
            args.w = list()
        args.w.extend(args.wordlist.read().split("\n"))
    setup = init_formatting(args.fstring, args.w)
    iterative_printer(*setup, args.r)
