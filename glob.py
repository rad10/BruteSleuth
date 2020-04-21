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


# Checking if formatting uses id
use_id = True


# Now properly formatting string
custom = list()
proper = list()
# {\d*:[\s\d\w\.\-\_]*\w} # get officially formatted
# {[\w\d\s]{0,1}\d+\w+} # string for autoGen

custom = re.findall(r'{(?:(\d+)\+)?([\w\d\s]?\d+)(\w+)}', test)
proper = re.findall(r'{(\d*):([\s\d\w\.\-\_]*\d)(\w)}', test)

# determining use of id
temp = custom
temp.extend(proper)
for i in temp:  # use id if no first groups are blank
    use_id *= not i[0] == ""

# Building generator list
if not use_id:
    gen_list = [None for a in range(len(custom) + len(proper))]
else:
    temp_list = set()
    for i in temp:
        temp_list.add(int(i[0]))
    gen_list = [None for a in range(max(temp))]

dict_box = list()
if use_id:
    for i in custom:
        dict_box.clear()
        for symbol in i[2].split():
            if (symbol == "a"):
                dict_box.append(lowercase)
            elif (symbol == "A"):
                dict_box.append(uppercase)
            elif (symbol == "d"):
                dict_box.append(digit)
        gen_list[i[0]] = BruteChain(i[1], dict_box.copy())
        dict_box.clear()