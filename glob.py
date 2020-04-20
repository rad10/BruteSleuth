from sys import argv
import re

test = "test-{0:04}"

lowercase = [chr(a) for a in range(97, 123)] # cheaty way of generating the alphabet
uppercase = [chr(a) for a in range(65, 91)]
digit = [a for a in range(10)]

class BruteChain:
    modulus = []
    length = 0
    value = []

    def __init__(self, length:int, data: list):
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
            else: # The idea here is that if the current bit doesnt need to be reset
                break # Then theres no need to continue as nothing else has changed
        # Finished
        return curr

# Checking if formatting uses id
use_id = bool(re.match(r'({\d*:[\s\d\w\.\-\_]*\w})|({\d+\+[\w\d\s]{0,1}\d+\w+})'))


# Now properly formatting string
custom = []
proper = []
# {\d*:[\s\d\w\.\-\_]*\w} # get officially formatted
# {[\w\d\s]{0,1}\d+\w+} # string for autoGen

for select in re.findall(r'{[\d+\+]{0,1}[\w\d\s]{0,1}\d+\w+}', test):
    custom.append(select[0])


for select in re.findall(r'{\d*:[\s\d\w\.\-\_]*\w}', test):
    proper.append(select[0])


# Building generator list
if not use_id:
    gen_list = [None for a in range(len(custom) + len(proper))]
else:
    # This regex basically selects only the numbers at "{1:" or "{1+" for preprocessing
    temp = []
    for pos in re.findall(r'(?<={)\d+(?=(:[\s\d\w\.\-\_]*\w})|(\+[\w\d\s]{0,1}\d+\w+}))', test):
        temp.append(int(pos[0]))
    gen_list = [None for a in range(max(temp))]

# if there are id's, then sort out formal id's first
if use_id:
    for i in custom:
        index, formatting = i.split("+")
        dict_box = []
        