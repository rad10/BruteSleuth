# BruteSleuth

[![GitHub Version](https://img.shields.io/github/v/release/rad10/BruteSleuth)](https://github.com/rad10/BruteSleuth/releases)
[![PyPI](https://img.shields.io/pypi/v/BruteSleuth?style=flat)](https://pypi.org/project/BruteSleuth/)
[![GPL3 License](https://img.shields.io/github/license/rad10/BruteSleuth?style=flat)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![Package build status](https://img.shields.io/github/workflow/status/rad10/BruteSleuth/Python%20package?logo=GitHub)](https://github.com/rad10/BruteSleuth/actions/workflows/python-package.yml)

This program uses string formatting to give a list of strings related to an original string based off regex

## Table of Contents

 * [How to install BruteSleuth](#how-to-install-brutesleuth)
    * [Pip](#pip)
    * [Debian](#debian)
    * [RHEL](#rhel)
    * [Arch](#arch)
    * [Source](#source)
 * [What is BruteSleuth](#what-is-brutesleuth)
 * [Why use BruteSleuth](#why-use-brutesleuth)
 * [Contributing](#contributing)
 * [Links](#links)
 * [Authoring](#authoring)


## How to install BruteSleuth

With the way that the project is set up, there are multiple ways to install
BruteSleuth. The main way to install it is through pip, but it can be installed
on Debian, Arch, and RHEL.

### Pip

to install the project from anywhere, the command is simply:

```bash
python -m pip install BruteSleuth
```

or

```bash
pip install BruteSleuth
```

If you are deciding to use the manual wheel from the releases page, you can
always install it directly with pip as well

```bash
pip install ./BruteSleuth-1.4.0-py3-none-any.whl
```

### Debian

In the releases, there should be a `.deb` file for debian users. It is not
bound to any particular distro. The only special difference with it is that it
requires the OS to recognize a version of Python 3, which most Distro's already
have installed. You can install the deb file with either of these two commands.

```bash
sudo apt install ./python3-brutesleuth_1.4.0-1_all.deb
```

or with

```bash
sudo dpkg -i python3-brutesleuth_1.4.0-1_all.deb
```

### RHEL

For you fedora/RHEL users, I also provided an RPM file that can be used with
dnf. You can install it with:

```bash
sudo rpm -i BruteSleuth-1.4.0-1.noarch.rpm
```
or

```bash
sudo dnf localinstall BruteSleuth-1.4.0-1.noarch.rpm
```

or

```bash
sudo yum localinstall BruteSleuth-1.4.0-1.noarch.rpm
```

### Arch

I include a `PKGBUILD` file in the root of the repo that can be used to install
the package (written by me, so you know that the source is trustworthy.) To
install the package, either clone the repo or just download the `PKGBUILD` file
then run the usual commands that you would to install the package.

```bash
makepkg -si
```

Or if you don't want to build it yourself (which I get), I also include a
`.pkg.tar.zst` file that you can use directly with pacman.

```bash
pacman -U python-brutesleuth-git-1.4.0.r0.?-1-any.pkg.tar.zst
```

### Source

For those of you wanting to be a little bit adventurous out there or want to
directly install a modified version of this library, you can easily directly
install the package by going into the cloned folder and running:

```bash
python setup.py install
```

## What is BruteSleuth

BruteSleuth is a smart Bruteforce engine. What this means is that it can take
a pattern string and output **every** combination that fits within that
pattern into a wordlist. There are tools that can make every permutation of a
character for a given length to be used in a wordlist, but what makes
BruteSleuth smarter is that you as the user can decide what positions a
character can be and what spots are constants. This means that the number of
words that will be used for your wordlist go down the more information that
you know, making it a smart Bruteforcer.

## Why use BruteSleuth

Story time:
I first created this tool to be used in the National Cyber League
([NCL](https://nationalcyberleague.org/)) to be used in one of their Capture
The Flags (CTFs). I specifically made this tool for the hash cracking
section. One of the sections is always to find the flag that the hash
represents. The flag would always be SKY, 4 letters, then 4 digits as such:
`SKY-KVjW-1830`, but then there was another section where all the hashes
were a developers name, an animal, then 2 digits. I could make a wordlist by
making a python script that generates each combination. The SKY flags would
require at least 2 nested for loops to get every combo, and the developer
hashes would require at least 3 nested for loops. Plus the script wasnt easily
modifiable to go from one to the other. After doing to many hash cracking
challenges where I have to make a new python script to make my wordlist, I
started to get fed up with it and decided that I would make a python script to
[rule them all](https://static0.gamerantimages.com/wordpress/wp-content/uploads/2021/08/Lord-of-the-Rings-Eye-of-Sauron-Mordor-1.jpg).
Since then, I have been using this script to make all of my custom wordlists.
[/story]

Why would you want to use BruteSleuth? Because making a custom python script
every time that you have a unique wordlist is obnoxious. Why do that when you
could use this tool to do all the forloops for you in the background. If you
understand how f-strings work, then you can make any custom wordlist that your
heart desires. You can even use full words in your combinations if you wanted.

For those of you who are looking at this and asking: How is this better than
hash masks? For those who do not know, some BruteForce tools, such as
[John the Ripper](https://www.openwall.com/john/doc/RULES.shtml) and
[Hashcat](https://hashcat.net/wiki/doku.php?id=mask_attack) both provide a
ruleset to make smart patterns for BruteForcing. The way that this tool is
better than these options is that it isn't. Even if the pattern ruleset is far
superior to hashcat or johns, nothing will beat the unison. When hashcat uses
a mask, the mask gets directly turned into a hash and compared. With this tool,
you would have to first output the wordlist to a file (which could go into the
GB in size), then use that file as input for hashcat. For memory and storage
sake, hashcat/john is 100% the way to go, but there is still a good reason to
use this tool for bruteforcing. There are far more bruteforcing tools besides
hashcat and john, and most do not support a masking feature. Bruteforcing tools
such as Medusa, Ncrack, aircrack-ng, and hydra (kinda) do not have a way to
make a passwordlist based off a pattern or a hash mask. Since there will always
be tools like these that will only accept a file with password lines on each
line, it is a solid option to be able to convert your mask consistently to a
wordlist that can be used by **any** tool that is designed for some form of
bruteforcing. In addition to this, BruteSleuth can even take a pattern string
and convert it into a hash mask for you in case you dont know how to program
one yourself (though it is 100% worth it to learn).

Another reason to use this tool for those masochistic enough to still want a
python script for their wordlist generation is that all the major functions
used in making any permutation wordlist can be used in your own scripts. I
heavily document every function that I write (seriously, roughly 2/3 of every
file is comments or doc strings). These include everything from the custom
classes used to permutate combinations, to a proper iter_product function that
properly products every iter without using all the memory (itertools, eat your
heart out), to the functions that convert a pattern string into an iter class
with every password available. All that and more by simply adding this to your
project:

```python
import brutesleuth
```

## Contributing

see [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## Links
[1] https://docs.python.org/3.4/library/string.html#format-string-syntax

## Authoring
This program was built by Nicholas Cottrell (Rad10Logic)
April 4th, 2020
