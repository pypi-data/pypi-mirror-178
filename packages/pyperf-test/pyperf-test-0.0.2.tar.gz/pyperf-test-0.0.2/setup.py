import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
setuptools.setup(
    name="pyperf-test",
    version="0.0.2",
    author="Maxim Volkovskiy",
    author_email="maxwolf8852@gmail.com",
    description="test python speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxwolf8852/perf_test.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)