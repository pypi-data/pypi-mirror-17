check_mysql_slave
#################

Check MySQL seconds behind master for Nagios-like monitoring.

Usage
-----

.. code:: shell

    $ check_mysql_slave --help
    usage: check_mysql_slave [-h] -u [USER] -p [PASSWORD] [--host [HOST]]
                             [--port PORT]
                             [warning_threshold] [critical_threshold]

    positional arguments:
      warning_threshold     Warning threshold (defaults to 60)
      critical_threshold    Critical threshold (defualts to 300)

    optional arguments:
      -h, --help            show this help message and exit
      -u [USER], --user [USER]
                            Login username
      -p [PASSWORD], --password [PASSWORD]
                            Login password
      --host [HOST]         Login host
      --port PORT           Login port

License
-------

This software is licensed under the MIT license (see the :code:`LICENSE.txt`
file).

Author
------

Nimrod Adar, `contact me <nimrod@shore.co.il>`_ or visit my `website
<https://www.shore.co.il/>`_. Patches are welcome via `git send-email
<http://git-scm.com/book/en/v2/Git-Commands-Email>`_. The repository is located
at: https://www.shore.co.il/git/.
