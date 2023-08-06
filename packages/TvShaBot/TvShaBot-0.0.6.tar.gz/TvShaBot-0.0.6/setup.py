from setuptools import setup, find_packages

setup(
    name="TvShaBot",
    version="0.0.6",
    author="ShaeNaZar",
    description="A bot to request a show info",
    install_requires=['pydantic'],
    long_description_content_type="text/markdown",
    packages=find_packages(),
)