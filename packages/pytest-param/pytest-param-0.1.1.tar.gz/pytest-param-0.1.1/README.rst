pytest-param
============

pytest-param is a plugin for `py.test <http://pytest.org>`_ that makes it
easy to test all, first, last or random params.

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/cr3/pytest-param/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-param.svg
   :target: https://pypi.python.org/pypi/pytest-param/
   :alt: PyPI
.. image:: https://img.shields.io/travis/cr3/pytest-param.svg
   :target: https://travis-ci.org/cr3/pytest-param/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/cr3/pytest-param.svg
   :target: https://github.com/cr3/pytest-param/issues
   :alt: Issues

Requirements
------------

You will need the following prerequisites to use pytest-param:

- Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy or PyPy3
- py.test 2.6 or newer

Installation
------------

To install pytest-param:

.. code-block:: bash

  $ pip install pytest-param

Testing a param
---------------

Given `test_file.py` with this test:

.. code-block:: python

  import pytest
  @pytest.mark.parametrize("params", [True, False])
  def test_param(params):
      pass

Use the :code:`--param=first` command line option to test the :code:`True`
param:

.. code-block:: bash

  $ py.test --param=first test_file.py

Use :code:`--param=last` to test the :code:`False` param:

.. code-block:: bash

  $ py.test --param=last test_file.py

Use :code:`--param=random` to test one of the params at random.


Resources
---------

- `Release Notes <http://github.com/cr3/pytest-param/blob/master/CHANGES.rst>`_
- `Issue Tracker <http://github.com/cr3/pytest-param/issues>`_
- `Code <http://github.com/cr3/pytest-param/>`_
