========
Overview
========



APEX is a next generation APRS based protocol. This repository represents the reference implementation and is a full features application for digipeating across multiple AX.25 KISS TNC devices using the full APEX stack.

For more information on the project please check out `the project's home page <http://apexprotocol.com/>`_.

Running the app
===============

Install the application using pip:

    pip install apex-radio

The application is written for python 2 or 3. Once installed copy the apex.conf.example file over to apex.conf in the
/etc directory, then edit the file and replace it with your details. Next just run the application with the following
command.:

    apex-radio

There isn't much to the application right now, so thats all you should need to run it. Digipeating will occur
automatically and respond to the WIDEN-n paradigm as well as your own callsign. Cross-band repeating is enabled right
now but only by specifying the call sign directly. The application is still pre-release so more features and
configuration options should be added soon.

This is Free software: Apache License v2

Installation
============

::

    pip install apex

Documentation
=============

https://apex.readthedocs.io/

Development
===========

Initial setup::

    pip install -U pyenv tox
    pyenv install 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1
    pyenv global 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1

NOTE: The specific versions mentioned above may be different for each platform. use `pyenv install --list` to view the
list of available versions. You will need a version of 2.7.x, 3.3.x, 3.4.x, 3.5.x, and pypy. Try to use the latest
available version for each. Also some flavors of pyenv have different formats for it's arguments. So read the pyenv
documentation on your platform.

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Releasing
---------

* Ensure you have an account on PyPI, if you do not create one `here <https://pypi.python.org/pypi?%3Aaction=register_form>`_.

* Create or verify your `~/.pypirc` file. It should look like this::

    [distutils]
    index-servers =
      pypi
      pypitest

    [pypi]
    repository=https://pypi.python.org/pypi
    username = <username>
    password = <password>

    [pypitest]
    repository=https://testpypi.python.org/pypi
    username = <username>
    password = <password>


* Update CHANGELOG.rst

* Commit the changes::

    git add CHANGELOG.rst
    git commit -m "Changelog for upcoming release 0.1.1."


* Install the package again for local development, but with the new version number::

    python setup.py develop


* Run the tests::

    tox



* Release on PyPI by uploading both sdist and wheel::

    python setup.py sdist upload -r pypi
    python setup.py sdist upload -r pypitest
    python setup.py bdist_wheel --universal upload -r pypi
    python setup.py bdist_wheel --universal upload -r pypitest

  NOTE: Make sure you have Python Wheel installed for your distribution or else the above commands will not work.

* Update version number (can also be minor or major)::

    bumpversion patch


* Commit the version bump changes::

    git add .
    git commit -m "Bumping version for release cycle"


* Test that it pip installs::

    pip install apex-radio
    <try out my_project>


* Push: `git push`

* Push tags: `git push --tags`

* Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy
  and paste the RestructuredText into `ninjs <http://rst.ninjs.org/>`_ to find out what broke the formatting.

* Edit the release on `GitHub <https://github.com/Syncleus/apex/releases>`_ . Paste the release notes into the
  release's release page, and come up with a title for the release.


Changelog
=========

0.0.1
-----

* First release on PyPI.

0.0.2
-----

* The configfile command line argument added.
* When no configfile argument present APEX will now search multiple default paths to find a configuration file.
* Changed LICENSE file text to include the full text of the Apache Software License version 2.
* Colorized some of the output.
* Changed the way plugins are discovered, they can now be installed anywhere.
* Fixed a bug in the APRS-IS class which threw a broken pipe error.
* Refactored several classes and renamed them: Kiss class now has two subclasses and AprsInternetServer is renamed to IGate
* Encapsulated IGate connection with a buffer that automatically reconnects when disconnected.
* Removed a few obsolete and unused util functions.
* Fix several errors thrown due to missing sections in the configuration file.


