from setuptools import setup

setup(
    name = 'tp_extract',
    version = '0.1.0',
    packages = ['tp_extract'],
    entry_points = {
        'console_scripts': [
            'tp_extract = tp_extract.__main__:main'
        ]
    })