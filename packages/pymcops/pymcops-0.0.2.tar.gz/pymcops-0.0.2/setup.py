from setuptools import setup, find_packages
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
README_FILE = os.path.join(PROJECT_ROOT, "README.md")

VERSION = '0.0.2'

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent",
]

def get_long_description():
    with open(README_FILE, encoding="utf-8") as f:
        return f.read()


setup(
    name='pymcops',
    version=VERSION,
    author="Danh Phan",
    author_email="danh.phan.mq@gmail.com",
    description='pymcops',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "test_*"]),
    classifiers=classifiers,
    
)