import logging
import logging.config
import yaml

def setup_logging():
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        f.close()

    logging.config.dictConfig(config)
    return logging.getLogger("shard_logging")
