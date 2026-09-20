"""Module entry point: ``python -m tc_fitness`` runs the same gate as the script.

The ``tc-fitness`` console script is resolved from the environment's bin
directory and therefore runs whatever is *installed*. Invoking the package as a
module instead resolves it through the caller's import path, so a caller can
execute the candidate it is actually testing rather than a copy that may differ
from it.
"""

from __future__ import annotations

import sys

from tc_fitness.gate import main

if __name__ == "__main__":
    sys.exit(main())
