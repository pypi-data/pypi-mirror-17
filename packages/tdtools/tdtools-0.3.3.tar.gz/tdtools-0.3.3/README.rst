tdtools
=======

.. image:: https://img.shields.io/pypi/v/tdtools.svg
     :target: https://pypi.python.org/pypi/tdtools
     :alt: PyPi
.. image:: https://img.shields.io/badge/License-GPL%20-blue.svg
     :target: http://www.gnu.org/licenses/gpl
     :alt: License

`tdtools <https://bitbucket.org/padhia/tdtools>`_ is a collection of tools and utilities I developed for my personal use. I am making these tools open-source in the hope that someone else may find them useful as well.

*NOTE:* These tools are not endorsed by `Teradata Inc <http://www.teradata.com/>`_.

Requirements
------------

Since I always try to use latest Python, you may find that some of the features require pretty recent version of Python. As of this writing, my installation consists of Python 3.5. If there is a strong interest in supporting earlier version of Python that requires me making minimal changes, I'll consider supporting earlier Python versions. However, I do suggest using the latest version of Python.

There is a dependency on `teradata <https://pypi.python.org/pypi/teradata/>`_ python package. However, it'll be downloaded automatically if you install using standard python installer ``pip``.

Installation
------------

Use Python's standard ``pip`` utility to install ``tdtools``. Although ``tdtools`` doesn't have too many dependecies, you may choose to install in an ``virtualenv``.::

  $ pip install tdtools

Configuration
-------------

No configuration is required except setting up the needed ODBC connections. All scripts that are part of ``tdtools`` accept arbitrary ``ODBC`` connection strings using ``--tdconn`` parameter.

If more flexibility is needed, for example, to use Teradata REST APIs, it can be done by providing ``sqlcsr_site.py`` in your ``PYTHONPATH``. Have a look at ``sqlcsr.py`` module to get an idea about what can be overriden in ``sqlcsr_site.py``.

Tools
-----

All tools are command-line utilities that are automatically installed when ``tdtools`` is installed using ``pip``. What follows is a brief description of each tool. Each tool support ``--help`` or ``-h`` command-line option that shows detailed description of options supported.

* ``dbhr``: Displays Teradata database hierarchy.
* ``vwref``: Display (or save) view hierarchy.
* ``tptload``: Load using and/or generate TPT script.

All **show\*** utilities generate DDLs for different types of Teradata objects.

* ``showdb``: Teradata database or user
* ``showgrant``: Teradata grants to user/role
* ``showprof``: Teradata profile
* ``showrole``: Teradata role
* ``showtvm``: Wrapper around Teradata ``SHOW <object>`` command
* ``showzone``: Teradata zone

Support:
--------

If you encounter an issue, report it using `issue tracker <https://bitbucket.org/padhia/tdtools/issues?status=new&status=open>`_. I'll try to provide a fix as soon as I can. If you already have a fix, send me a pull request.

Contributions:
--------------

Feel free to fork this repository and enhance in a way that you see fit. If you think your changes will benefit more people, send me a pull request.
