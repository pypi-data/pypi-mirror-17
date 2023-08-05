import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a simple app for publishing links to news articles on your site",
    name="pinax-news",
    long_description=read("README.rst"),
    version="1.1.2",
    url="http://github.com/pinax/pinax-news/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax.news": []
    },
    test_suite="runtests.runtests",
    tests_require=[
    ],
    install_requires=[
        "django-imagekit>=3.3",
        "Markdown>=2.6.6"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
