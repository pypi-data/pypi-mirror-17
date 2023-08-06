##############
Travis-Encrypt
##############

|travis| |coverage| |dependencies| |codacy| |version| |status| |pyversions| |format| |license|


Travis-Encrypt is a Python command line application that provides a way to encrypt passwords
for use with Travis CI. This application intends to be a replacement for the Travis Ruby client
as that client is not maintained and does not provide detail regarding password encryption.

*************
Installation
*************


To install Travis-Encrypt simply run the following command in a terminal window::

    $ pip install travis-encrypt

If you would rather install from source, run the following commands in a terminal window::

    $ git clone https://github.com/mandeep/Travis-Encrypt.git
    $ cd Travis-Encrypt
    $ python setup.py install

Travis-Encrypt will attempt to install the cryptography package, however the package requires
headers for Python. If installation fails, please see the cryptography installation guide:
https://cryptography.io/en/latest/installation/

******
Usage
******

With Travis-Encrypt installed, the command line application can be invoked with the following command and mandatory arguments::

    travis-encrypt GITHUB_USERNAME REPOSITORY PATH

    Example:

    travis-encrypt mandeep Travis-Encrypt /home/user/.travis.yml

The application will then issue a mandatory password prompt. Once the password is filled,
Travis-Encrypt will write the encrypted password to the given .travis.yml file.

.. |travis| image:: https://travis-ci.org/mandeep/Travis-Encrypt.svg?branch=master
    :target: https://travis-ci.org/mandeep/Travis-Encrypt
.. |coverage| image:: https://img.shields.io/coveralls/mandeep/Travis-Encrypt.svg
    :target: https://coveralls.io/github/mandeep/Travis-Encrypt 
.. |dependencies| image:: https://img.shields.io/librariesio/github/mandeep/Travis-Client.svg
    :target: https://dependencyci.com/github/mandeep/Travis-Encrypt
.. |codacy| image:: https://img.shields.io/codacy/grade/16d519300c4d4524a38b385f6a7a2275.svg
    :target: https://www.codacy.com/app/bhutanimandeep/Travis-Encrypt/dashboard
.. |version| image:: https://img.shields.io/pypi/v/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |status| image:: https://img.shields.io/pypi/status/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |format| image:: https://img.shields.io/pypi/format/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |license| image:: https://img.shields.io/pypi/l/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt