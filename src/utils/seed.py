import random

import numpy as np


def set_seed(seed: int) -> None:
    """Set global random seeds for reproducibility.

    This covers Python's built-in random module and NumPy, which are used
    by most sampling and evaluation utilities in this framework.

    Note: LLM-level seeds are separate. They are passed per-request via
    GenerationConfig.seed directly to the Ollama backend. This function
    does NOT control what the model outputs — it controls everything else
    (e.g. random sampling in evaluation, shuffling agent order, etc.).

    Args:
        seed: Integer seed value. Use the same seed across runs to get
              identical non-LLM behavior.
    """
    random.seed(seed)
    np.random.seed(seed)
