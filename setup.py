"""
Setup script for Minimal Decimal SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="minimal-decimal-sdk",
    version="1.0.0",
    author="Maxwell2019",
    description="Минимальный SDK для работы с блокчейном Decimal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="decimal blockchain sdk web3 ethereum",
    project_urls={
        "Bug Reports": "https://github.com/decimalchain/decimal-python-sdk/issues",
        "Source": "https://github.com/decimalchain/decimal-python-sdk",
    },
)
