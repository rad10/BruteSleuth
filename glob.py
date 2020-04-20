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


# Now properly formatting string
temp = re.findall(r'{((\d+:)?\d+\w+)}', test)
formats = list(str(temp))
gen_list = [None for a in range(len(formats))]

for i in range(len(gen_list)):
    if formats[i].find(":") != -1:
        j, mod = formats[i].split(":")
        if j.isdecimal() or j.isdigit():
            i = int(j)

        # grabbing length of format
        for j in range(len(mod)):
            if not mod[j].isdigit():
                mod = mod[:j] + mod[j + 1:]