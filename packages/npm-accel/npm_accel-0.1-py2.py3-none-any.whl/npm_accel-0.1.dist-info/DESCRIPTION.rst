npm-accel: Accelerator for npm, the Node.js package manager
===========================================================

.. image:: https://travis-ci.org/xolox/python-npm-accel.svg?branch=master
   :target: https://travis-ci.org/xolox/python-npm-accel

.. image:: https://coveralls.io/repos/xolox/python-npm-accel/badge.svg?branch=master
   :target: https://coveralls.io/r/xolox/python-npm-accel?branch=master

The npm-accel program is a wrapper for npm_ (the Node.js_ package manager) that
optimizes one specific use case: Building a node_modules_ directory from a
package.json_ file as quickly as possible. It works on the assumption that you
build node_modules directories more frequently then you change the contents of
package.json files, because it computes a fingerprint of the dependencies and
uses that fingerprint as a cache key, to cache the complete node_modules
directory in a tar archive. The npm-accel project is currently tested on Python
2.6, 2.7, 3.4, 3.5 and PyPy (yes, it's written in Python, deal with it :-P).

.. contents::
   :local:

Status
------

The npm-accel project was developed and published in September '16 because I
got fed up waiting for ``npm install`` to finish, specifically in the context
of continuous integration builds and deployments (where you frequently start
with an empty ``node_modules`` directory). It was developed in about a week
without much prior knowledge about Node.js_ or npm_, which explains why it's
written in Python :-P. On the one hand npm-accel hasn't seen much actual use,
on the other hand it has a test suite with about 95% test coverage and I was
careful not to repeat the bugs I encountered in npm-cache_ and
npm-fast-install_ while evaluating those tools :-).

To summarize: Give it a try, see if it actually speeds up your ``npm install``
commands and then decide whether you want to use it or not.

Performance
-----------

The following table lists the output of ``npm-accel --benchmark`` (with some
enhancements) against a private code base with about 30 dependencies listed in
the package.json file (resulting in a 401 MB node_modules directory):

=====================  =========  =======================  ==========
Approach               Iteration  Elapsed time             Percentage
=====================  =========  =======================  ==========
npm install                  1/2  1 minute and 36 seconds      100.0%
npm install                  2/2  1 minute and 40 seconds      104.1%
npm-accel                    1/2  1 minute and 40 seconds      104.1%
npm-accel                    2/2             7.26 seconds        7.5%
npm-cache install npm        1/2  3 minutes and 9 seconds      196.8%
npm-cache install npm        2/2  2 minutes and 9 seconds      134.3%
npm-fast-install             1/2  1 minute and 5 seconds        72.2%
npm-fast-install             2/2  1 minute and 6 seconds        73.3%
=====================  =========  =======================  ==========

Installation
------------

The `npm-accel` package is available on PyPI_ which means installation
should be as simple as:

.. code-block:: sh

   $ pip install npm-accel

There's actually a multitude of ways to install Python packages (e.g. the `per
user site-packages directory`_, `virtual environments`_ or just installing
system wide) and I have no intention of getting into that discussion here, so
if this intimidates you then read up on your options before returning to these
instructions ;-).

Usage
-----

There are two ways to use the `npm-accel` package: As the command line program
``npm-accel`` and as a Python API. For details about the Python API please
refer to the API documentation available on `Read the Docs`_. The command line
interface is described below.

.. contents::
   :local:

.. A DRY solution to avoid duplication of the `npm-accel --help' text:
..
.. [[[cog
.. from humanfriendly.usage import inject_usage
.. inject_usage('npm_accel.cli')
.. ]]]

**Usage:** `npm-accel [OPTIONS] [DIRECTORY]`

The npm-accel program is a wrapper for npm (the Node.js package manager) that optimizes one specific use case: Building a "node_modules" directory from a "package.json" file as quickly as possible.

It works on the assumption that you build "node_modules" directories more frequently then you change the contents of "package.json" files, because it computes a fingerprint of the dependencies and uses that fingerprint as a cache key, to cache the complete "node_modules" directory in a tar archive.

**Supported options:**

.. csv-table::
   :header: Option, Description
   :widths: 30, 70


   "``-p``, ``--production``","Don't install modules listed in ""devDependencies""."
   "``-i``, ``--installer=NAME``","Set the installer to use. Supported values for ``NAME`` are
   ""npm"" (the default), ""npm-cache"" and ""npm-fast-install""."
   "``-c``, ``--cache-directory=DIR``",Set the pathname of the directory where the npm-accel cache is stored.
   "``-n``, ``--no-cache``","Disallow writing to the cache managed by npm-accel (reading is still
   allowed though). This option doesn't disable the caching that's done by
   npm-cache and npm-fast-install internally."
   "``-b``, ``--benchmark``","Benchmark and compare the following installation methods:

   1. npm install
   2. npm-accel
   3. npm-cache
   4. npm-fast-install

   The first method performs no caching (except for the HTTP caching that's
   native to npm) while the other three methods each manage their own cache
   (that is to say, the caching logic of npm-accel will only be used in the
   second method).

   Warning: Benchmarking wipes the caches managed by npm, npm-accel, npm-cache
   and npm-fast-install in order to provide a fair comparison (you can
   override this in the Python API but not on the command line)."
   "``-r``, ``--remote-host=SSH_ALIAS``","Operate on a remote system instead of the local system. The
   ``SSH_ALIAS`` argument gives the SSH alias of the remote host."
   "``-v``, ``--verbose``",Make more noise.
   "``-q``, ``--quiet``",Make less noise.
   "``-h``, ``--help``","Show this message and exit.
   "

.. [[[end]]]

Future improvements
-------------------

**Automatic cache invalidation**
 Currently the ``~/.cache/npm-accel`` directory will simply keep growing as new
 installations are added to the cache. Eventually I want npm-accel to
 automatically remove cache entries that are no longer being used. Given that
 "last accessed time" of files is frequently disabled in high performance
 situations like continuous integration environments and build servers I may
 need to enhance the cache directory with metadata per cache entry. I'm still
 thinking about the best way to approach this...

**Accelerate installations with changes**
 Currently when the fingerprint (cache key) of the dependencies doesn't match a
 cache entry, the complete caching mechanism is bypassed and a full ``npm
 install`` run is performed. It might be faster to unpack a previous (now
 invalid) cache entry corresponding to the same project and then run ``npm
 install && npm prune``. Given the fact that defining "same project" might be
 non-trivial I'm not actually sure this is worth my time.

**Dealing with optionalDependencies**
 I've never seen ``optionalDependencies`` in the wild but encountered them
 while browsing through the package.json_ documentation. Maybe these should be
 part of the computed cache keys aswell?

Contact
-------

The latest version of `npm-accel` is available on PyPI_ and GitHub_. The
documentation is hosted on `Read the Docs`_. For bug reports please create an
issue on GitHub_. If you have questions, suggestions, etc. feel free to send me
an e-mail at `peter@peterodding.com`_.

License
-------

This software is licensed under the `MIT license`_.

© 2016 Peter Odding.


.. External references:
.. _GitHub: https://github.com/xolox/python-npm-accel
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License
.. _Node.js: https://nodejs.org/en/
.. _node_modules: https://docs.npmjs.com/getting-started/installing-npm-packages-locally#installing
.. _npm-cache: https://www.npmjs.com/package/npm-cache
.. _npm-fast-install: https://www.npmjs.com/package/npm-fast-install
.. _npm: https://www.npmjs.com/
.. _package.json: https://docs.npmjs.com/files/package.json
.. _per user site-packages directory: https://www.python.org/dev/peps/pep-0370/
.. _peter@peterodding.com: peter@peterodding.com
.. _PyPI: https://pypi.python.org/pypi/npm-accel
.. _Read the Docs: https://github.com/xolox/python-npm-accel
.. _virtual environments: http://docs.python-guide.org/en/latest/dev/virtualenvs/


