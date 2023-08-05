sealights-python-agent
================

sealights-python-agent is a plugin for py.test that integrates with the Sealights platform.


Requirements
------------

You will need the following prerequisites in order to use sealights-python-agent:

- pytest


Installation
------------

To install sealights-python-agent::

    $ pip install sealights-python-agent

Then run your tests with::

    $ py.test --customer_id <customer_id> --app_name <app_name> --server https://prod-sealights-gw.sealights.co/api


If you would like to run tests without sealights-python-agent, use::

    $ py.test -p no:sealights-python-agent