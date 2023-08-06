===============
poor-smime-sign
===============

.. image:: https://img.shields.io/pypi/v/poor-smime-sign.svg
        :target: https://pypi.python.org/pypi/poor-smime-sign

.. image:: https://img.shields.io/travis/seporaitis/poor-smime-sign.svg
        :target: https://travis-ci.org/seporaitis/poor-smime-sign


A very poor tool to generate S/MIME signatures for arbitrary content & probably insecurely too.

A quick example:

.. code-block:: python

    >>> smime_sign(
    ...     signer_cert_path="/path/to/files/signer.cert",
    ...     signer_key_path="/path/to/files/signer.pem",
    ...     recipient_cert_path="/path/to/files/recipient.cert",
    ...     content="test",
    ...     output_format="PEM",
    ... )

Features
--------

* Does S/MIME signatures.
* Verifies S/MIME signatures.


Why?
--------

This utility library has single purpose - provide support for making
S/MIME signatures on Python2 **and 3**, which currently lacks any
proper libraries for that purpose.

The main use case it is built for: at work our system has to generate
Apple Passbook Pass files, which include an S/MIME
signature. Currently it is done using ``M2Crypto.SMIME``. While that
works - we want to migrate to Python3, and unfortunately for us
``M2Crypto`` is not fully supported. ``smime_sign`` is a poor man's
solution for this problem.

Internally this does nothing more than call `openssl smime`_, so you
might want to see its docs too.

.. _openssl smime: https://www.openssl.org/docs/manmaster/apps/smime.html


Why not?
--------

* This may be insecure.
* This may be slow if you are signing large blobs of text.


API
===

``smime_sign(signer_cert_path, signer_key_path, cert_path, recipient_cert_path, content, output_format)``
---------------------------------------------------------------------------------------------------------

Generates and returns signature string for ``content`` in
``output_format``.

All ``*_path`` arguments must be absolute
paths.

``content`` must be a string, not a path.

Example to generate signature for Passbook manifest:

.. code-block:: python

    >>> manifest_json = "..."  # JSON string with `manifest.json` content
    >>> signature = smime_sign(
    ...     signer_cert_path="/path/to/files/signer.cert",
    ...     signer_key_path="/path/to/files/signer.pem",
    ...     cert_path="/path/to/files/intermediate.cert",
    ...     recipient_cert_path=None,
    ...     content=manifest_json,
    ...     output_format="DER",
    ... )

``smime_verify(signer_cert_path, content_path, signature_path, signature_format)``
----------------------------------------------------------------------------------

Verifies a ``content_path`` file against a signature at ``signature_path``.

Note: this function was added to help in the tests only.


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage




History
-------

2.0.3 (2016-09-13)
------------------

* Change the licence from ``AGPLv3`` to ``MIT``.

2.0.2 (2016-01-07)
------------------

* Fix documentation rendering on PyPI

2.0.1 (2016-01-07)
------------------

* Added support for passing intermediate certificates.
* Made recipient certificate optional.
* Argument structure for ``smime_sign`` has changed, therefore major version bump-up.


1.0.0 (2015-11-27)
------------------

* First release on PyPI.


