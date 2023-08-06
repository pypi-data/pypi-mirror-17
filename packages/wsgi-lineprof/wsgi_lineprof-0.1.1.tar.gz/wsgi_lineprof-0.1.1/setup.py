from codecs import open
from os import path
from warnings import warn

from setuptools import Extension, find_packages, setup


root = path.abspath(path.dirname(__file__))

with open(path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

cmdclass = {}
source = "extensions/line_profiler."

try:
    from Cython.Distutils import build_ext
    cmdclass["build_ext"] = build_ext
    source += "pyx"
except ImportError:
    source += "c"
    if not path.exists(path.join(root, source)):
        raise Exception("No Cython installation, no generated C file")
    warn("Could not import Cython, using generated C source code instead")

setup(
    name="wsgi_lineprof",

    version="0.1.1",

    description="WSGI middleware for line-by-line profiling",
    long_description=long_description,

    url="https://github.com/ymyzk/wsgi-lineprof",

    author="Yusuke Miyazaki",
    author_email="miyazaki.dev@gmail.com",

    license="MIT",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
    ],

    # What does your project relate to?
    # keywords="sample setuptools development",

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests"]),

    ext_modules=[
        Extension("_wsgi_lineprof",
                  sources=[source, "extensions/timer.c"])
    ],

    extras_require={
        "build": ["Cython>=0.24"],
        "test": [
            "pytest>=3.0.0,<4.0.0",
            "tox>=2.0.0,<3.0.0",
        ]
    },
)
