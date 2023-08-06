import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="import-export",
    version=__import__("export", locals=locals()).__version__,
    description="A Python module methods decorator",
    keywords=["python", "import", "module", "package", "export"],
    long_description=open("./README.pypi.md", mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="JL Connor",
    author_email="AbLaternae@outlook.com",
    url="https://github.com/ablaternae/py-export",
    # download_url="",
    license="GLWTPL",
    # license_files=[],
    py_modules=["export"],
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
