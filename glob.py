import argparse
import re
from itertools import product

test = "test-{0:04}"

# cheaty way of generating the alphabet
lowercase = [chr(a) for a in range(97, 123)]
uppercase = [chr(a) for a in range(65, 91)]
digit = [a for a in range(10)]


class BruteChain:
    modulus = []
    length = 0
    value = []

    def __init__(self, length: int, data: list):
        self.length = length
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

    def __next__(self):
        # Check to see if at end
        if (self.value[0] >= len(self.modulus)):
            self.value = [0 for a in range(self.length)]
            raise StopIteration
        # Building current string
        curr = ""
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


class BaseChain:
    base = int()
    length = int()
    value = int()

    def __init__(self, base: int, length: int):
        self.base = base
        self.length = length

    def __iter__(self):
        return self

    def __next__(self):
        if (self.value >= self.base ** self.length):
            self.value = 0
            raise StopIteration
        self.value += 1
        return self.value - 1


def init_formatting(test: str):
    # Checking if formatting uses id
    use_id = True

    # Now properly formatting string
    custom = list()
    proper = list()
    formatList = list()
    # {\d*:[\s\d\w\.\-\_]*\w} # get officially formatted
    # {[\w\d\s]{0,1}\d+\w+} # string for autoGen
    custom = re.findall(r'({(?:(\d+)\+)?([\w\d\s]*)(\d+)(\w+)})', test)
    proper = re.findall(r'({(\d*):([\s\d\w\.\-\_]*)(\d+)(\w)})', test)
    # Args are setup as such: full format, id num, filler char, length, format

    # This regex grabs every format tag in order of appearance
    formatList = re.findall(
        r'((?:{(?:\d+\+)?[\w\d\s]*\d+\w+})|(?:{\d*:[\s\d\w\.\-\_]*\d+\w}))', test)

    # determining use of id
    temp = custom.copy()
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
            gen_list[int(i[1])] = BruteChain(int(i[3]), dict_box.copy())
            dict_box.clear()
            # formatting custom formats to pythonic formatting
            test = test.replace(i[0], "{{{0[1]}:{0[2]}{0[3]}s}}".format(i), 1)
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
        index = int()

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
            gen_list[index] = BruteChain(int(i[3]), dict_box.copy())
            dict_box.clear()
            # formatting custom formats to pythonic formatting
            test = test.replace(i[0], "{{:{0[2]}{0[3]}s}}".format(i), 1)
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

    return (test, gen_list)


def iterative_printer(format_string: str, generators: list, regex: str = ""):
    if regex == "":
        for i in product(*generators):
            print(format_string.format(*i))
    else:
        reg_filter = re.compile(regex)
        for i in product(*generators):
            if bool(re.match(reg_filter, format_string.format(*i))):
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

    parser.epilog = """
        Description of Formatting
        This script works with official python formatting. For more information on proper python
        formatting, see the official documentation[1].
        This program also works with custom formatting of its own design. This was implemented so
        that iteration using multiple unique character sets was possible.

        Custom Formatting
        An example of a unique character set would be "{4a}", which is a custom combo of an iterator
        of 4 characters long using lowercase letters. {5aAd} is a 5 character long iterator using
        lowercase, uppercase, and number characters for iteration. As of right now, the current custom
        formats available are:
        
        a: Lowercase Alphabet
        A: Uppercase Alphabet
        d: decimal numbers
        
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
        [1] https://docs.python.org/3.4/library/string.html#format-string-syntax\n
        
        Authoring:
        This program was built by Nicholas Cottrell (Rad10Logic)
        April 4th, 2020"""

    args = parser.parse_args()
    setup = init_formatting(args.fstring)
    iterative_printer(*setup, args.r)
