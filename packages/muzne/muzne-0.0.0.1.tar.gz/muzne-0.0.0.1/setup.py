# This file is part of Uzoenr.
# Copyright (C) 2022 sherekhan at pypi.org
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from setuptools import setup, find_packages
from os.path import join, dirname
import re

s = open("muzne/__init__.py").read().split('\n')[0]
__version__ = re.search('\"[0-9\.]+\"$', s).group()[1:-1]

setup(
   name='muzne',
   version=__version__,
   author='sherekhan at pypi.org',
   author_email='sherekhan@jungle.tes',
   packages=find_packages(),
   license='GNU GPL3+',
   description='Just a simple web server',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "markdown>=3.4.1",
   ],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
    ],
   entry_points={
        'console_scripts':
            ['muzne = muzne:start']
        }
)
