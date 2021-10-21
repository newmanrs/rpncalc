from setuptools import setup

setup(
    name='rpncalc',
    version='0.0.1',
    py_modules=['rpncalc'],
    packages=['rpncalc'],
    install_requires=['numpy'
    ],
    entry_points={
        'console_scripts': [
            'rpncalc=rpncalc.rpncalc:main',
        ],
    },
)
