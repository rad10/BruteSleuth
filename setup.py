import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BruteSleuth",
    version="1.3.5",
    author="Nicholas Cottrell",
    author_email="ncottrellweb@gmail.com",
    description="This program uses string formatting to give a list of strings related to an original string based off regex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rad10/StringPlus",
    project_urls={
        "Bug Tracker": "https://github.com/rad10/StringPlus/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    scripts=['bin/brutesleuth'],
)
