Contribution
============

If you like to contribute to this project please read the following guides.

Django Code
-----------

You have to install some dependencies for development and testing.

.. code-block:: bash

    $ pip install -e .[tests]

Testing the code
````````````````

`django-anylink` uses ``py.test`` for testing. Please ensure that all tests pass
before you submit a pull request. ``py.test`` also runs PEP8 and PyFlakes checks
on every run.

We created a Makefile to make some commands more easy to run.

This is how you execute the tests and checks from the repository root directory.

.. code-block:: bash

    $ py.test

Or with the shortcut in the Makefile.

.. code-block:: bash

    $ make tests

If you want to generate a coverage report, you can use the following command.

.. code-block:: bash

    $ make coverage

If you want a coverage report with html output.

.. code-block:: bash

    $ make coverage-html

Documentation
`````````````

`django-anylink` uses Sphinx for documentation. You find all the sources files
in the ``docs/source`` folder.

To update/generate the html output of the documentation, use the following
command inside the ``docs`` folder.

.. code-block:: bash

    $ make html

Please make sure that you don't commit the build files inside ``docs/build``.

JavaScript Code
---------------

TBD
