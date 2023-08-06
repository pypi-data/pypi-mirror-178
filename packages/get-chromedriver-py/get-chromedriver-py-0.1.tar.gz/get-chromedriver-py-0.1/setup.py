import os

from setuptools import setup

version = "0.1"

try:
    readme = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
except OSError:
    readme = ""

install_requires = []

extras_require = []

tests_require = [
    "parameterize",
    "pytest",
    "pytest-cov",
    "pytest-pythonpath",
    "tox",
]

setup(
    name="get-chromedriver-py",
    version=version,
    description="Get chromedriver-py version most suitable for your system.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/"
                       "get-chromedriver-py/issues",
        "Documentation": "https://get-chromedriver-py.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/"
                       "get-chromedriver-py/",
        "Changelog": "https://get-chromedriver-py.readthedocs.io/"
        "en/latest/changelog.html",
    },
    entry_points={
        "console_scripts": ["get-chromedriver = get_chromedriver:run_cli"]
    },
    keywords="get-chromedriver-py, chromedriver-py",
    author="Artur Barseghyan",
    author_email="artur.barseghyan@gmail.com",
    url="https://github.com/barseghyanartur/get-chromedriver-py/",
    py_modules=["get_chromedriver"],
    license="MIT",
    python_requires=">=3.7",
    install_requires=(install_requires + extras_require),
    tests_require=tests_require,
    include_package_data=True,
)
