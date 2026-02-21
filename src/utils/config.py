from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file and return it as a plain dict.

    All experiment parameters (model, agents, rounds, topic, seed) live
    in YAML files rather than in source code. This means you can run a
    different experiment by changing a file, not by changing code.

    Args:
        path: Path to the .yaml config file.

    Returns:
        Parsed config as a nested dict.

    Raises:
        FileNotFoundError: If the config file does not exist at the given path.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
