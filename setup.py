import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="dotnettimeparser",
    version="1.0.0",
    description="Microsoft .NET Like Time String Converter for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/newvicx/dotnettimeparser",
    author="newvicx",
    author_email="chrisnewville1396@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dotnettimeparser"],
    include_package_data=True,
    install_requires=["python-dateutil"],
)