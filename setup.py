#    Copyright (C) 2014  Yubico AB
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from setuptools.command.sdist import _sdist as sdist
from os import path
from release import release
import re

VERSION_PATTERN = re.compile(r"(?m)^__version__\s*=\s*['\"](.+)['\"]$")


def get_version():
    """Return the current version as defined by u2fval/__init__.py."""

    with open('u2fval/__init__.py', 'r') as f:
        match = VERSION_PATTERN.search(f.read())
        return match.group(1)


class custom_sdist(sdist):
    def run(self):
        print "copying default settings..."
        source = path.abspath('u2fval/default_settings.py')
        target = path.abspath('conf/u2f-val.conf')
        with open(target, 'w') as target_f:
            with open(source, 'r') as source_f:
                target_f.write(source_f.read())
        sdist.run(self)


setup(
    name='u2fval',
    version=get_version(),
    author='Dain Nilsson',
    author_email='dain@yubico.com',
    maintainer='Yubico Open Source Maintainers',
    maintainer_email='ossmaint@yubico.com',
    url='https://github.com/Yubico/u2fval',
    packages=['u2fval', 'u2fval.core', 'u2fval.client'],
    scripts=['scripts/u2f-val'],
    setup_requires=['nose>=1.0'],
    data_files=[('/etc/yubico/u2f-val',
                 ['conf/u2f-val.conf', 'conf/logging.conf'])],
    install_requires=['python-u2flib-server', 'SQLAlchemy', 'python-memcached',
                      'WebOb'],
    test_suite='nose.collector',
    tests_require=[''],
    cmdclass={'release': release, 'sdist': custom_sdist},
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]
)
