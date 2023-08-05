import setuptools

__name__ = "Mycol"
__version__ = "0.0.2"
__description__ = "Collection of random functions"
__author__ = "Matti"
__email__ = "877cmatt@gmail.com"
__homepage__ = "https://github.com/Mattimated/my"
__bug_tracker__ = "https://github.com/Mattimated/my/issues"

setuptools.setup(
    name=__name__, 
    version=__version__, 
    author=__author__, 
    author_email=__email__, 
    description=__description__, 
    url=__homepage__, 
    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language : Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ]
)