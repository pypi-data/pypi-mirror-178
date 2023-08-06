from setuptools import setup


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pymcops',
    version='0.0.1',
    description='pymcops',
    py_modules=['pymc'],
    package_dir={'':'pymcops'},
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danhphan/PymcOps",
    author="Danh Phan",
    author_email="danh.phan.mq@gmail.com",
)