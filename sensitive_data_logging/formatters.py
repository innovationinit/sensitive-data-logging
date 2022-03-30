"""Formatters for sensitive data logging."""

import logging


class SensitiveDataFormatter(logging.Formatter):

    """Log Formatter class to prepend sensitive data to message"""

    def format(self, record: logging.LogRecord) -> str:
        """Override message with sensitive data info"""
        if not getattr(record, 'sensitive_data_added_to_message', False):
            try:
                record.msg = "[sensitive_data=%s] %s" % (record.sensitive_data or '{}', record.msg or '')
                record.sensitive_data_added_to_message = True
            except AttributeError:
                pass
        return super().format(record)
