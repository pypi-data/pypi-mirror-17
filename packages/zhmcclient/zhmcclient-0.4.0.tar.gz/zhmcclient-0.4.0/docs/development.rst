.. Copyright 2016 IBM Corp. All Rights Reserved.
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..


.. _`Development`:

Development
===========

This section only needs to be read by developers of the zhmcclient package.
People that want to make a fix or develop some extension, and people that
want to test the project are also considered developers for the purpose of
this section.


.. _`Repository`:

Repository
----------

The repository for zhmcclient is on GitHub:

https://github.com/zhmcclient/python-zhmcclient


.. _`Setting up the development environment`:

Setting up the development environment
--------------------------------------

The development environment is pretty easy to set up.

Besides having a supported operating system with a supported Python version
(see :ref:`Supported environments`), it is recommended that you set up a
`virtual Python environment`_.

.. _virtual Python environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then, with a virtual Python environment active, clone the Git repo of this
project and prepare the development environment with ``make develop``:

::

    $ git clone git@github.com:zhmcclient/python-zhmcclient.git
    $ cd python-zhmcclient
    $ make develop

This will install all prerequisites the package needs to run, as well as all
prerequisites that you need for development.

Generally, this project uses Make to do things in the currently active
Python environment. The command ``make help`` (or just ``make``) displays a
list of valid Make targets and a short description of what each target does.


.. _`Building the documentation`:

Building the documentation
--------------------------

The ReadTheDocs (RTD) site is used to publish the documentation for the
zhmcclient package at http://python-zhmcclient.readthedocs.io/

This page automatically gets updated whenever the ``master`` branch of the
Git repo for this package changes.

In order to build the documentation locally from the Git work directory, issue:

::

    $ make builddoc

The top-level document to open with a web browser will be
``build_doc/html/docs/index.html``.


.. _`Testing`:

Testing
-------

To run unit tests in the currently active Python environment, issue one of
these example variants of ``make test``:

::

    $ make test                                  # Run all unit tests
    $ TESTCASES=test_resource.py make test       # Run only this test source file
    $ TESTCASES=TestInit make test               # Run only this test class
    $ TESTCASES="TestInit or TestSet" make test  # py.test -k expressions are possible

To run the unit tests and some more commands that verify the project is in good
shape in all supported Python environments, use Tox:

::

    $ tox                              # Run all tests on all supported Python versions
    $ tox -e py27                      # Run all tests on Python 2.7
    $ tox -e py27 test_resource.py     # Run only this test source file on Python 2.7
    $ tox -e py27 TestInit             # Run only this test class on Python 2.7
    $ tox -e py27 TestInit or TestSet  # py.test -k expressions are possible

The positional arguments of the ``tox`` command are passed to ``py.test`` using
its ``-k`` option. Invoke ``py.test --help`` for details on the expression
syntax of its ``-k`` option.


.. _`Contributing`:

Contributing
------------

Third party contributions to this project are welcome!

In order to contribute, create a `Git pull request`_, considering this:

.. _Git pull request: https://help.github.com/articles/using-pull-requests/

* Test is required.
* Each commit should only contain one "logical" change.
* A "logical" change should be put into one commit, and not split over multiple
  commits.
* Large new features should be split into stages.
* The commit message should not only summarize what you have done, but explain
  why the change is useful.
* The commit message must follow the format explained below.

What comprises a "logical" change is subject to sound judgement. Sometimes, it
makes sense to produce a set of commits for a feature (even if not large).
For example, a first commit may introduce a (presumably) compatible API change
without exploitation of that feature. With only this commit applied, it should
be demonstrable that everything is still working as before. The next commit may
be the exploitation of the feature in other components.

For further discussion of good and bad practices regarding commits, see:

* `OpenStack Git Commit Good Practice`_
* `How to Get Your Change Into the Linux Kernel`_

.. _OpenStack Git Commit Good Practice: https://wiki.openstack.org/wiki/GitCommitMessages
.. _How to Get Your Change Into the Linux Kernel: https://www.kernel.org/doc/Documentation/SubmittingPatches

Format of commit messages
-------------------------

A commit message must start with a short summary line, followed by a blank
line.

Optionally, the summary line may start with an identifier that helps
identifying the type of change or the component that is affected, followed by
a colon.

It can include a more detailed description after the summary line. This is
where you explain why the change was done, and summarize what was done.

It must end with the DCO (Developer Certificate of Origin) sign-off line in the
format shown in the example below, using your name and a valid email address of
yours. The DCO sign-off line certifies that you followed the rules stated in
`DCO 1.1`_. In short, you certify that you wrote the patch or otherwise have
the right to pass it on as an open-source patch.

.. _DCO 1.1: https://raw.githubusercontent.com/zhmcclient/python-zhmcclient/master/DCO1.1.txt

We use `GitCop`_ during creation of a pull request to check whether the commit
messages in the pull request comply to this format.
If the commit messages do not comply, GitCop will add a comment to the pull
request with a description of what was wrong.

.. _GitCop: http://gitcop.com/

Example commit message:

::

    cookies: Add support for delivering cookies

    Cookies are important for many people. This change adds a pluggable API for
    delivering cookies to the user, and provides a default implementation.

    Signed-off-by: Random J Developer <random@developer.org>

Use ``git commit --amend`` to edit the commit message, if you need to.

Use the ``--signoff`` (``-s``) option of ``git commit`` to append a sign-off
line to the commit message with your name and email as known by Git.

If you like filling out the commit message in an editor instead of using
the ``-m`` option of ``git commit``, you can automate the presence of the
sign-off line by using a commit template file:

* Create a file outside of the repo (say, ``~/.git-signoff.template``)
  that contains, for example:

  ::

      <one-line subject>

      <detailed description>

      Signed-off-by: Random J Developer <random@developer.org>

* Configure Git to use that file as a commit template for your repo:

  ::

      git config commit.template ~/.git-signoff.template
