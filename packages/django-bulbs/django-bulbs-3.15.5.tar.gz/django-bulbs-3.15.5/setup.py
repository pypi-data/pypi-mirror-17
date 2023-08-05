#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import re
import sys


name = "django-bulbs"
package = "bulbs"
description = "America's Finest Namespace"
url = "https://github.com/theonion/django-bulbs"
author = "Chris Sinchok"
author_email = "csinchok@theonion.com"
license = "BSD"
requires = [
    "Django>=1.8,<1.9",
    "beautifulsoup4>=4.4.1",
    "celery==3.1.10",
    "contextdecorator==0.10.0",
    "django-enumfield==1.2.1",
    "django-betty-cropper>=0.2.6",
    "django-filter==0.9.2",
    "django-jsonfield==0.9.19",
    # TODO: remove django-json-field from previous JSONField references.
    "django-json-field==0.5.5",
    "django-polymorphic==0.7.1",
    "djangorestframework-csv==1.4.1",
    "pageview_client==1.0.4",
    "djangorestframework==3.1.1",
    "drf-extensions==0.2.8",
    "djes>=0.1.109",
    "drf-nested-routers==0.11.1",
    "firebase-token-generator==1.3.2",
    "python-dateutil==2.1",
    "pytz==2012h",
    "requests>=1.1.0",
    "simplejson==3.3.0",
    "six==1.10.0",
]

dev_requires = [
    "pylint==1.0.0",
    "mock==1.0.1",
    "httmock==1.0.5",
    "model-mommy==1.2.4",
    "psycopg2==2.5.1",
    "pytest==2.7.3",
    "pytest-cov==1.8.1",
    "pytest-django==2.8.0",
    "coveralls==0.4.1",
    "freezegun",
    "vcrpy",
    "ipdb",
    "requests-mock",
    "flake8",
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, "__init__.py"))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, "", 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, "__init__.py"))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    args = {"version": get_version(package)}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
)
