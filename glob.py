from sys import argv
import re

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
formatList = re.findall(r'((?:{(?:\d+\+)?[\w\d\s]*\d+\w+})|(?:{\d*:[\s\d\w\.\-\_]*\d+\w}))')

# determining use of id
temp = custom
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
    gen_list = [None for a in range(max(temp))]

dict_box = list()
if use_id:
    for i in custom:
        dict_box.clear()
        for symbol in i[4].split():
            if (symbol == "a"):
                dict_box.append(lowercase)
            elif (symbol == "A"):
                dict_box.append(uppercase)
            elif (symbol == "d"):
                dict_box.append(digit)
        gen_list[i[1]] = BruteChain(int(i[3]), dict_box.copy())
        dict_box.clear()
        # formatting custom formats to pythonic formatting
        test.replace(i[0], "{{{0[0]}:{0[1]}{0[2]}s}}".format(i))

    for i in proper:
        if i[4] == "s":
            continue  # skip strings since they should be custom
        elif (i[4] == "d" or i[4] == "n"):
            gen_list[i[1]] = BaseChain(10, int(i[3]))
        elif (i[4] == "x" or i[4] == "X"):
            gen_list[i[1]] = BaseChain(16, int(i[3]))
        elif (i[4] == "o"):
            gen_list[i[1]] = BaseChain(8, int(i[3]))
        elif (i[4] == "b"):
            gen_list[i[1]] = BaseChain(2, int(i[3]))
else:
    index = int()

    for i in custom:
        dict_box.clear()
        index = formatList.index(i[0])
        for symbol in i[4].split():
            if (symbol == "a"):
                dict_box.append(lowercase)
            elif (symbol == "A"):
                dict_box.append(uppercase)
            elif (symbol == "d"):
                dict_box.append(digit)
        gen_list[index] = BruteChain(int(i[3]), dict_box.copy())
        dict_box.clear()
        # formatting custom formats to pythonic formatting
        test = test.replace(i[0], "{{:{0[1]}{0[2]}s}}".format(i), 1)
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