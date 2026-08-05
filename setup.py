from setuptools import setup

# A valid, named setup.py alongside requirements.txt. Its only job here is to
# create the multi-manifest condition (two resolution paths: the repo root and
# requirements.txt) that TKA-10822 needs. It is intentionally NOT a bare
# setup.py (that is a different bug, TKA-10149) so it does not confound the repro.
setup(
    name="tka-10822-pipdeptree-urllib3-partial-scan",
    version="0.1.0",
    install_requires=["six>=1.10.0"],
)
