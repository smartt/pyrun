pyrun
=====

Python library for loading and running arbitrary Python packages based on string representations of the package and function names, like this:

```
from pyrun import runner

runner.run(package='scripts/hello', function='run')

```
