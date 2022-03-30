"""Test for sensitive data logging"""

import logging
import logging.config

from sensitive_data_logging.loggers import SensitiveDataLogger
from sensitive_data_logging.configurators import DictConfigurator


logging.setLoggerClass(SensitiveDataLogger)
logging.config.dictConfigClass = DictConfigurator
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'class': 'sensitive_data_logging.formatters.SensitiveDataFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'first_logger': {
            'handlers': ['console'],
        },
        'second_logger': {
            'handlers': ['console'],
            'sensitive_data_in_extra': ['phone_number'],
        },
        'third_logger': {
            'handlers': ['console'],
            'sensitive_data_in_message': True,
        },
        'fourth_logger': {
            'handlers': ['console'],
            'sensitive_data_in_extra': ['last_name'],
            'sensitive_data_in_message': True,
        },
    },
})


def test_logging_without_sensitive_data(caplog):
    """Test behaviour of logger and formatter when no sensitive data is supplied nor configured."""
    logger = logging.getLogger('first_logger')

    logger.info('This log has no %s data', 'sensitive')

    log_record = caplog.records[0]

    assert log_record.message == "[sensitive_data={}] This log has no sensitive data"
    assert log_record.sensitive_data == {}


def test_logging_with_explicitly_supplied_sensitive_data(caplog):
    """Test behaviour of logger and formatter when sensitive data is supplied to logger by sensitive_data kwarg."""
    logger = logging.getLogger('first_logger')

    logger.info('This log explicitly supplied sensitive data', sensitive_data={'secret': 'confidential'})

    log_record = caplog.records[0]

    assert log_record.message == "[sensitive_data={'secret': 'confidential'}] This log explicitly supplied sensitive data"
    assert log_record.sensitive_data == {'secret': 'confidential'}


def test_logging_with_configured_which_extra_is_sensitive_data(caplog):
    """Test behaviour of logger and formatter when sensitive data is configured as some key from extra."""
    logger = logging.getLogger('second_logger')

    logger.info('Client called!', extra={'first_name': 'Marek', 'phone_number': '+48698800200'})

    log_record = caplog.records[0]

    assert log_record.message == "[sensitive_data={'phone_number': '+48698800200'}] Client called!"
    assert log_record.first_name == 'Marek'
    assert not hasattr(log_record, 'phone_number')
    assert log_record.sensitive_data == {'phone_number': '+48698800200'}


def test_logging_with_configured_sensitive_data_in_message(caplog):
    """Test behaviour of logger and formatter when sensitive data is configured as whole message of logger."""
    logger = logging.getLogger('third_logger')

    logger.info('Client called (first_name=%s, phone_number=%s)!', 'Marek', '+48698800200')

    log_record = caplog.records[0]

    assert log_record.message == (
        "[sensitive_data={'message': 'Client called (first_name=Marek, phone_number=+48698800200)!'}]"
        " [Message moved to sensitive_data]"
    )
    assert log_record.args == ()
    assert log_record.sensitive_data == {
        'message': 'Client called (first_name=Marek, phone_number=+48698800200)!',
    }


def test_logging_with_configured_sensitive_data_in_message_and_in_extra_and_explicitly_supplied(caplog):
    """Test behaviour of logger and formatter when sensitive data is configured as whole message, key in extra and supplied explicitly."""
    logger = logging.getLogger('fourth_logger')

    logger.info(
        'Client called (first_name=%s, phone_number=%s)!',
        'Marek',
        '+48698800200',
        extra={'last_name': 'Nowak'},
        sensitive_data={'secret_key': '21key3secret7'},
    )

    log_record = caplog.records[0]

    assert log_record.message == (
        "[sensitive_data={'secret_key': '21key3secret7', 'last_name': 'Nowak',"
        " 'message': 'Client called (first_name=Marek, phone_number=+48698800200)!'}]"
        " [Message moved to sensitive_data]"
    )
    assert log_record.args == ()
    assert not hasattr(log_record, 'last_name')
    assert log_record.sensitive_data == {
        'secret_key': '21key3secret7',
        'last_name': 'Nowak',
        'message': 'Client called (first_name=Marek, phone_number=+48698800200)!',
    }
