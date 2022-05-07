def get_logger(name, level=None):
    """
    Get a logger with the given name and level.
    """
    import logging
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger


def get_config(config_file):
    """
    Get the config from the given file.
    """
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_report_dir(config):
    """
    Get the report directory from the given config.
    """
    return config['report']['report_dir']
