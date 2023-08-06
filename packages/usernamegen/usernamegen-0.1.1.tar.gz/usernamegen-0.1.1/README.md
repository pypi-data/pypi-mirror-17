# usernamegen
> Genrate usernames with a Markov chain based on a wordlist

[![Build Status](https://travis-ci.org/stylesuxx/usernamegen.svg?branch=master)](https://travis-ci.org/stylesuxx/usernamegen) [![Downloads](https://img.shields.io/pypi/dm/browserinfo.svg)](https://img.shields.io/pypi/dm/usernamegen.svg) [![Documentation Status](https://readthedocs.org/projects/usernamegen/badge/?version=latest)](http://sync.readthedocs.io/?badge=latest)

## Wordlist
In order to get the most out of the word generation, make sure that you have one word per line, all lower case.

## Installation
Simply install via pip:

    pip install usernamegen

## Usage
### Library
You can use the usernamegen directly in your python application.
```bash
>>> import usernamegen
>>> words = ['foo', 'foobar', 'foobarbla', 'foobarblafasel']
>>> formatters = [{'format': usernamegen.Formatter.Join, 'weight': 1}]
>>> minLength = 8
>>> size = 3
>>> gen = usernamegen.Generator(words, size, minLength)
>>> gen.setFormatters(formatters)
>>> gen.getString()
'foobarfoobarblafasel'
```

When multiple formmatters are used, the heigher the weight of a formatter the more likely it is, that it is used.

The following formatters are available:

* Join
* Underscore
* Capitalize
* CapitalizeExceptFirst
* AppendNumber
* CapitalizeAppendNumber

### Scripts
After installation there will be two script available:

#### markov
```bash
usage: markov [-h] [-p PREV] [-n N] WORDLIST

Markov chain word generator. Generate new words based on aword list.

positional arguments:
  WORDLIST    Path to wordlist used for word generation

optional arguments:
  -h, --help  show this help message and exit
  -p PREV     Number of previous letters to base chain on
  -n N        Amount of new words to generate
```

#### username
```bash
usage: username [-h] [-p PREV] [-n N] [-m MIN] WORDLIST

Generate usernames based on a wordlist and a Markov chain.

positional arguments:
  WORDLIST    Path to wordlist used for word generation

optional arguments:
  -h, --help  show this help message and exit
  -p PREV     Number of previous letters to base chain on
  -n N        Amount of new words to generate
  -m MIN      Minimum username length
```

## Running tests
```bash
nosetests --with-coverage --cover-package=usernamegen --with-json-extended
```

## Generating Documentation
```bash
sphinx-apidoc -o docs/source usernamegen -f
cd docs && make html && cd ..
```
