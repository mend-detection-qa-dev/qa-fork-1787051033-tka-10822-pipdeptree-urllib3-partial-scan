from setuptools import setup

# A valid, named setup.py alongside requirements.txt, kept per TKA-10822 (the
# customer's repo contains BOTH requirements.txt and setup.py, and setup.py resolved
# cleanly in their scan).
#
# It declares a real, importable package (`tka10822_probe`) via `packages=[...]`.
# The previous version was a stub with no packages/py_modules: `pip install .` then
# produced an empty distribution, and Mend reported the project's own dist as an
# unresolved dependency of itself -> a spurious FILE_PARSING WARN
# ("Failed to resolve [tka-10822-pipdeptree-urllib3-partial-scan-0.1.0]"). With a real
# package, `pip install .` yields a resolvable distribution and the repo-root RESOLUTION
# path completes clean (no warning in scaResults).
#
# Still intentionally NOT a bare setup.py (that is a different bug, TKA-10149).
setup(
    name="tka-10822-pipdeptree-urllib3-partial-scan",
    version="0.1.0",
    packages=["tka10822_probe"],
    install_requires=["six>=1.10.0"],
)
