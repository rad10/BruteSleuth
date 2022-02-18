# Contributing

contributing to this tool/library is not only available but actively
encouraged. Anyone who desires to add to this framework need only make a
pull-request and I will look it over and decide if its worth including. Before
adding community additions, some guidelines have to be acknowledged before any
code can be included.

# Rules for developing chains

To anyone who does not know what a chain is, a chain in the context of this
library is an iterator that takes a set of symbols and creates a string of a
given length of every possible combination given those symbols.

For anyone wanting to include additional chains, there are two major rules that
need to be followed before any additions can be included with them. The first
rule is that they have to be iterators. Due to the math of permutations based
on character sets being `base^{length}`, this means that the resulting number
of combinations can be astronomical. Because of this, memory can be a serious
issue since most systems will not have enough ram to hold all the combinations
created by a permutation. To fix this, all chains have to be iters. The next
element in the chain has to be either calculated, or held in a single section of
memory in order to ensure that who ever is producing all the values they desire
do not end up crashing.

The second rule is that any chains added have to be either incredibly common or
they have to be very useful. The idea of making the chains as external classes
rather than being embedded into the tool (because this project is a tool first
and foremost) is so that people can take the classes and make extended classes
for themselves. This ends up being especially helpful for those permutations
that require a specific character set.

# Adding interface languages

An interface language is any formal language that allows for pattern
expression. Examples of these include, RegEx, f-strings, and hashmasks. If you
think theres a particular language that you want to be able to make bruteforce
strings with, you can make an interface. The main rule behind this is that all
interfaces must output the same thing. All interfaces must output a given
string (in this case an f-string because its python), and an ordered list of
chains that can then be utilized to make an iterator for the string itself.
The reason that this is required is for universal compatibility. Since
interpereting the patterns doesnt require nor depend on the generation portion,
it should in no way be able to influence it. This makes compatibility easier,
as well as allow the option for switching between patterns.

# Testing additions

If you are wanting to add new features or new components to the library, what
you'll need to be sure to do is add means to test if that code still works.
This becomes very important for when someone later changes your code down the
line and it no longer functions as it is intended to. Having testing functions
allows me to have anyones changes tested before merging in any new changes. If
any new code is to be included, there should be a well made framework of tests.
If you are unsure on how to add tests or where to start, you can look under the
test directory at the examples that I have placed down for your benefit.

# Contributing your results

If you have added changes that follow these guidelines and you feel that it is
so beneficial that it should be in the main project, throw in a pull request.
From there I will review it, test it, and if I think that it is a worthy
contribution, it will go into code.
