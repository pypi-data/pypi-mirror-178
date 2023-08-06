from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='pycodemarker',
    packages=find_packages(include=['pycodemarker']),
    version='0.0.4',
    description='Code Marker Library from Doctor Droid to instrumenting product metrics',
    author='Dipesh Mittal',
    author_email = "dipeshmittal14@gmail.com",
    license='MIT',
    python_requires = ">=3.6",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)