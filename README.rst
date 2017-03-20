===============================
ftps
===============================

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License

.. image:: https://img.shields.io/pypi/v/ftps.svg
    :target: https://pypi.python.org/pypi/ftps
    :alt: PyPI version

.. image:: https://img.shields.io/travis/jcollado/ftps.svg
    :target: https://travis-ci.org/jcollado/ftps
    :alt: Continuous Integration

.. image:: https://coveralls.io/repos/github/jcollado/ftps/badge.svg?branch=master
    :target: https://coveralls.io/github/jcollado/ftps?branch=master
    :alt: Coverage

.. image:: https://landscape.io/github/jcollado/ftps/master/landscape.svg?style=flat
   :target: https://landscape.io/github/jcollado/ftps/master
   :alt: Code Health

.. image:: https://readthedocs.org/projects/ftps/badge/?version=latest
    :target: https://ftps.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jcollado/ftps/shield.svg
    :target: https://pyup.io/repos/github/jcollado/ftps/
    :alt: Updates


ftps client based on pycurl

Motivation
----------

If you use the python standard library to connect to an ftps server, you might
have to face some bugs as described `here <https://bugs.python.org/issue19500>`_
and `there <https://bugs.python.org/issue25437>`_.

An alternative is to give a try to pycurl_ which doesn't have those problems.
However, its interface is not very python and sometimes is not very pleasant to
work with it.

The goal of this small library is to provide a wrapper around pycurl_ that can
be used easily in a pythonic way.


Features
--------

* List remote path
* Download remote file
* Upload local file


Quick start
-----------

::

    import ftps

    client = ftps.FTPS(ftps.FTPS('ftp://<user>:<passwd>@<server>'))
    client.list()
    client.download(<remote_filename>, <local_filename>)
    client.upload(<local_filename>, <remote_filename>)


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _pycurl: http://pycurl.io/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

