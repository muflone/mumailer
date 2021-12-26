##
#     Project: MuMailer
# Description: Simple mailer agent using SMTP
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import os.path
import pkg_resources
import setuptools

import mumailer.constants


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

# Get dependencies from requirements.txt
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'requirements.txt'),
          encoding='utf-8') as f:
    install_requires = [str(requirement)
                        for requirement
                        in pkg_resources.parse_requirements(f)]

setuptools.setup(
    name=mumailer.constants.APP_NAME,
    version=mumailer.constants.APP_VERSION,
    author=mumailer.constants.APP_AUTHOR,
    author_email=mumailer.constants.APP_AUTHOR_EMAIL,
    description=mumailer.constants.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=mumailer.constants.APP_URL,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 1 - Planning ',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
