# Sensitive Data Logging

Utils for handling sensitive data in logs.

## Setup

After installing package to use it's features you need to set default logger and dict configurator class.

Before using and configuring loggers set this things up:
```python
import logging
import logging.config

from sensitive_data_logging.loggers import SensitiveDataLogger
from sensitive_data_logging.configurators import DictConfigurator


logging.setLoggerClass(SensitiveDataLogger)
logging.config.dictConfigClass = DictConfigurator
```

## Configuration

Logger supplied by this package relies on logging dict configuration. In your configuration dict set (or not) variables `sensitive_data_in_extra` and `sensitive_data_in_message`.
They can be used in every logger we want to secure, and event in `root` logger.

`sensitive_data_in_extra` - is list of keys which supplied in loggers `extra` data should be moved to sensitive_data
`sensitive_data_in_message` - is bool whether move loggers message to sensitive_data or not

```python
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    ...
    'loggers': {
        'first_logger': {
            'handlers': ['console'],
        },
        'second_logger': {
            'handlers': ['console'],
            'sensitive_data_in_extra': ['phone_number'],  # Key 'phone_number' from extra data will be moved to sensitive_data
        },
        'third_logger': {
            'handlers': ['console'],
            'sensitive_data_in_message': True,  # Whole message and args will be moved to sensitive_data
        },
    },
})
```

You can also use `sensitive_data_logging.formatters.SensitiveDataFormatter` in development environments to prepend sensitive_data to logged message.

## Use of logger

With `sensitive_data_logging.loggers.SensitiveDataLogger` set as default you can use additional keyword argument when logging to explicitly supply sensitive_data:
```python
logger.info('Some log', sensitive_data={'secret': 'value'})
```

## License
The Sensitive Data Logging package is licensed under the [FreeBSD
License](https://opensource.org/licenses/BSD-2-Clause).
