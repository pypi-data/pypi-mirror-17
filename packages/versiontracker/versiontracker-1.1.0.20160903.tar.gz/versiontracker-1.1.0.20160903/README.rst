`Version Tracker <https://gitlab.com/gallaecio/versiontracker>`_ is a project
that provides both a command-line tool and a library to query the latest stable
versions of different software products using web scrapping.

For example, do you know `VLC <http://www.videolan.org/index.html>`_ ? You can
use the command-line interface of Version Tracker to find out what is the
latest stable version of VLC::

    $ versiontracker vlc
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/

Version Tracker is currently being used to detect obsolete packages in `Chakra
<http://chakralinux.org/>`_ and to feed updated software version information to
`Wikidata <http://wikidata.org/>`_.


Installing Version Tracker
==========================

You can install Version Tracker with `pip`::

    pip install versiontracker


Using the Command-Line Tool
===========================

Using the `versiontracker` command line is easy, you just pass it a list of
software IDs. For example::

    $ versiontracker vlc xfce
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/
    xfce: 4.12 (2015-02-28) @ http://archive.xfce.org/xfce/

You can use the `--list` option to get a list of supported software IDs::

    $ versiontracker --list
    0ad
    4kslideshowmaker
    …


Using the Library
=================

To get information about the latest stable version of a single product, use the
`latest_stable_version()` function::

    >>> from pprint import pprint
    >>> from versiontracker import latest_stable_version
    >>> pprint(latest_stable_version('vlc'))
    {'id': 'vlc',
     'reference_url': u'http://get.videolan.org/vlc/',
     'release_date': datetime.datetime(2016, 7, 6, 10, 10),
     'version': u'2.2.2'}

If you want to get version information for several products, you can use the
`iter_latest_stable_versions()` function, which uses multithreading to perform
multiple requests simultaneously::

    >>> from versiontracker import iter_latest_stable_versions
    >>> for version_data in iter_latest_stable_versions(('vlc', 'xfce')):
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

To obtain a list of supported software IDs, use the `supported_software()`
function::

    >>> from versiontracker import supported_software
    >>> supported_software()
    [u'kde-l10n-ca', u'kdiamond', u'kontactinterface', u'entropy', u'go', …]
    >>>


Additional Documentation
========================

The `doc` folder contains additional documentation:

- `extending_data.rst` describes how to add new software entries to the
  `data.json` file that Version Tracker uses to determine how to retrieve
  version information for each product.

- `custom_seeker.rst` describes how to write *ad hoc* web scrapping code to
  determine the version information of a new product. When the latest version
  of a product can only be queried through a product-specific website, this is
  the way to go.

- `creating_seekers.rst` describes how to write your own seeker, which is a web
  scrapping class that can be used to fetch the version information of several
  different products by feeding it slightly different data for each product.


Credits and License
===================

Version Tracker may be used under the terms of the GNU Affero General Public
License version 3 or later (AGPLv3+).

For a list of authors who should be credited, see the `AUTHORS.txt` file.
