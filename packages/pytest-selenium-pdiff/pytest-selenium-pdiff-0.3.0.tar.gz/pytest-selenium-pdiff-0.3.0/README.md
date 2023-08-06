# pytest-selenium-pdiff

[![Current Version](https://img.shields.io/pypi/v/pytest-selenium-pdiff.svg)](https://pypi.python.org/pypi/pytest-selenium-pdiff)
[![Build Status](https://img.shields.io/circleci/project/rentlytics/pytest-selenium-pdiff.svg)](https://circleci.com/gh/rentlytics/pytest-selenium-pdiff)

A pytest package implementing perceptualdiff for Selenium tests.

* Free software: MIT license
* Documentation: https://pytest-selenium-pdiff.readthedocs.org.

## Features
* Embeds screenshots in [pytest-html](https://pypi.python.org/pypi/pytest-html) reports
* Supports ImageMagick or perceptualdiff for image comparison.

## Use with pytest-html and pytest-selenium
By default pytest-selenium will embed a screenshot depicting the current browser state.  This will lead to a duplicated screenshot because of this plugin's behavior.  At this time the best way to exclude the pytest-selenium screenshot is to set the environment variable `SELENIUM_EXCLUDE_DEBUG=screenshot`.

## Running tests
1. Ensure `tox` is installed with `pip install tox`
1. Install PhantomJS with `brew install phantomjs`
1. Use `tox` to run tests against py2.7 and py3.5.
1. Rentlytics employees can run `make release` to push to PyPi.  In order to authenticate, you need a `.pypirc` file in your home directory
