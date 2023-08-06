from setuptools import setup

with open("README.md", "r") as readme_bf:
    readme_content = readme_bf.read()

setup(
    name="wcdeetlist",
    version="0.0.0.1",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="scrapper scraper crawler deetlist",
    description=u"Web Crawler for https://deetlist.com",
    packages=["wcdeetlist"],
    install_requires=["requests", "bs4"],
)