#!/usr/bin/env python
import os
import sys

# Force our parent directory (the `pyrun` package) into python path:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runner import run

# --------------------------------------------------
if __name__ == "__main__":
    print("########################")
    print("Running a script...\n")
    run(package='scripts/hello', function='run', path_extras=["scripts"], verbose=True)

    print("\n########################")
    print("Calling a model method...\n")
    run(package='models/hello', model='Hello', method='hi', verbose=True)

    print("\n########################")
    print("Done.")

