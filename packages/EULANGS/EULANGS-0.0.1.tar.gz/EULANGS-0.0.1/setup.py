import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
	name="EULANGS",
	version="0.0.1",
	author="Simon Hengchen",
	author_email="simon@iguanodon.ai",
	description="This package allows you to import a list of official EU languages.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "."},
    packages = setuptools.find_packages(where="."),
    python_requires = ">=3.4"
)
