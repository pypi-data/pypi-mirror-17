# py-chillog

Python library for building logging data structure based on [GELF](http://docs.graylog.org/en/2.1/pages/gelf.html)


Installation
============

```shell
$ make install
```


Usage
=====

```python
from chillog.logger import Chillog

logger = Chillog()

# simple log
logger.info("Message")

# log with optional field(s) using kwargs
logger.info("Message", key_one="value_one", key_two="value_two")

# log with optional field(s) using dict
optional_fields = {
    "key_one": "value_one",
    "key_two": "value_two"
}

logger.info("Message", **optional_fields)  # notice `**` sign before `optional_fields` variable

# log with detailed message
logger.info("Message", full_message="More detailed message")
```

By default, this library will read value of environment variable with key `SERVICE_NAME` to fill `service` json field.
This library also read hostname using python native (`socket.gethostname()`).

Service name and hostname can overridden when initialisation Chillog object like example below

```python
from chillog.logger import Chillog

logger = Chillog(service_name="SERVICE_NAME", hostname="HOSTNAME")
```

There are 7 logger you can use:

- ``debug``
- ``info``
- ``notice``
- ``warning``
- ``error``
- ``critical``
- ``alert``

Output log:

```json
{
  "version": 1,
  "host": "HOSTNAME",
  "service": "SERVICE_NAME",
  "short_message": "log description",
  "full_message": "long log description if any",
  "timestamp": 1472009181293,
  "level": 1,
  "_additional_key": "additional value"
}
```

Running Test
============

```shell
$ make test
```
