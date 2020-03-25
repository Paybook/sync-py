# DEVELOPMENT BINNACLE

## Tools used

* [Python](https://www.python.org/): 3.7
* [Pipenv](https://github.com/pypa/pipenv): 2018.11.26
* [Twine](https://github.com/pypa/twine/) : 3.1.1

Run develoment local:
```bash
    cd sync-py
    pipenv install --dev -e .
    pipenv graph
```

Create **dist files**: 
```bash
pipenv run python setup.py sdist bdist_wheel
```

Check **dist files**: 
```bash
twine check dist/*
```

Publish on test.pypi.org: 
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

> Don't forget to increase the version

## TODO

- [ ] Add version one version manager (https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version)
- [ ] Add properly test


###  External documentation used

1. [Distributing packages Official documentation](https://packaging.python.org/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi)

1. [Real python blog - How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

1. [Pipenv documentation](https://github.com/pypa/pipenv)

1. [Getting Started With Testing in Python](https://realpython.com/python-testing/)
