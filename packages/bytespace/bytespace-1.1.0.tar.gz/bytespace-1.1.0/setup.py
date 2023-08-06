from setuptools import find_packages, setup

setup(
    name="bytespace",
    packages=find_packages(include=["bytespace"]),
    version="0.1.0",
    description="A Python library for the bytespace.network API",
    author="Remy",
    license="MIT",
    install_requires=["requests"],
    setup_requires=["pytest-runner"],
    test_requires=["pytest"],
    test_suite="tests",
)