from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="card_roulette",
    version="1.1.0",
    author="Dhya El Bahri",
    author_email="dhya.bahri@icloud.com",
    description="A simple card game simulation called Card Roulette",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Disciple0fMarx/card_roulette",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
