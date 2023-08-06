Originally a proof of concept, I've used this in enough projects that
I've decided to publish it tomake it easier to import. The name is a
play on words similar to Markup/Markdown.

Basic Use
=========

Use the included ``from_sentences()`` and ``from_words()`` if your data
already behaves nicely. Your input sequences of words or sentences
should be delimited by newlines. Use ``next_word()`` and
``next_sentence()`` to generate your output.

In the case that you want ot generate sequences from non-text data, read
the following paragraph. Instantiate with ``m = markoff.Markov(seeds)``
where ``seeds`` is an iterable of sub-iterables. Each sub-iterable being
a chain in the set of chains you want to model.

You can supply it with just one chain or many.

Then use ``m.generate(max_length=100)`` to produce a single chain
limited to ``max_length`` automatically terminating at known ending
state.

Examples
========

Generating Sentences
--------------------

Input
~~~~~

::

    m = pymarkoff.from_sentences(
    """The quick brown fox jumped over the lazy dog.
    Jack and Jill ran up the hill to fetch a pail of water.
    Whenever the black fox jumped the squirrel gazed suspiciously."""
    )

    print([m.next_sentence() i for i in range(10)])

Output
~~~~~~

::

    [
        'The quick brown fox jumped over the black fox jumped the lazy dog.',
        'The quick brown fox jumped the squirrel gazed suspiciously.',
        'Whenever the squirrel gazed suspiciously.',
        'Jack and Jill ran up the lazy dog.',
        'Jack and Jill ran up the hill to fetch a pail of water.',
        'Jack and Jill ran up the black fox jumped the hill to fetch a pail of water.',
        'Whenever the lazy dog.',
        'The quick brown fox jumped over the lazy dog.',
        'Jack and Jill ran up the hill to fetch a pail of water.',
        'Jack and Jill ran up the squirrel gazed suspiciously.'
     ]

Generating Words
----------------

Input
~~~~~

::

    seeds = """Ana
    Bastion
    D.Va
    Genji
    Hanzo
    Junkrat
    Lúcio
    McCree
    Mei
    Mercy
    Pharah
    Reaper
    Reinhardt
    Roadhog
    Soldier: 76
    Symmetra
    Torbjörn
    Tracer
    Widowmaker
    Winston
    Zarya
    Zenyatta"""

    brain = pymarkoff.from_words(mystr)
    print([brain.next_word() for i in range(10)])

Output
~~~~~~

::

    ['Zen', 'D.Vaperein', 'Za', 'To', 'Merya', 'Metrdo', 'So', 'Junjör', 'Ph', 'Mera']

Notes
=====

This module is still under development and is mostly for me to play
around with and learn Markov Chains. Cheers.
