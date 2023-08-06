pub2
====

Pub2 is a self-publishing framework.

Overview
--------

Pub2 is a self-publishing framework.  It integrates with Jekyll to provide LaTeX publishing.

Installation
^^^^^^^^^^^^

The following will install pub2.

::

    mkvirtualenv -a . my-website
    pip install pub2

Pub2 can be installed system-wide with Homebrew.

::

    brew install https://raw.githubusercontent.com/iandennismiller/pub2/master/etc/pub2.rb

Usage
^^^^^

Create a new folder and switch to it.  The following will initialize the folder and render a sample document.

::

    pub2 init
    pub2 build

Documentation
^^^^^^^^^^^^^

http://pub2.readthedocs.io
