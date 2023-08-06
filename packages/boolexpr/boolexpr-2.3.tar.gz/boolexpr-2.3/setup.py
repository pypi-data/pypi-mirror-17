#!/usr/bin/env python3
#
# Copyright 2016 Chris Drake
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
from glob import glob
from os.path import join
from setuptools import Extension
from setuptools import setup


with open(join("/home/cjdrake/Downloads/src/github.com/cjdrake/boolexpr", "README.rst")) as fin:
    README = fin.read()

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: C++",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    "Topic :: Scientific/Engineering :: Mathematics",
]


sources = [
    join("boolexpr", "third_party", "glucosamine", "src", "core", "Solver.cc"),
]
sources += glob(join("boolexpr", "src", "*.cc"))

include_dirs = [
    join("boolexpr", "include"),
    join("boolexpr", "third_party", "glucosamine", "src"),
    join("boolexpr", "third_party", "boost-1.54.0"),
]

define_macros = [
    ("NDEBUG", None),
]

extra_compile_args = []
# Assume MSVC on Windows
if sys.platform == "win32":
    extra_compile_args += ["/std:c++11", "/Wall"]
# Assume Clang on MacOS
elif sys.platform == "darwin":
    extra_compile_args += ["-std=c++11", "-Wall"]
    extra_compile_args += ["-stdlib=libc++"]
    extra_compile_args += ["-mmacosx-version-min=10.7"]
# Assume GNU otherwise
else:
    extra_compile_args += ["-std=c++11", "-Wall"]

bx = Extension(
         name="boolexpr._boolexpr",
         sources=sources,
         include_dirs=include_dirs,
         define_macros=define_macros,
         extra_compile_args=extra_compile_args,
         language = "c++",
     )


setup(
    # distutils
    name="boolexpr",
    version="2.3",
    description="Boolean Expressions",
    long_description=README,
    author="Chris Drake",
    author_email="cjdrake@gmail.com",
    url="http://www.boolexpr.org",
    download_url="",
    packages=["boolexpr"],
    ext_modules=[bx],
    classifiers=CLASSIFIERS,
    license="Apache 2.0",

    # setuptools
    install_requires=["cffi>=1.5.0"],
)
