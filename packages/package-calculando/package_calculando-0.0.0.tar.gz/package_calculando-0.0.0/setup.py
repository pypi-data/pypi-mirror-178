from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_calculando",
    version="0.0.0",
    author="Adriana Andrade",
    author_email="andrade.m.drika@gmail.com",
    description="Calculadora com funcionalidades basicas",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdrianaAndrade2203",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)