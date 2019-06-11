from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="syscall_number",
    version="0.1.0",
    description="CLI tool to search for Intel x86 Linux system call names and get the system call number.",
    long_description=readme,
    author="Martin Clauß",
    author_email="mc@cs.uni-bonn.de",
    url="https://github.com/martinclauss/syscall_number",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "click",
        ],
    entry_points = {
        "console_scripts": [
            "syscall_number=syscall_number.syscall_number:main",
        ]
    }
)

