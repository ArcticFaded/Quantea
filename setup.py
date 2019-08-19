import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantea",
    version="0.0.5",
    author="Jonathan Beltran",
    author_email="jbeltran7@gatech.edu",
    description="A backtrading framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArcticFaded/Quantea",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
