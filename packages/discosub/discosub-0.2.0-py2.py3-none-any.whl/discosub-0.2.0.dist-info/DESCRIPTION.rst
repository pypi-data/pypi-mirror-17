==============
discosub 0.2.0
==============

Free and opensource subdomain scanner. Discosub is simple and faster
subdomain discover.

Discosub test if a list of subdomains exist via fuzzing on root domain.

Discosub use dictionaries for perform an analyze (BruteForce).

You can use discosub directly from a python interpreter, or use it
inside docker container.

You can perform an anonymous scanning directly by using a specific
`docker version <https://hub.docker.com/r/4383/discosub/tags/>`__ (alias
tor).

Different type of docker container are available: \* simple docker
container with discosub installed on \* `torified
(tor) <https://www.torproject.org/>`__ docker container with discosub
installed on (all discosub scanning connections use tor network)

For more details visit the `official webpage
project <https://4383.github.io/discosub/>`__.

Install from pypi
-----------------

.. code:: shell

    pip install -U discosub

Install as a docker container
-----------------------------

.. code:: shell

    docker pull 4383/discosub:latest

Install as an anonymous scanner (tor + docker)
----------------------------------------------

.. code:: shell

    docker pull 4383/discosub:tor

Install from sources
--------------------

.. code:: shell

    $ git clone https://github.com/4383/discosub
    $ cd discosub
    $ python setup.py install

Usages from a local installation (from pypi or from sources)
------------------------------------------------------------

.. code:: shell

    discosub run google.com

Usages inside a docker container
--------------------------------

.. code:: shell

    docker run -e "TARGET=google.com" 4383/discosub:latest

Usages as an anonymous scanner from docker container (using tor inside docker)
------------------------------------------------------------------------------

.. code:: shell

    docker run -e "TARGET=google.com" 4383/discosub:tor

Prerequistes
------------

-  python >= 2.6 (but prefer python3.x)

Features
--------

-  Analyze a root domain and discover its subdomains
-  Analyze domain over tor via specific docker container (anonymous
   scanning)

Advertissments
--------------

-  scan over docker container are more slowly than direct usage from
   python interpreter
-  scan over torified docker container are more slowly than direct usage
   from python interpreter and classical discosub docker container
-  scan over torified docker container are more verbose than an
   classical scanning (identifiable IP)

Guidelines
----------

-  Perform whois request on discovered subdomains

License
-------

-  Free software: GNU General Public License v3

Credits
-------

Author: 4383 (Hervé Beraud)

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
project template.


=======
History
=======

0.1.0 (2016-08-29)
------------------

* First release on Github.

0.1.6 (2016-08-31)
------------------

* First release on Pypi.
* Using click instead of argparse

0.1.10 (2016-08-31)
-------------------

* Dockerize app
* Stable pypi deployment via travis-ci

0.1.11 (2016-08-31)
-------------------

* Fix somes documentation mistakes and syntax error

0.1.12 (2016-08-31)
-------------------

* Fix somes documentation mistakes and syntax error
* Update pypi project classifiers

0.1.13 (2016-09-01)
-------------------

* Link official webpage with repo (pypi, github, docker)

0.1.14 (2016-09-01)
-------------------

* Fixing bad packaging. Error when loading dictionaries files.

0.1.15 (2016-09-01)
-------------------

* Fixing mistake on Dockerfile (docker run command)

0.1.16 (2016-09-02)
-------------------

* Apply Alpha development status for pypi classifiers
* Adding badges on README

0.2.0 (2016-09-03)
-------------------

* New docker tag for allow anonymous scanning. Integrate a second dockerfile for build a container where network connections are relayed per a tor client embdded inside this container.


