<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/kitconcept/kitconcept.richpage/main/docs/kitconcept.png" width="70" /></div>

<h1 align="center">kitconcept.richtext</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)
[![PyPI - License](https://img.shields.io/pypi/l/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)
[![PyPI - Status](https://img.shields.io/pypi/status/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/kitconcept.richpage)](https://pypi.org/project/kitconcept.richpage/)

[![Code analysis checks](https://github.com/kitconcept/kitconcept.richpage/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/kitconcept/kitconcept.richpage/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/kitconcept/kitconcept.richpage/actions/workflows/tests.yaml/badge.svg)](https://github.com/kitconcept/kitconcept.richpage/actions/workflows/tests.yaml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/kitconcept/kitconcept.richpage)](https://github.com/kitconcept/kitconcept.richpage)
[![GitHub Repo stars](https://img.shields.io/github/stars/kitconcept/kitconcept.richpage?style=social)](https://github.com/kitconcept/kitconcept.richpage)

</div>

Installation
------------

Add **kitconcept.richpage** to the Plone installation using `pip`:

```bash
pip install kitconcept.richpage
```
or add it as a dependency on your package's `setup.py`

```python
    install_requires = [
        "kitconcept.richpage",
        "Products.CMFPlone",
        "plone.restapi",
        "setuptools",
    ],
```

Start Plone and activate the plugin in the addons control-panel.


Source Code and Contributions
-----------------------------

If you want to help with the development (improvement, update, bug-fixing, ...) of `kitconcept.richpage` this is a great idea!

- [Issue Tracker](https://github.com/kitconcept/kitconcept.richpage/issues)
- [Source Code](https://github.com/kitconcept/kitconcept.richpage/)


Please do larger changes on a branch and submit a Pull Request.

We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

Development
-----------

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.7 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```

To run tests for this package:

```bash
make test
```

By default we use the latest Plone version in the 6.x series.

License
-------

The project is licensed under the GPLv2.
