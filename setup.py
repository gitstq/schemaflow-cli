#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SchemaFlow - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="schemaflow",
    version="1.0.0",
    author="SchemaFlow Team",
    author_email="hello@schemaflow.dev",
    description="Lightweight JSON Schema Terminal Visualizer & Validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/schemaflow",
    py_modules=["schemaflow"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    keywords="json schema validator visualizer cli terminal tool",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/schemaflow/issues",
        "Source": "https://github.com/gitstq/schemaflow",
        "Documentation": "https://github.com/gitstq/schemaflow#readme",
    },
    entry_points={
        "console_scripts": [
            "schemaflow=schemaflow:main",
            "sf=schemaflow:main",
        ],
    },
)
