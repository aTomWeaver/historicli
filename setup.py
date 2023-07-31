import setuptools

setuptools.setup(
        name='when',
        version='1.0',
        description='a simple cli timeline app for historical events',
        author='Tom Weaver',
        packages=setuptools.find_packages(),
        install_requires=['click', 'termcolor', 'colored_traceback']
        )
