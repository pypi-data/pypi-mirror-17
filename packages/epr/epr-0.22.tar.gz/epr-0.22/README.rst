# EPR #

Easy debug printing

### Example usage ###

```python
from epr import epr
epr(some_object, 'red')

# auto including

This script will automatically include epr in all python files which attempt to
use it:

```python
from epr import epr_include_recursive
epr_include_recursive(path)
