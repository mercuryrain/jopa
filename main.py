import fire

from config import load_config, validate_config
from executor import Executor

if __name__ == '__main__':
    config = load_config()

    validate_config(config)
    executor = Executor(config)

    fire.Fire(executor)
