Alignak External commands Module
================================

*Alignak external commands module*

Build status (stable release)
-----------------------------

.. image:: https://travis-ci.org/Alignak-monitoring/alignak-module-external-commands.svg?branch=master
    :target: https://travis-ci.org/Alignak-monitoring/alignak-module-external-commands


Build status (development release)
----------------------------------

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-external-commands.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-external-commands


Short description
-----------------

This module is an example skeleton to build Alignak modules ...


Installation
------------

From PyPI
~~~~~~~~~
To install the module from PyPI:
::

    pip install alignak-module-external-commands


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files:
::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-module-external-commands
    cd alignak-module-external-commands
    pip install -r requirements
    python setup.py install


Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-external-commands.cfg*. This file is commented to help configure all the parameters.

To configure an Alignak daemon to use this module:

    - edit your daemon configuration file
    - add your module alias value (`external-commands`) to the `modules` parameter of the daemon


Bugs, issues and contributing
-----------------------------

Please report any issue using the project `GitHub repository: <https://github.com/Alignak-monitoring-contrib/alignak-module-external-commands/issues>`_.

License
-------

Alignak Module External commands is available under the `GPL version 3 license`_.

.. _GPL version 3 license: http://opensource.org/licenses/GPL-3.0
.. _Alignak monitoring contrib: https://github.com/Alignak-monitoring-contrib
.. _PyPI repository: <https://pypi.python.org/pypi>
