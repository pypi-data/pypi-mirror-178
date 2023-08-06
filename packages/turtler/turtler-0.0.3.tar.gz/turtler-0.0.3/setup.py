import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turtler",
    version="0.0.3",
    author="Aaryan Dehade",
    author_email="dehadeaaryan@gmail.com",
    description="A fun way to get started with graphics and data science in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dehadeaaryan/turtler",
    project_urls={
        "Bug Tracker": "https://github.com/dehadeaaryan/turtler/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)