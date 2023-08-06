from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Adds new data types to your python project'
LONG_DESCRIPTION = 'Create new data types using this module, adds 6 new data types in your project, create questions, calculator and much more using this module'

# Setting up
setup(
    name="newdatatypes-1.0.0",
    version=VERSION,
    author="Technology Power (Bhargav Raj)",
    author_email="technologypower24@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'newdatatypes'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
