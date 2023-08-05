import setuptools

__name__ = "Mycol"
__version__ = "0.0.1"
__description__ = "Collection of random functions"
__author__ = "Matti"
__email__ = "877cmatt@gmail.com"
__url__ = "https://github.com/Mattimated/my"

setuptools.setup(
    name=__name__, 
    version=__version__, 
    author=__author__, 
    author_email=__email__, 
    description=__description__, 
    url=__url__, 
    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language : Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ]
)