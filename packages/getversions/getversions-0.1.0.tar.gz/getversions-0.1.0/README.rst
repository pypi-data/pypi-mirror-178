getversions
===========

Get the versions of a package available in the repository via pip, and the installed
version for the current interpreter.

You could use ``getversions`` in a deploy shell script to deploy the installed
version of a package if it is not already available in the repository.

.. code-block:: shell

  version=$(pygetversions -ie mypkg) \
  && echo deploying mypkg ${version} \
  || echo mypkg ${version} already in repo, not deploying

Installation
------------

.. code-block:: shell

  pip install getversions

Usage
-----

There are a few ways to invoke the ``main`` function from the command line. You
can use the console script installed with the package, run the package with Python,
or run the main module with Python. In each case, pass arguments on the command line.

Print Available and Installed Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the console script:

.. code-block:: shell

  pygetversions package_name

Run the package:

.. code-block:: shell

  python -m getversions package_name

Run the main module:

.. code-block:: shell

  python -m getversions.main package_name

For instance,

.. code-block:: shell

  pygetversions black

would produce output similar to

.. code-block:: shell

  *22.10.0
  22.8.0
  22.6.0
  22.3.0
  22.1.0

where ``black 22.10.0`` is installed for the current Python interpreter.

Print The Installed Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass the ``-i`` or ``--installed-only`` option to only print the installed version
for the current interpreter.

.. code-block:: shell

  pygetversions -i black

would produce output similar to

.. code-block:: shell

  22.10.0

where ``black 22.10.0`` is installed for the current Python interpreter.

Check Installed Version Available in Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass the ``-e`` or ``--exists-in-repo`` option to produce an exit code of 0 if the
installed version is not available in the repository, in which case you might want
to upload the installed version to the repository.

.. code-block:: shell

  pygetversions -e black

would produce output similar to

.. code-block:: shell

  *22.10.0
  22.8.0
  22.6.0
  22.3.0
  22.1.0

and an exit code of 1 if ``black 22.10.0`` is installed and available in the
repository.

.. code-block:: shell

  pygetversions -e getversions

may produce output similar to

.. code-block:: shell

  0.0.2
  0.0.1
  +0.0.3

and an exit code of 0 if ``getversions 0.0.3`` is installed, but not available in
the repository.

You could print just the installed version:

.. code-block:: shell

  pygetversions -ie getversions

which would produce output similar to

.. code-block:: shell

  0.0.3

and an exit code of 0 if ``getversions 0.0.3`` is installed, but not available in
the repository.
