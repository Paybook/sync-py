# DEVELOPMENT BINNACLE

## Tools used

* [Python](https://www.python.org/): 3.7
* [Pipenv](https://github.com/pypa/pipenv): 2018.11.26
* [Twine](https://github.com/pypa/twine/) : 3.1.1
* [bumb2version](https://pypi.org/project/bump2version/) : 1.0.0

### Dependencies
* [requests](https://pypi.org/project/requests/) : 2.23.0

### Development dependencies
* [python-dotenv](https://pypi.org/project/python-dotenv/) : 0.12.0 

## Set up local development 
Run development local:
```bash
    cd sync-py
    pipenv install --dev -e .
    pipenv graph
```

##  Versioning

1. Install bump2version: `pip install --upgrade bump2version`

1. Then run the respective version update:
- Major: `pipenv run bump2version major` // 0.1.0 --> 1.0.0
- Minor: `pipenv run bump2version minor` // 0.1.0 --> 0.2.0
- Patch: `pipenv run bump2version patch` // 0.1.0 --> 0.1.1

## Publish on test.pypi.org

1.Create **dist files**: 
```bash
pipenv run python setup.py sdist bdist_wheel
```

2.Check **dist files**: 
```bash
twine check dist/*
```

3.Publish on test.pypi.org: 
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

> Don't forget to increase the version

## Test from test.pypi.org
1. Pipfile
```python
[[source]]
name = "test"
url = "https://test.pypi.org/simple"
verify_ssl = true

[dev-packages]
python-dotenv = "*"

[packages]
sync-py = {index = "test",version = "*"}

# .
# .
# .
# Omitted
```

2. Install and update`pipenv install --dev` and `pipenv update`

3. Run `pipevn run python path-to/test.py`

## Publish on pypi.org

1.Create **dist files**: 
```bash
pipenv run python setup.py sdist bdist_wheel
```

2.Check **dist files**: 
```bash
twine check dist/*
```

3.Publish on pypi.org: 
```bash
twine upload dist/*
```

## TODO

- [ ] Add version one version manager (https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version)
- [ ] Add properly test


###  External documentation used

1. [Distributing packages Official documentation](https://packaging.python.org/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi)

1. [Real python blog - How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

1. [Pipenv documentation](https://github.com/pypa/pipenv)

1. [Getting Started With Testing in Python](https://realpython.com/python-testing/)
