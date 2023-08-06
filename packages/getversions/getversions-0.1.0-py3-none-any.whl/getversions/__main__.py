"""The entry point module for the getversions package.

This module is executed automatically when the package is run, e.g., with ``python
-m getversions package-name``, and dispatches the command line arguments to the
``main`` function in the ``main`` module.

"""

from getversions.main import main

raise SystemExit(main())
