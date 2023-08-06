import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="homovec",
    version="1.0.1",
    author="Andrei Geadau",
    author_email="andreigeadau@tudelft.nl",
    description="Python Homomorphic Encryption Library for Vectors."
                " Supports common mathematical operations such as"
                " additions of ciphertexts and multiplication by constants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayDew/homovec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
