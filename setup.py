import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def installNLTKDependencies():
    import nltk
    nltk.download("punkt")
    nltk.download("stopwords")


setuptools.setup(
    name="sentence_tokenizer",
    version="0.0.1",
    author="Ottavio Fogliata",
    author_email="ottavio.fogliata@storykube.com",
    description="A really rough text cleaner with an ugly code. But very useful.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/storykube/text_cleaner",
    project_urls={
        "Bug Tracker": "https://github.com/storykube/text_cleaner/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

installNLTKDependencies()
