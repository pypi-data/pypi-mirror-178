from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as requirements:
    install_requires = [line.rstrip() for line in requirements.readlines()]

setup(
    name="picsexl",
    version="0.0.1",
    author="pog7x",
    author_email="poluningm@gmail.com",
    url="https://github.com/pog7x/picsexl",
    license="MIT",
    keywords="python calendar ics excel",
    description="Converter from ics format to xls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[""],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
