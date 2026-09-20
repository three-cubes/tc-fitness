#!/usr/bin/env python3
import sys
from pathlib import Path

Path(sys.argv[1]).write_text("produced\n")
