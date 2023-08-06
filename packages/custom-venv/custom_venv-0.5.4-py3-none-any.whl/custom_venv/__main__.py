"""Main.
"""
import sys
from . import main

try:
    sys.exit(main())
except Exception as exception:  # pylint: disable=broad-except
    print('Error: %s' % exception, file=sys.stderr)
