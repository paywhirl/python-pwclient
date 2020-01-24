import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paywhirl",
    version="1.2",
    author="PayWhirl",
    author_email="developer@paywhirl.com",
    description="Python client for PayWhirl API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paywhirl/python-pwclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
