try:
    from setuptools import setup, find_packages
except: 
    from distutils.core import setup

setup(
    name = "spreadsheet_maker",
    version = '1.0',
    packages = find_packages(),
    requires = [],
    author = "Andrew Babenko",
    author_email = "andruonline11@gmail.com",
    description = "Simple framework to create Google Spreadsheet with python",
    long_description = open('README').read(),
    license = "LICENSE",
    keywords = "'google-spreadsheet', 'spreadsheet', 'create-google-spreadsheet'",
    url = "https://github.com/HolmesInc/spreadsheet_maker.git",
    include_package_data = True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
)