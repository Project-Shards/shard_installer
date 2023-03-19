import logging
import logging.config
import yaml

def setup_logging():

    logging_config = """
version: 1

formatters:
    simple:
        format: "%(name)s - %(lineno)d -  %(message)s"

    complex:
        format: "%(asctime)s - %(name)s - %(lineno)d -  %(message)s"


handlers:
    console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple

    file:
        class: logging.handlers.TimedRotatingFileHandler
        when: midnight
        backupCount: 5
        level: DEBUG
        formatter: simple
        filename : shard_installer.log

loggers:

    shard_logging:
        level: DEBUG
        handlers: [console,file]
        propagate: yes

    __main__:
        level: DEBUG
        handlers: [console]
        propagate: yes

    """

    config = yaml.safe_load(logging_config)
    logging.config.dictConfig(config)
    return logging.getLogger("shard_logging")
