Contribution
============

If you like to contribute to this project please read the following guides.

Django Code
-----------

To install all requirements for development and testing, you can use the provided
requirements file.

.. code-block:: terminal

    $ pip install -r resources/requirements-develop.txt

Testing the code
````````````````

`django-anylink` uses ``py.test`` for testing. Please ensure that all tests pass
before you submit a pull request. ``py.test`` also runs PEP8 and PyFlakes checks
on every run.

This is how you execute the tests and checks from the repository root directory.

.. code-block:: terminal

    $ py.test

If you want to generate a coverage report, you can use the following command.

.. code-block:: terminal

    $ py.test --cov=omnibus --cov-report=html .

Documentation
`````````````

`django-anylink` uses Sphinx for documentation. You find all the sources files
in the ``docs/source`` folder.

To update/generate the html output of the documentation, use the following
command inside the ``docs`` folder.

.. code-block:: terminal

    $ make html

Please make sure that you don't commit the build files inside ``docs/build``.

JavaScript Code
---------------

TBD
