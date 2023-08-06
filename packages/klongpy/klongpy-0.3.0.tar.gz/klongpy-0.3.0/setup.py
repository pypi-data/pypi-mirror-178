from setuptools import setup

setup(
    name='klongpy',
    packages=['klongpy'],
    version='0.3.0',
    description='Python implementation of Klong language.',
    author='Brian Guarraci',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.1'],
    test_suite='tests',
)
