from setuptools import setup

setup(
    name='dsprovgen',
    version='0.1',
    packages=['dsprovgen'],
    author='Filip Krikava',
    author_email='filip.krikava@inria.fr',
    description='A script for generating devstack provisioning using various tools',

    requires=['PyYAML (>=3.0)'],

    entry_points={
        'console_scripts': ['dsprovgen = dsprovgen:main']
    }
)
