click-man
=========

|Build Status| |PyPI Package version|

Create **man pages** for `click <https://github.com/pallets/click>`__
application as easy as this:

.. code:: bash

    python3 setup.py --command-packages=click_man.commands man_pages

.. figure:: https://raw.githubusercontent.com/timofurrer/click-man/master/docs/asciicast.gif
   :alt: Demo

   Demo

What it does
------------

*click-man* will generate one man page per command from your click CLI
application specified in ``console_scripts`` in your ``setup.py``.

Installation
------------

.. code:: bash

    pip3 install click-man

**click-man** is also available for Python 2:

.. code:: bash

    pip install click-man

Usage Recipes
-------------

The following sections describe different usage example for *click-man*.

Use with setuptools
~~~~~~~~~~~~~~~~~~~

**click-man** provides a sane setuptools command extension which can be
used like the following:

.. code:: bash

    python setup.py --command-packages=click_man.commands man_pages

or specify the man pages target directory:

.. code:: bash

    python setup.py --command-packages=click_man.commands man_pages --target path/to/man/pages

Debian packages
~~~~~~~~~~~~~~~

*Coming soon ...*

Standalone
~~~~~~~~~~

*Coming soon ...*

.. |Build Status| image:: https://travis-ci.org/timofurrer/click-man.svg?branch=master
   :target: https://travis-ci.org/timofurrer/click-man
.. |PyPI Package version| image:: https://badge.fury.io/py/sure.svg
   :target: https://pypi.python.org/pypi/click-man
