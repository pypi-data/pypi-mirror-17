===============================
sumchecker
===============================


.. image:: https://img.shields.io/pypi/v/sumchecker.svg
        :target: https://pypi.python.org/pypi/sumchecker

.. image:: https://img.shields.io/travis/zacwalls'/sumchecker.svg
        :target: https://travis-ci.org/zacwalls'/sumchecker

.. image:: https://readthedocs.org/projects/sumchecker/badge/?version=latest
        :target: https://sumchecker.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/zacwalls'/sumchecker/shield.svg
     :target: https://pyup.io/repos/github/zacwalls'/sumchecker/
     :alt: Updates


A python script that will meet all of you're sumchecking needs!


* Free software: ISC license
* PyPI: https://pypi.python.org/pypi/sumchecker

What is 'SumChecker?'
---------------------

SumChecker is a Python script that more easily allows you to practice
safe internet browsing practices by checking the provided checksum of a file
downloaded from the internet.

What is a Checksum?
-------------------

A checksum is a small piece of data that helps detect errors and whether or not
something has been tampered with. By making sure that the provided checksum is the
same as the one you generate locally, you are making sure your files have not been
tampered with by a third party source.

What Checksum hash algorithms are supported?
--------------------------------------------

This script uses a library called hashlib, which currently only supports a handful of
hashes. These include MD5, SHA-224, SHA-256, SHA-384 and SHA-512.

Why did you include MD5?
------------------------

I am aware that the MD5 algorithm is currently broken, but I decided to implement it anyway
because it is still in use all over the internet. 

Why use SumChecker?
-------------------

SumChecker makes the process of checking a hash a lot easier. The process of using 
SumChecker is very easy as well as reassuring to the user.

Credits
------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Development Lead
--------------- 

* Zac Walls <zwallace0790@gmail.com>

Contributors
------------

None yet. Contributors are always welcome. So feel free to help in any way you see fit.