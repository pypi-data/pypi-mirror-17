Chakra Version Tracker
======================

`Chakra Version Tracker <https://gitlab.com/gallaecio/chakraversiontracker>`_
is a project that provides a command-line tool to query `Chakra
<https://chakralinux.org/>`_ packages in `rolling repositories
<http://goo.gl/DSFlMl>`_ that are out of date.


Requirements
------------

- `Python 3 <https://docs.python.org/3/>`_

  .. note:: If you really need a Python 2 version let us know and we will
     consider providing support for both versions, but to make things simpler
     for us we currently support Python 3 only.

- `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_

- `jinja2 <http://jinja.pocoo.org/docs/dev/>`_

- `lxml <http://lxml.de/>`_

- `sphinx-argparse <https://sphinx-argparse.readthedocs.io/en/latest/>`_

- `termcolor <https://pypi.python.org/pypi/termcolor>`_

- `versiontracker <http://version-tracker.rtfd.io/>`_


Installation
------------

Installing with `pip <https://pip.pypa.io/en/stable/quickstart/>`_::

    pip install chakraversiontracker

Installing from sources::

    python setup.py install

Installing from sources for development (if you plan to extend tracked
packages)::

    python setup.py develop


Basic Usage
-----------

The `chakraversiontracker` command-line tool does not require any parameters::

    $ chakraversiontracker
    desktop:
        gsoap 2.8.33 → 2.8.34
        libguess 1.1 → 1.2

It lists outdated packages in rolling repositories, showing for each package
which version is currently in the repositories and which one is the latest
stable version.

If you want to get the name of the repository containing each package as well,
use `-t repositories.cli`::

    $ chakraversiontracker -t packages.cli
    gsoap 2.8.33 → 2.8.34
    libguess 1.1 → 1.2


Excluding Packages
------------------

You can use the `-e` option to exclude a package from the results::

    $ chakraversiontracker -e gsoap
    desktop:
        libguess 1.1 → 1.2

You can also use `-e` with a package tag to exclude all packages that have that
tag. Tags are similar to Chakra package groups, only that they are specific to
Chakra Version Tracker. Use `--list-tags` to get a list of available tags::

    $ chakraversiontracker --list-tags
    haskell
    kde-applications
    …


Selecting Repositories
----------------------

By default, Chakra Version Tracker checks package versions in the rolling
repositores: `testing`, `desktop`, `gtk`, `lib32`, `ccr`.

You may manually specify one or more target repositories with `-r`. For
example, to check package versions only in the `testing` and `desktop`
repositories::

    chakraversiontracker -r testing -r desktop

If you prefer, you may indicate repositories to exclude from the defalut list
using `--exclude-repository`. For example, to check package versions in all
rolling repositories but the `ccr`::

    chakraversiontracker --exclude-repository ccr


Configuring the Output
----------------------

The output of the `chakraversiontracker` command can be completely customized
with a template. Use the `--list-templates` option to get a list of available
built-in templates that you can pass to the `-t` option.

Built-in templates may have either a `.txt` file extension or a `.cli` file
extension. If you want to redirect the output of the command to a file, use the
`-o` option and one of the `.txt` templates. `.cli` templates include data for
terminal coloring that does not look well in plain text files.

By default, a line in printed on the standard output with the progress of the
query for the latest stable versions of tracked packages found in the specified
repositories. If you are using a pipe to redirect the output to a file instead
of using the `-o` option, you may want to use the `--no-progress` option to
prevent the progress lines from being printed.

You can write a custom template and pass its path to the command using the
`-t` option to format the output data however you like. Your template must be a
`Jinja2 <http://jinja.pocoo.org/docs/dev/templates/>`_ template that can use
the following variables:

- `packages` is a list of dictionaries represeting outdated packages. They are
  sorted alphabetically, and each dictionary contains the name of the package
  (`name`), the name of the repository that contains the package
  (`repository`), the version of the package found in the repositories
  (`repository_version`) and the latest stable version of the package
  (`upstream_version`).

- `repositories` is an ordered dictionary (in the order in which the user
  specified the repositories) where keys are repository names and values are
  dictionaries with the same keys as the items in the `packages` list, with the
  exception of the `repository` key.

- `date` is a dictionary with two keys: `local` and `utc`. They are `datetime`
  objects containing the local time and the UTC time, respectively.


Extending Package Support
--------------------------

Chakra Version Tracker is not designed to let each user keep their custom
package tracking data. Changes require you to *fork* the source code. If you
do, we encourage you to `send us back your changes
<https://gitlab.com/gallaecio/chakraversiontracker/merge_requests>`_ so that
everyone can benefit from them.

Use the following to clone the Git repository and install in development mode,
so that your changes have effect on your system as soon as you save:

.. code-block:: bash

    # If you have chakraversiontracker installed:
    sudo pip3 uninstall chakraversiontracker

    git clone https://gitlab.com/gallaecio/chakraversiontracker.git
    cd chakraversiontracker
    sudo python3 setup.py develop

You can now work directly on the newly created folder, and whenever you execute
`chakraversiontracker` the code in that folder will be executed.

The data used to determine how to fetch version information of a supported
package is defined in a JSON file, `chakraversiontracker/data.json`. This file
indicates how packages in the Chakra repositories map to `Version Tracker
<http://version-tracker.rtfd.io/>`_ software IDs.

The data file contains a JSON object where keys are package names, and their
value is a JSON object with settings::

    {
        "0ad": { … },
        "0ad-data": { … },
        …
    }

The object of each entry is usually empty, which indicates that the package is
associated with the Version Tracker software ID with the same name::

    "0ad": {}

If the package matches a different Version Tracker software ID, that ID is
specified as the value of the `versiontracker` field::

    "0ad-data": { "versiontracker": "0ad" }

If a package should not be tracked (e.g. no new releases are expected), set the
`skip` field to `true`::

    "man2html": {
        "skip": true
    }

If you want to ignore the package until a new version comes out (e.g. because
the repositories are using a non-stable version that is newer than the stable
version reported by Version Tracker), set the value of the `skip` field to the
latest stable version reported by Version Tracker::

    "lockdev": {
        "skip": "1.0.3"
    }

Packages can be tagged, so that you can easily ignore all packages with a given
tag. To add one or more tags to a package, use the `tags` field::

    "dragon": {
        "tags": [
            "kde-applications"
        ]
    }


Command Line Help
-----------------

.. argparse::
   :module: chakraversiontracker.__main__
   :func: _build_argument_parser
   :prog: chakraversiontracker
   :nodefault:


Credits and License
-------------------

Chakra Version Tracker may be used under the terms of the :doc:`GNU Affero
General Public License version 3 </license>` or later (AGPLv3+).

For a list of authors who should be credited, see :doc:`/authors`.

.. toctree::
   :hidden:

   self
   license
   authors
