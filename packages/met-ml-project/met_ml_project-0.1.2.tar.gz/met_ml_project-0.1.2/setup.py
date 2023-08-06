import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="met_ml_project",
    author="Denis Shibitov",
    author_email="ttwtest1@gmail.com",
    description="MADE MLOps homework 1",
    keywords="mlops, homework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['ml_project'],
    version="0.1.2",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
    python_requires=">=3.7",
    install_requires=required
)
