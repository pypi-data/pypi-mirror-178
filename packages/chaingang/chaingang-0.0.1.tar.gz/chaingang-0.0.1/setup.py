import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="chaingang",
    version="0.0.1",
    description="Python class decorator that adds selection chaining",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eddiethedean/chaingang",
    author="Odos Matthews",
    author_email="odosmatthews@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[]
)