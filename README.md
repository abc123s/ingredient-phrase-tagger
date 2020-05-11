# CS 230 Final Project Baseline
Simple baseline model for structured data extraction from recipe ingredient lists.

# CRF Ingredient Phrase Tagger

[![Build Status](https://travis-ci.org/mtlynch/ingredient-phrase-tagger.svg?branch=master)](https://travis-ci.org/mtlynch/ingredient-phrase-tagger) [![Docker Pulls](https://img.shields.io/docker/pulls/mtlynch/ingredient-phrase-tagger.svg?maxAge=604800)](https://hub.docker.com/r/mtlynch/ingredient-phrase-tagger/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.md)

## Fork Notes

This is a fork of the original [NY Times ingredient-phrase-tagger](https://github.com/NYTimes/ingredient-phrase-tagger). This fork is maintained by [Michael Lynch](https://github.com/mtlynch)

This fork maintains the design of the original ingredient-phrase-tagger, but adds bugfixes and additional features to aid in future development:

* Adds a [Docker image](https://hub.docker.com/r/mtlynch/ingredient-phrase-tagger/) for easy deployment.
* Adds a [continuous integration build](https://travis-ci.org/mtlynch/ingredient-phrase-tagger) on every check-in.
* Adds unit tests.
* Adds end-to-end tests.
* Enforces rules for source formatting and linting.

These improvements were described in a series of blog posts on [mtlynch.io](https://mtlynch.io):

* [Resurrecting a Dead Library: Part One - Resuscitation](https://mtlynch.io/resurrecting-1/)
* [Resurrecting a Dead Library: Part Two - Stabilization](https://mtlynch.io/resurrecting-2/)
* [Resurrecting a Dead Library: Part Three - Rehabilitation](https://mtlynch.io/resurrecting-3/)

## Zestful

[Zestful](https://zestfuldata.com) is a managed ingredient-parsing service based on this library. It has higher accuracy and more frequent updates:

* https://zestfuldata.com

## Overview

This repo contains scripts to extract the Quantity, Unit, Name, and Comments
from unstructured ingredient phrases. We use it on [Cooking][nytc] to format
incoming recipes. Given the following input:

    1 pound carrots, young ones if possible
    Kosher salt, to taste
    2 tablespoons sherry vinegar
    2 tablespoons honey
    2 tablespoons extra-virgin olive oil
    1 medium-size shallot, peeled and finely diced
    1/2 teaspoon fresh thyme leaves, finely chopped
    Black pepper, to taste

Our tool produces something like:

    {
        "qty":     "1",
        "unit":    "pound"
        "name":    "carrots",
        "other":   ",",
        "comment": "young ones if possible",
        "input":   "1 pound carrots, young ones if possible",
        "display": "<span class='qty'>1</span><span class='unit'>pound</span><span class='name'>carrots</span><span class='other'>,</span><span class='comment'>young ones if possible</span>",
    }

We use a conditional random field model (CRF) to extract tags from labelled
training data, which was tagged by human news assistants. We wrote about our
approach [on the New York Times Open blog][openblog]. More information about
CRFs can be found [here][crf_tut].

On a 2012 Macbook Pro, training the model takes roughly 30 minutes for 130k
examples using the [CRF++][crfpp] library.

## Development

On OSX:

```bash
brew install crf++
python setup.py install
```

Docker:

```bash
docker pull mtlynch/ingredient-phrase-tagger
```

## Quick Start

```bash
docker run -it mtlynch/ingredient-phrase-tagger bash

# Train a new model
MODEL_DIR=$(mktemp -d)
bin/train-prod-model "$MODEL_DIR"
MODEL_FILE=$(find $MODEL_DIR -name '*.crfmodel')

# Parse some ingredients
echo '
2 tablespoons honey
1/2 cup flour
Black pepper, to taste' | bin/parse-ingredients.py --model-file $MODEL_FILE
```

```text
[
  {
    "display": "<span class='qty'>2</span><span class='unit'>tablespoons</span><span class='name'>honey</span>",
    "input": "2 tablespoons honey",
    "name": "honey",
    "qty": "2",
    "unit": "tablespoon"
  },
  {
    "display": "<span class='qty'>1/2</span><span class='unit'>cup</span><span class='name'>flour</span>",
    "input": "1/2 cup flour",
    "name": "flour",
    "qty": "1/2",
    "unit": "cup"
  },
  {
    "comment": "to taste",
    "display": "<span class='name'>Black pepper</span><span class='other'>,</span><span class='comment'>to taste</span>",
    "input": "Black pepper, to taste",
    "name": "Black pepper",
    "other": ","
  }
]
```

## Authors

* [Erica Greene][eg]
* [Adam Mckaig][am]
* [Michael Lynch](https://github.com/mtlynch)


## License

[Apache 2.0][license].


[nytc]:     http://cooking.nytimes.com
[crf_tut]:  http://people.cs.umass.edu/~mccallum/papers/crf-tutorial.pdf
[crfpp]:    https://taku910.github.io/crfpp/
[openblog]: http://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/?_r=0
[eg]:       mailto:ericagreene@gmail.com
[am]:       http://github.com/adammck
[license]:  https://github.com/NYTimes/ingredient-phrase-tagger/blob/master/LICENSE.md
