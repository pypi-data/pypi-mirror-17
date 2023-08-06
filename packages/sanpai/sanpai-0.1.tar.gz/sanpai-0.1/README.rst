sanpai
======

Sanpai is a tool for inspecting and diffing SANs on x509 certificates.


Modules
-------
For converting a directory to a dict, use convert_dir:

.. code-block:: python

    >>> from sanpai import san
    >>> domains = san.inspect(pem_file="path/to/cert.pem")
    >>> type(domains)
    <type 'list'>


Scripts
-------
From command line, retrieve newline-separated list of domains attached to a cert:

.. code-block:: bash

    $ sanpai /path/to/cert.pem
    subdomain.example.com
    example.org
    *.wilcard.io

Compare two certs:

.. code-block:: bash

    $ sanpai /path/to/cert1.pem --diff /path/to/cert2.pem
    - subdomain.example.com
    + www.example.org
    ! example.org
    ...


Installation
------------
To install Sanpai, simply:

.. code-block:: bash

    $ pip install sanpai
