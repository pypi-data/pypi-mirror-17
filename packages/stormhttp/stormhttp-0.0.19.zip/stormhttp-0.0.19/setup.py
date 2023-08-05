from distutils.core import setup
from setuptools.command.test import test
from stormhttp import __version__


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        import sys
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name="stormhttp",
    packages=[
        "stormhttp"
    ],
    version=__version__,
    description="Lightning-fast HTTP primitives based on httptools",
    license="Apache 2",
    author="Seth Michael Larson",
    author_email="sethmichaellarson@protonmail.com",
    url="https://github.com/SethMichaelLarson/stormhttp",
    download_url="https://github.com/SethMichaelLarson/stormhttp/tarball/" + __version__,
    keywords=["web"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP"
    ],
    install_requires=[
        "httptools>=0.0.9",
        "brotlipy>=0.5.1"
    ],
    tests_require=[
        "pytest",
        "coverage",
        "coveralls"
    ],
    cmdclass={
        "test": PyTest
    }
)
