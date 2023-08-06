from distutils.core import setup

from setuptools import find_packages

setup(
    name='kfk_vvvvvvvvv',
    version='0.1.1',
    install_requires=[
        "kafka-python",
        "rich"
    ],
    packages=find_packages(),
    author='vova',
    entry_points={
        'console_scripts': [
            'kfk = kfk.main:main',
        ]
    }
)
