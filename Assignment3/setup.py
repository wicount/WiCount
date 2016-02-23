import sys
from setuptools import setup

setup(
    name = "Assignment3",        # what you want to call the archive/egg
    version = "0.1",
    packages=["src"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author="Velda Conaty",
    author_email = "velda.conaty@ucdconnect.ie",
    description = "Organise seats in an auditorium",
    license = "BSD",
    keywords= "auditorium",
    url = "http://",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "sample_python_prog = src.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
