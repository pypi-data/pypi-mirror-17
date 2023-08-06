===========================
helga-api-monitor
===========================

Allow helga a way to monitor APIs

Installation
============

After installing and configuring helga, use::

    pip install helga-api-monitor

Add to your settings if necessary and restart helga::

    'api_monitor',

Add the following settings::

    API_MONITOR_URL = 'http://www.example.com/'
    API_MONITOR_ENDPOINT = 'http://www.example.com/api/'
    API_MONITOR_CHANNEL = '#bots'
    API_MONITOR_INTERVAL = 2 # minutes

Usage
=====

To initialize the monitor after starting helga, you must first trigger the watching with::

    !api_monitor

This will start a regular job to poll endpoints for errors

License
=======

Copyright (c) 2016 Jon Robison

See included LICENSE for licensing information
