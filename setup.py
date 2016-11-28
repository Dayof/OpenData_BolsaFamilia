from setuptools import setup

setup(
    name='bf',
    packages=['bf'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'unitest',
    ],
)
