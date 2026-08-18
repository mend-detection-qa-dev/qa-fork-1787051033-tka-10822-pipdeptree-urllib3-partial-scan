"""Minimal real package so `pip install .` produces a resolvable distribution.

Its existence (not its content) is what matters: a stub setup.py with no packages
built an empty dist that Mend reported as an unresolved dependency of itself. See
../setup.py for the full rationale (TKA-10822 probe self-flag fix).
"""

__version__ = "0.1.0"
