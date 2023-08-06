
#!/usr/bin/env python3
import sys
from setuptools import setup

if sys.version_info < (3, 8):
    print("Python 3.8 or higher is required - earlier python 3 versions may work but were not tested.")
    sys.exit(1)
setup(
    author='Yazhou He',
    author_email='yhe@irishfilm.ie',
    long_description=("""\
Scripts for use in the IFI Irish Film Archive. It is used for ingest strongbox csv report autmatically
"""),
    scripts=[
        'strongbox_csv.py'
    ],
    install_requires=[
        'datetime',
        'keyboard',
        'selenium',
        'webdriver_manager',
        'packaging'
    ],
    name='strongbox_csv',
    version='2022.11.25.1',
    python_requires='>=3.8'
)
