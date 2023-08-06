# Geeklish: Learn English by Coding

[![PyPI version](https://badge.fury.io/py/geeklish.svg)](https://badge.fury.io/py/geeklish)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/fchollet/keras/blob/master/LICENSE)

Geeklish is a library that lets you create English sentences by writing code.

Read the documentation at [kenzotakahashi.github.io/geeklish/](https://kenzotakahashi.github.io/geeklish/).

```python
from geeklish.clause import Clause
from geeklish.adverb import Adverb
from geeklish.noun import Pronoun, Noun
from geeklish.verb import Verb
from geeklish.others import sentence

c = Clause()

he = Pronoun('he')
dog = Noun('dog', number='plural')
like = Verb('like')
really = Adverb('really')

c.take_subject(he)
c.take_verb(like)

like.take_complement(dog)
like.take_adverb(really)

print(sentence(c)) # He really likes dogs.
```

## Installation

You can install Geeklish from PyPI:
```sh
pip install geeklish
```

Geeklish supports Python 2.7, 3.3, 3.4 and 3.5.
