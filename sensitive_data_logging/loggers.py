"""Loggers for sensitive data logging."""

import collections
import logging
from typing import Set


class SensitiveDataLogger(logging.Logger):

    """Sensitive data logger"""

    sensitive_data_in_extra: Set[str] = frozenset()
    sensitive_data_in_message: bool = False
    message_moved_placeholder = '[Message moved to sensitive_data]'

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, sensitive_data=None):
        """Fill sensitive_data key of extra with sensitive data from different sources.

        Move whole message of log to sensitive_data when sensitive_data_in_message is True.
        Move data from extra with keys specified in sensitive_data_in_extra to sensitive_data.
        Add content of kwarg sensitive_data to sensitive_data dict.
        """
        new_extra = {
            'sensitive_data': {},
        }

        if sensitive_data is not None:
            new_extra['sensitive_data'].update(sensitive_data)

        if extra:
            for key in extra.keys():
                if key in self.sensitive_data_in_extra:
                    new_extra['sensitive_data'][key] = str(extra[key])  #logstash requires JSON serializable value
                else:
                    new_extra[key] = extra[key]

        if self.sensitive_data_in_message:
            # Logic moved from LogRecord class used to prepare log message
            if (args and len(args) == 1 and isinstance(args[0], collections.Mapping) and args[0]):
                args = args[0]
            new_extra['sensitive_data']['message'] = msg % args
            msg = self.message_moved_placeholder
            args = ()

        super()._log(level=level, msg=msg, args=args, exc_info=exc_info, extra=new_extra, stack_info=stack_info)
