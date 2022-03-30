"""Configurators for sensitive data logging."""

from logging.config import DictConfigurator as BaseDictConfigurator

from .loggers import SensitiveDataLogger


class DictConfigurator(BaseDictConfigurator):

    """Subclass of logging.config.DictConfigurator which configures SensitiveDataLogger specific variables."""

    def common_logger_config(self, logger, config, incremental=False):
        """If configured logger is instance of SensitiveDataLogger, set sensitive_data_in_extra and sensitive_data_in_message attributes."""
        super().common_logger_config(logger, config, incremental)
        if isinstance(logger, SensitiveDataLogger):
            logger.sensitive_data_in_extra = set(config.get('sensitive_data_in_extra', []))
            logger.sensitive_data_in_message = config.get('sensitive_data_in_message', False)
