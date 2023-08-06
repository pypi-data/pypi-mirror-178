from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A handy geospatial tool package for processing geospatial data"
LONG_DESCRIPTION = "Under Construction."

# Build Wheel CMD 
"""
python setup.py sdist bdist_wheel
""" 

# Setting up
setup(
    name="geodummy",
    version=VERSION,
    author="Weixing Zhang",
    author_email="weixing.zhang365@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["gdal", "numpy"],
    keywords=["python", "geospatial", "gis", "remote sensing"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)