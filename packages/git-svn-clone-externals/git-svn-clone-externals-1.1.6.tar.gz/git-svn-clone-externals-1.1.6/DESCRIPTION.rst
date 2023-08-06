Clone an svn repo with externals
================================

|Join the chat at https://gitter.im/naufraghi/git-svn-clone-externals|
|PyPI version| |PyPI downloads| |GitHub license|

Usage
-----

``git-svn-clone-externals svn-working-copy dest-dir``

The main difference between this and other alternative scripts is that
this one starts from an svn checkout to discover the externals.

The package comes with some utility command to manage a nested
``git-svn`` clone:

-  ``git-svn-dcommit`` and ``git-svn-rebase``: as ``git svn <command>``
   but with automatic ``stash save`` and ``stash pop``
-  ``git-svn-outgoing``: shows a diff of dcommit'able commits

All scripts are offering a ``--recursive`` option.

Installation
------------

The scritps depends on ``git svn``, in Ubuntu you can get the package
with:

``$ sudo apt-get install git-svn``

and than install the script with:

``$ pip install git-svn-clone-externals``

License
-------

This script is released under the `MIT
License <http://naufraghi.mit-license.org>`__

TODO
----

-  git-ignore externals
-  test on convoluted externals (relative paths)
-  manage fixed revision externals

.. |Join the chat at https://gitter.im/naufraghi/git-svn-clone-externals| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/naufraghi/git-svn-clone-externals?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |PyPI version| image:: https://img.shields.io/pypi/v/git-svn-clone-externals.svg
   :target: https://pypi.python.org/pypi/git-svn-clone-externals
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/git-svn-clone-externals.svg
   :target: https://pypi.python.org/pypi/git-svn-clone-externals#downloads
.. |GitHub license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/naufraghi/git-svn-clone-externals
