from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Simple Math Package"
LONG_DESCRIPTION = "My first Python package with a slightly longer description"

# Setting up
setup(
    name = "mathmodule-rickwang577",
    version = VERSION,
    author = "Rick Wang",
    author_email = "yenhao0508@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packges = find_packages(),
    install_requires = [],                  
    # add additional packages if needs to be installed along with your package
    
    keywords = ["python", "first package"],
    classifiers = [
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)