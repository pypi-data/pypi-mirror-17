Version Tracker
===============

`Version Tracker <https://gitlab.com/gallaecio/versiontracker>`_ is a project
that provides both a command-line tool and a library to query the latest stable
versions of different software products using web scrapping.

For example::

    $ versiontracker vlc
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/


It is currently being used to detect obsolete packages in `Chakra
<http://chakralinux.org/>`_ and to feed updated software version information to
`Wikidata <http://wikidata.org/>`_.


Installation
------------

Installing with `pip <https://pip.pypa.io/en/stable/quickstart/>`_::

    pip install versiontracker

Installing from sources::

    python setup.py install

Installing from sources for development (if you plan to extend supported
software)::

    python setup.py develop


Command-Line Usage
------------------

To use the `versiontracker` command-line application pass it a list of software
IDs::

    $ versiontracker vlc xfce
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/
    xfce: 4.12 (2015-02-28) @ http://archive.xfce.org/xfce/

You can use the `-l` option to get a list of supported software IDs::

    $ versiontracker -l
    0ad
    4kslideshowmaker
    …

.. _library-usage:

Library Usage
-------------

Use `version_info()` to get information about the latest stable
version of a single product::

    >>> from pprint import pprint
    >>> from versiontracker import version_info
    >>> pprint(version_info('vlc'))
    {'id': 'vlc',
     'reference_url': u'http://get.videolan.org/vlc/',
     'release_date': datetime.datetime(2016, 7, 6, 10, 10),
     'version': u'2.2.2'}

Use `iter_version_info()` to iterate through the version information of several
products::

    >>> from versiontracker import iter_version_info
    >>> for version_data in iter_version_info(('vlc', 'xfce')):
    ...     pprint(version_data)
    ...
    {'id': 'vlc',
     'reference_url': u'http://get.videolan.org/vlc/',
     'release_date': datetime.datetime(2016, 7, 6, 10, 10),
     'version': u'2.2.2'}
    {'id': 'xfce',
     'reference_url': u'http://archive.xfce.org/xfce/',
     'release_date': datetime.datetime(2015, 2, 28, 21, 7),
     'version': '4.12'}

Use `supported_software()` to get a list of supported software IDs::

    >>> from versiontracker import supported_software
    >>> supported_software()
    [u'kde-l10n-ca', u'kdiamond', u'kontactinterface', u'entropy', …]


Extending Software Support
--------------------------

To extend the list of supported software products, see:

- :doc:`/extending_data` describes how to add new software entries to the
  `data.json` file.

  This is how you extend software support, as long as you can use one of the
  existing seekers for the software that you want to support.

- :doc:`/custom_seeker` describes how to write code that determines the version
  information of a new product.

  This is what you should do if none of the built-in seekers works for the
  software that you wanto to support, and writing a new seeker does not make
  sense because the code will only work for the target software.

- :doc:`/creating_seekers` describes how to write your own seeker, a Python
  class that can fetch version information of several software products.


API Reference
-------------

- :ref:`versiontracker`

- :ref:`versiontracker.baseseekers`


Credits and License
-------------------

Version Tracker may be used under the terms of the :doc:`GNU Affero General
Public License version 3 </license>` or later (AGPLv3+).

For a list of authors who should be credited, see :doc:`/authors`.

.. toctree::
   :hidden:

   self
   extending_data
   custom_seeker
   creating_seekers
   versiontracker
   license
   authors
