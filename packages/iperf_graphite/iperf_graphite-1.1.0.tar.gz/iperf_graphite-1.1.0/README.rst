iperf_graphite
==============

|PyPi Status|

Run bi-directional iperf3 tests and send results to Graphite.
Results include bps and retransmits

Installation
------------

.. code:: bash

    pip install iperf_graphite

Usage
-----

.. code:: bash

    $ iperf_graphite --help
    usage: iperf_graphite [-h] [-f CONFIG_FILE] [-V]

    send iperf stats to graphite

    optional arguments:
      -h, --help      show this help message and exit
      -f CONFIG_FILE  Config file
      -V, --version   show program's version


Sample config file:

.. code:: bash

    # Configuration for iperf-graphite.py

    # Graphite details
    carbon_server: myserver.example.net
    carbon_port: 2003
    data_point_prefix: "test.iperf"

    # Iperf options
    iperf_port: 5201
    iperf_test_duration: 10

    # Sleep time (seconds) between tests
    sleep: 0

    # List of tests to iterate over
    tests:
      - src: 192.0.2.1
        dst: 192.0.2.2
      - src: 1.2.3.4
        dst: 5.6.7.8


Authors
-------
Carlos Vicente (<cvicente@dyn.com>)

.. |PyPi Status| image:: https://img.shields.io/pypi/v/iperf_graphite.svg
   :target: https://pypi.python.org/pypi/iperf3_graphite
