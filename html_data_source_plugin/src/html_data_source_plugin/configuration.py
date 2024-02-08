import os
from typing import Any

import toml

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def create_default_configuration() -> dict[str, Any]:
    default_config = {
        'url': 'http://www.scrapethissite.com',
        'node_cap': 20
    }

    with open(os.path.join(__location__, 'config.toml'), 'w') as f:
        toml.dump(default_config, f)

    return default_config


def marshall_configuration(config: dict[str, Any]):
    with open(os.path.join(__location__, 'config.toml'), 'w') as f:
        toml.dump(config, f)


def unmarshall_configuration() -> dict[str, Any]:
    with open(os.path.join(__location__, 'config.toml'), 'r') as f:
        config = toml.load(f)

    return config
