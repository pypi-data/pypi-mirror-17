Xenum: A simple alternative to Python 3 Enums.
==============================================

Xenum offers a simple alternative to Python 3 enums that's
especially useful for (de)serialization.  When you would like
to model your enum values so that they survive jumps to and
from JSON, databases, and other sources cleanly as strings,
Xenum will allow you to do so extremely easily.

Installation
------------

Installation is simple. With python3-pip, do the following:

$ sudo pip install -e .

Or, to install the latest version available on PyPI:

$ sudo pip install xenum

Usage
-----
Just create a basic class with attributes and annotate it with the
``@xenum`` attribute.  This will convert all of the class attributes
into Xenum instances and allow you to easily convert them to strings
via ``str(MyEnum.A)`` and from strings via ``MyEnum.by_name("MyEnum.A")``.

Example
-------
::

    from xenum import xenum

    @xenum
    class Colors:
      RED = 1
      GREEN = 2
      BLUE = 3

    # convert to a string
    str_value = str(Colors.RED)
    # convert from a string
    enum_value = Colors.by_name(str_value)
    
    if Colors.RED == enum_value:
      print('We did it!')

Checkout ``test.py`` in the git repo for more usage examples.

Change Log
----------

Version 1.1: August 31st, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Made Xenum instances hashable, removed value() as a function.

