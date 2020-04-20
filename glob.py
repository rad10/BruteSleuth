from sys import argv

mainString = "test-{0:04}"


class LowerAlphaChain:
    length = 0
    chr_array = []

    def __init__(self, length: int):
        self.length = length
        self.chr_array = ["a" for a in range(length)]

    def __iter__(self):
        return self

    def __next__(self):
        if (self.chr_array[0] == "{"):
            self.chr_array = ["a" for a in range(self.length)]
            raise StopIteration

        curr = "".join(self.chr_array)

        # increment last char
        self.chr_array[-1] = chr(ord(self.chr_array[-1]) + 1)

        # incrementing modulus chars
        for i in range(len(self.chr_array) - 1, 0, -1):
            if (self.chr_array[i] == "{"):
                self.chr_array[i] = "a"
                self.chr_array[i - 1] = chr(ord(self.chr_array[i - 1]) + 1)
            else:     # I can break because if the current bit doesnt overflow,
                break # then that means the next bits have no chance of overflowing
        return curr   # So I can skip all of them


class UpperAlphaChain:
    length = 0
    chr_array = []

    def __init__(self, length: int):
        self.length = length
        self.chr_array = ["A" for a in range(length)]

    def __iter__(self):
        return self

    def __next__(self):
        if(self.chr_array[0] == "["):
            self.chr_array = ["A" for a in range(self.length)]
            raise StopIteration

        curr = "".join(self.chr_array)

        # increment last character
        self.chr_array[-1] = chr(ord(self.chr_array[-1]) + 1)
        #incrementing all characters if need be
        for i in range(len(self.chr_array) - 1, 0, -1):
            if(self.chr_array[i] == "["):
                self.chr_array[i - 1] = chr(ord(self.chr_array[i - 1]) + 1)
                self.chr_array[i] = "A"
            else:
                break
        return curr