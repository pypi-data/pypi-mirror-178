#!/usr/bin/env python
import ast
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, "src", "tenant_admin", "__init__.py")

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open(init, "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

requirements = [
    "django-smart-admin>=2.6.0",
    "django-admin-extra-buttons>=1.5.5",
    "django-adminfilters>=2.0.3",
]
tests_require = [
    "black",
    "django-constance",
    "django-picklefield",
    "django-webtest",
    "factory-boy",
    "flake8",
    "isort",
    "mypy",
    "pre-commit",
    "pyquery",
    "pytest",
    "pytest-cov",
    "pytest-coverage",
    "pytest-django",
    "pytest-echo",
    "redis",
    "tox",
]
dev_require = ["pdbpp", "django", "check-manifest"]
docs_require = []

setup(
    name="django-tenant-admin",
    version=version,
    url="https://gitlab.com/os4d/django-tenant-admin",
    download_url="https://gitlab.com/os4d/django-tenant-admin",
    author="os4d",
    author_email="dev@os4d.org",
    description="",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=requirements,
    tests_require=tests_require,
    extras_require={
        "test": requirements + tests_require,
        "dev": dev_require + tests_require,
        "docs": dev_require + docs_require,
    },
    zip_safe=False,
    platforms=["any"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
