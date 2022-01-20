import re
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
from string import punctuation as symbols
from string import digits as digit
from math import prod
from random import randrange


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

    def setIndex(self, value: str) -> None:
        """Set the value that the iterator is currently at. Will raise exceptions if
        input isnt long enough or contains characters not within the dictionary
        """
        # Check that values are correct length
        if len(value) != len(self.value):
            raise IndexError
        # Check that values within values are contained within dictionary
        for char in value:
            if char not in self.modulus:
                raise ValueError

        # setting values from given value
        for i in range(len(value)):
            self.value[i] = self.modulus.index(value[i])

    def getRandom(self) -> str:
        """Returns a random configuration of the brutechain. This can be useful if used to
        implement a monkey sort brute forcer, or to create a random password based on rulesets
        """
        # Creating random values in memory
        randomMemory = [randrange(
            0, len(self.modulus)) for a in self.value]
        # building string
        curr: str = str()
        for i in randomMemory:
            curr += self.modulus[i]
        return curr


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

    def setIndex(self, value: int) -> None:
        """Set the value that the iterator is currently at. Will raise exceptions if
        input is larger than the iterators length
        """
        # Checking if value is past length
        if value >= self.__len__():
            raise IndexError

        # set the value. Easy peasy
        self.value = value

    def getRandom(self) -> int:
        """Returns a random configuration of the basechain. This can be useful if used to
        implement a monkey sort brute forcer, or to create a random password based on rulesets
        """
        # Creating random values in memory
        return randrange(0, self.__len__())


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


class iterative_product:
    """creates an iterator of a list of all the iterators added into itself.
    Functions the exact same way as itertools.product, but it properly creates
    and iterator that does not consume large amounts of memory regardless of
    its size.
    """

    def __init__(self, *iterators) -> None:
        self.hold = iterators
        self.memory = [a.__next__() for a in iterators]
        self.firstRun = True

    def __len__(self) -> int:
        return prod(map(len, self.hold))

    def __iter__(self):
        if len(self.hold) == 0:
            return
        else:
            return self

    def __next__(self) -> tuple:
        # checking if its the first time being run
        if self.firstRun:
            self.firstRun = False
            return tuple(self.memory)

        index = len(self.hold) - 1
        nudgeStep = True

        while nudgeStep and index >= 0:
            try:
                self.memory[index] = self.hold[index].__next__()
                nudgeStep = False
            except StopIteration:
                # if reached the end, reset current step to first bit then nudge
                self.memory[index] = self.hold[index].__next__()
                index -= 1
                nudgeStep = True

        # if the index is -1, the last nudge as gone full circle, ending all possible permutations
        if index == -1:
            raise StopIteration

        return tuple(self.memory)


class BruteListChain(iterative_product):
    """Creates an iterator class that will print out every combinations given
    into it.
    @param format_string The f-string used to be the template
    @param generators a list of iterators that aure used to collect every
    permutation possible.
    """

    def __init__(self, format_string: str, generators: list) -> None:
        self.format_string = format_string
        super().__init__(*generators)

    def __next__(self) -> str:
        return self.format_string.format(*super().__next__())


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


def convert_to_mask(format_string: str, mode: str = "universal") -> str:
    """Takes ruleset given in the form of an f-string and creates a mask that can be utilized
    by hash crackers such as hashcat or john the ripper.\n
    @param format_string the python formatting string used to created given variations\n
    @param mode modifies the output of the mask given. The options are "universal", "hashcat".
    and "john". Each mode will output a mask most preferrable to the specified hash cracker.
    "universal" will instead make a mask that works for any/all hash crackers listed.\n
    @returns a string containing custom charactersets (if any) first spearated by commas, then
    the actual mask at the end. This output can be placed directly into a mask file or have the
    custom character-sets separated and have the mask be directly run by the commandline.\n
    \n
    @author Nick Cottrell\n
    @version: 1.3.5\n
    @date 12/17/2021\n
    """
    # start by getting generators and their settings
    gens = re.findall(r"(\{\d*[:+]?(\d+)(\w+)\})", format_string)

    # charsets that already exist by default
    default_charsets: dict = {
        "d": "?d",
        "a": "?l",
        "A": "?u",
        "s": "?s",
        "w": "?w"
    }
    default_custom_charsets: dict = {
        "b": "01",
        "o": "012345678",
        "x": "?dabcdefABCDEF"
    }
    custom_charsets: [tuple] = list()

    # getting charsets utilized
    gen_chars = set(map(lambda x: x[2], gens))
    # filtering out default charsets to get custom ones utilized
    gen_chars = gen_chars.difference(default_charsets.keys())

    # creating charsets based on what remains
    temp_set = str()
    for custom_set in gen_chars:
        # iterating through dictionaries
        for gen_label, charset in list(default_custom_charsets.items()) + list(default_charsets.items()):
            if gen_label in custom_set and charset not in temp_set:
                temp_set += charset
        # fully built charset, now adding to custom sets
        custom_charsets.append((custom_set, temp_set))
        # resetting tempset
        temp_set = str()

    # custom charsets built, now to replace all gens with masks
    for tag, size, charset in map(lambda x: (x[0], int(x[1]), x[2]), gens):
        # Checking if the charset within the tag is a default set
        if charset in default_charsets:
            format_string = format_string.replace(
                tag, size * default_charsets[charset])
        # Otherwise, check if the tag is in a custom charset and replace according to that
        elif charset in map(lambda x: x[0], custom_charsets):
            # doing for loop because it seems like the easiest way to get specific set
            # without potential error
            for custom_set in filter(lambda x: x[0] == charset, custom_charsets):
                format_string = format_string.replace(
                    tag, size * f"?{custom_charsets.index(custom_set) + 1}")

    # new string complete, setting up custom charsets
    return ",".join(list(map(lambda x: x[1], custom_charsets)) + [format_string])


def get_string_variations(format_string: str, string: str) -> tuple:
    """Gets the varying values from within a password
    @param format_string the python formatting string used to created given variations
    @param string the string to collect varying values.
    """
    # start by making a regex string based on python formatting
    regex_string = re.sub(r"\{\:(\d*)\w\}", r"(.{\1})", format_string)
    return re.findall(regex_string, string)[0]


def set_position(format_string: str, starting_string: str, generators: list) -> list:
    """Sets the position of the password to the given value.
    """
    # Collecting variations between generators
    values = get_string_variations(format_string, starting_string)

    # setting each portion
    for i in range(len(generators)):
        if type(generators[i]) == BruteChain:
            generators[i].setIndex(values[i])
        else:
            generators[i].setIndex(int(values[i]))

    return generators


def print_random(format_string: str, generators: list) -> str:
    """Prints a random configuration of the password ruleset given.\n
    @param format_string the correct string that will be the basis of the bruteforce combo\n
    @param generators a list of iterators that are used for the format string\n
    \n
    @author Nick Cottrell\n
    @version: 1.3.1\n
    @date 12/17/2021\n
    """
    # getting a mapping of all generators running random function
    results = tuple(map(lambda x: x.getRandom(), generators))
    return format_string.format(*results)


def iterative_printer(format_string: str, generators: list, regex: str = "", limit: int = None):
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
    if limit:
        count = 0

    for i in iterative_product(*generators):
        if (regex != "" and bool(re.match(reg_filter, format_string.format(*i)))) or regex == "":
            print(format_string.format(*i))
            if limit:
                if count < limit:
                    count += 1
                if count >= limit:
                    return