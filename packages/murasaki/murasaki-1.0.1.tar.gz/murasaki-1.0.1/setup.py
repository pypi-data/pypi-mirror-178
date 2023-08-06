import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="murasaki",
    version="1.0.1",
    author="Leo Wallentin, Newsworthy",
    author_email="mejl@leowallentin.se",
    description="A Murasaki API wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/newsworthy/murasaki",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
