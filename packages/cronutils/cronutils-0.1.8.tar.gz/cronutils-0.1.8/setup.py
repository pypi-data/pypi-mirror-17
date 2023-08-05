"""
The MIT License (MIT)

Copyright (c) 2014 Zagaran, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: Zags (Benjamin Zagorsky)
"""

import sys

from setuptools import setup, find_packages

if sys.version < '2.5':
    print("ERROR: python version 2.5 or higher is required")
    sys.exit(1)

setup(
    name = "cronutils",
    version = "0.1.8",
    packages = find_packages(),
    
    author = "Zagaran, Inc.",
    author_email = "zags at zagaran.com",
    description = "Tool designed to simplify the configuration and dispatching of tasks via cron",
    license = "MIT",
    keywords = "cron crontab task error handling",
    url = "https://github.com/zagaran/cronutils",
    install_requires = [],
    classifiers = [
                 "Development Status :: 4 - Beta",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX",
                 "Programming Language :: Python",
                 "Topic :: Utilities",
                 ],
)
