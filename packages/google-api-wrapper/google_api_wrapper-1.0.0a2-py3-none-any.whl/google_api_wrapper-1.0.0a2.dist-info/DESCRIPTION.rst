===================
Google APIs Wrapper
===================

Overview
--------

This package provides a simple wrapper around Google APIs such as
Cloud Compute, IAM, Deployment Manager, and other cloud-related APIs.

It is used internally by Infolinks for provisioning and deployments, and has proven useful, so we've decided to
share it! Note that this is still work in progress - our internal version is currently more comprehensive in its
coverage of Google's APIs than this version; we will slowly transition more & more APIs from our internal version to
this open version, so stay tuned!

NOTE: Google APIs wrapper requires Python 3.5 and above.


Installation
------------

Installing this package from PyPy is simple, using ``pip``::

    pip install google-api-wrapper

You can add the ``--upgrade`` or ``-U`` flag to upgrade it if you already
have it installed.

Building
--------

Google APIs wrapper requires Python 3.5 and above. This is a hard requirement
unfortunately. That aside, however, building it is fairly simple - you just
use ``pyvenv`` and ``pip install -e``.

We recommend reading `Packaging Guide <https://packaging.python.org/distributing/>`_
and the `Virtual Environments Guide <https://docs.python.org/3/library/venv.html>`_,
but we've compiled a simple & quick how-to for your convenience:

1. Clone the repository::

    git clone git@bitbucket.org:infolinks/google-api-wrapper.git

2. Set up a virtual environment::

    pyvenv <virtual-env-directory>

3. Activate the virtual environment (once for every shell/terminal you will be
   using to build or develop in it)::

    source <virtual-env-directory>/bin/activate

4. Install the cloned copy of the source code using::

    pip install -e <git-checkout-of-google-api-wrapper>

5. You can now modify the source code freely.

6. When you want to test it, simple run your Python program which will import
   the ``googleapiwrapper`` package inside it.

7. To create a distribution package (not to be confused with a Python source package!) use this command::

    python setup.py sdist bdist_wheel

8. Now that we've created the distributions, we need to ensure we are able to upload our package to PyPi. To do this,
   ensure you have an account over at `PyPi <https://pypi.python.org>`_ as well as at
   `PyPi Testing <https://testpypi.python.org>`_. We will be using `Twine <https://pypi.python.org/pypi/twine>`_ to
   perform the upload.

9. Ensure you've created the ``~/.pypirc`` file, which should look like this (don't forget to fill-in your credentials
   inside it!)::

    [distutils]
    index-servers=
        pypi
        pypitest

    [pypitest]
    repository = https://testpypi.python.org/pypi
    username = <username>
    password = <password>

    [pypi]
    repository = https://pypi.python.org/pypi
    username = <username>
    password = <password>

10. The project needs to be registered with PyPi (to reserve the package name). **Note that this only needs to be done
    once in the project's lifetime, and has already been done for you! you DO NOT need to run this!**. But for
    documentational purposes, here is the command to do it::

    twine register --repository pypitest dist/google_api_wrapper-<version>-py3-none-any.whl
    twine register --repository pypi dist/google_api_wrapper-<version>-py3-none-any.whl

11. Now we can upload the package. We recommend first uploading it to the `PyPi Testing <https://testpypi.python.org>`_
    package index in order to verify it's working properly. Here's how::

    twine upload --repository pypitest dist/*
    twine upload --repository pypi dist/*


APIs
----

The package's entry point to the APIs is the ``Cloud`` module. This module contains a
single class - the ``Cloud`` class, which you create an instance of using a Google
Cloud JSON credentials file (usually generated from a service account) and one or more
scopes (scopes are essentially the list of permissions you are requesting to use). By
default, if you do not provide any scopes, the framework will ask for the
``https://www.googleapis.com/auth/cloud-platform`` scope which means full permissions.
Narrow it down to request more specific permissions instead.

Once you have an instance of the ``Cloud`` class, it can provide you with more specific
Google Cloud API wrappers:

* Compute: this API contains Google Compute APIs such as creating disks & instances,
  modifying instance group members, etc.

* IAM: this API is used for managing user and service accounts. Not implemented yet.

* Deployment Manager: this API is used for managing deployments using the Google Deployment
  manager service. Not implemented yet.

* More to come (Network, Pub/Sub, etc)


