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

    from xenum import xenum, ctor

    @xenum
    class Actions:
      INSERT = ctor('insert')
      UPDATE = ctor('update')
      DELETE = ctor('delete')

      def __init__(self, name):
         self.name = name
     
    assert Actions.INSERT == Actions.by_name('Actions.INSERT')
    assert Actions.INSERT().name == 'insert'

Checkout ``test.py`` in the git repo for more usage examples.

Change Log
----------

Version 1.4: September 5th, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add 'xenum.sref()' allowing enum values to be instances of the
  @xenum annotated class, whos `*args` is prepended with the 
  Xenum instance itself for self-reference.

Version 1.3: September 4th, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add 'xenum.ctor()' allowing enum values to be instances of the
  @xenum annotated class.
- Made Xenum instances callable, returning the enum's internal value.

Version 1.2: September 4th, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add 'values()' method to @xenum annotated classes for fetching
  an ordered sequence of the Xenum entities created.

Version 1.1: August 31st, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Made Xenum instances hashable, removed value() as a function.

