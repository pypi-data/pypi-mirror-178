from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = "0.0.1"
DESCRIPTION = "A geospatial tool package for processing geospatial data without using GDAL"
LONG_DESCRIPTION = "Under Construction."

# Wheel building cmd
"""
python setup.py sdist bdist_wheel
"""

# Upload the package
"""
twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*
"""

# Setting up
setup(
    name="nogdal",
    version=VERSION,
    author="Weixing Zhang",
    author_email="weixing.zhang365@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["numpy"],
    keywords=["python", "geospatial", "gis", "remote sensing"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={  # Optional
        "console_scripts": [
            "nogdal=nogdal:main",
        ],
    }
)