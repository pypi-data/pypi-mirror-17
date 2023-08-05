justbases-string
================

Purpose
-------
A small library for generating a human readable string value from a number
with an arbitrary base. The number is represented by five elements:

* a sign

  -1, 1, or 0 as appropriate

* an integer part

  a list of non-negative ints, where each element is less than the base value

* a non repeating fractional part

  a list of non-negative ints, where each element is less than the base value

* a repeating fractional part

  a list of non-negative ints, where each element is less than the base value

* a base

  the base of the number, must be an integer greater than 1.


Usage
-----

::

    >>> from justbases_string import *
    >>> xformer = String(DisplayConfig(), 2)
    >>> xformer.xform(-1, [1, 0, 1], [], [1, 0], 0)
    '-101.(10)_2'
    >>> xformer.xform(0, [], [0, 0], [], 0)
    '0_2'

An exception is raised if the parts of the number do not conform to the
necessary constraints: ::

    >>> xformer.xform(1, [2], [0, 0], [], 0)
    Traceback (most recent call last):
    ...

    >>> xformer.xform(1, [-1], [0, 0], [], 0)
    Traceback (most recent call last):
    ...

There are numerous options for configuring the string result: ::

    >>> digits_config = DigitsConfig(use_letters=False)
    >>> xformer = String(DisplayConfig(digits_config=digits_config), 1024)
    >>> xformer.xform(1, [2], [2, 4, 256], [], 0)
    '2.2~4~256_1024'

    >>> digits_config = DigitsConfig(use_caps=True)
    >>> xformer = String(DisplayConfig(digits_config=digits_config), 16)
    >>> xformer.xform(1, [], [0, 13], [], 0)
    '0.0D_16'

The final argument is the relation of the value being displayed to the value
it represents: ::

    >>> xformer.xform(1, [2], [2, 4, 256], [], Fraction(1, 3))
    '< 2.2~4~256_1024'
