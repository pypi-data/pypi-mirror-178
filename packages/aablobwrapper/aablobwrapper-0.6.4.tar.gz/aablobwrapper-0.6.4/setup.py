import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="aablobwrapper",
    version=version,
    author="Daniel Kirkegaard Mouritsen",
    author_email="daniel.mouritsen@gmail.com",
    description="Provide file-like wrapper for Azure Blobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justdanyul/aablobwrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "azure-storage-blob",
        "aiohttp",
    ],
    python_requires=">=3.7",
)
