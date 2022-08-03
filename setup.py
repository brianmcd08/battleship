try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A battleship game'
LONG_DESCRIPTION = 'Based on the class battleship game'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="battleship-game",
    version=VERSION,
    author="Brian McDowell",
    author_email="<brianmcd08@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'battleship'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
