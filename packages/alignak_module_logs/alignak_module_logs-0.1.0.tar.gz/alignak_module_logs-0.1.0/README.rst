Alignak Log Module
==================

*Alignak module for the monitoring logs*

Build status (stable release)
-----------------------------

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-log.svg?branch=master
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-log


Build status (development release)
----------------------------------

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-log.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-log


Short description
-----------------

This module for Alignak collects the monitoring logs (alerts, notifications, ...) to log them into a dedicated file.

You can plainly use the powerful of the Python logging system thanks to the use of a logging configuration file which will allow you to define when, where and how to send the monitoring logs ...

Known issues
------------
This module is not compatible with Python 2.6 if you intend to use a logger configuration file as this feature is not available before Python 2.7 version.
If you are still using the old 2.6 version, upgrade or define the logger parameters in the module configuration file.

Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-logs.cfg*. This file is commented to help configure all the parameters.

To configure Alignak broker to use this module:

    - edit your broker daemon configuration file
    - add the `module_alias` parameter value (`logs`) to the `modules` parameter of the daemon

To set up several logs collectors:

    - copy the default configuration to another file,
    - change the module alias parameter (`logs_bis`)
    - edit your broker daemon configuration file
    - add the new `module_alias` parameter value (`logs_bis`) to the `modules` parameter of the daemon


Bugs, issues and contributing
-----------------------------

Please report any issue using the project `GitHub repository: <https://github.com/Alignak-monitoring-contrib/alignak-module-log/issues>`_.

License
-------

Alignak Backend Modules is available under the `GPL version 3 <http://opensource.org/licenses/GPL-3.0>`_.

