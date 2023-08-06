supervisor-logging-gelf
==================

A [supervisor] plugin to stream events to an external Graylog instance.

Installation
------------

```
pip install supervisor-logging-gelf
```

Usage
-----

The Graylog server to send the events to is configured with the environment
variables:

* `GRAYLOG_SERVER`
* `GRAYLOG_PORT`

You can set the variables up in the config below as well.

Add the plugin as an event listener in your main `supervisor.conf` of in a conf.d file like `/etc/supervisor/conf.d/logging.conf`:

```
[eventlistener:logging]
command = supervisor_logging_gelf
environment = GRAYLOG_SERVER=logs.myserver.com,GRAYLOG_PORT=12201
events = PROCESS_LOG
buffer_size = 1024
```

Enable the log events in your program:

```
[program:yourprogram]
stdout_events_enabled = true
stderr_events_enabled = true
```

[supervisor]: http://supervisord.org/
