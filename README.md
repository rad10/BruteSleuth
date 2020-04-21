# StringPlus
This program uses string formatting to give a list of strings related to an original string based off regex

## Description of Formatting
This script works with official python formatting. For more information on proper python
formatting, see the official documentation[1].

This program also works with custom formatting of its own design. This was implemented so
that iteration using multiple unique character sets was possible.

## Custom Formatting
An example of a unique character set would be "{4a}", which is a custom combo of an iterator
of 4 characters long using lowercase letters. {5aAd} is a 5 character long iterator using
lowercase, uppercase, and number characters for iteration. As of right now, the current custom
formats available are:

> a: Lowercase Alphabet
> A: Uppercase Alphabet
> d: decimal numbers

More are on the way, but the custom iterators allow any combonation of each other for more unique
bruteforcing.

## ID Tags
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

## Links:
[1] https://docs.python.org/3.4/library/string.html#format-string-syntax

## Authoring:
This program was built by Nicholas Cottrell (Rad10Logic)
April 4th, 2020