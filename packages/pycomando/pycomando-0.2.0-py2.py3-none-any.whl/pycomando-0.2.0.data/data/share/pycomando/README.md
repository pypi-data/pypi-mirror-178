# INTRODUCTION

pycomando is a Library for creating command line program's command with minimal effort
pycomando is based on argparse allowing the creation of commands starting from a simple yml file.

- PyPI: https://pypi.python.org/pypi/pycomando/
- GitLab: https://gitlab.com/doberti/pycomando/
- Documentation: https://gitlab.com/doberti/pycomando/-/wikis/Documentation/

![sgstat](https://gitlab.com/doberti/pycomando/-/raw/main/sgstat.jpg)

# MAINTAINERS:
	- Daniel Oberti (obertidaniel@gmail.com)

# Install this package

### Using a distribuible package:

This project is deployed as a python package. 
Once cloned we advice to install it with pip. 
In order to do that the user needs to open a command prompt, go into the directory containing the project and execute the next command:

```bash
git clone <REPO>

# creating the dist. package
cd <REPO>
python setup.py sdist

# install the dist. package (located on folder "sdist")
pip install <PACKAGE.tar.gz>
```

### Using git + pip
```bash
git clone <REPO>
pip install -e <PACKAGE>
```

### Using pypi

#### How to - uploading to pypi
```bash
# install the required tools
python -m pip install -U pip setuptools twine
python setup.py bdist_wheel
# (publicar en pypi)
python -m twine upload dist/* --skip-existing
```

#### How to - install from pypi

```bash
# install the package anywhere:
pip install <PACKAGE>
```

# Uninstall this package
```bash
pip uninstall <PACKAGE>
```

# Redis server setup using Docker

pycomando has an option to store commands into a redis db.
You can use docker to deploy it easely as shown below:

Run redis in docker with:
```bash
$ docker run --name redis -p 7010:6379 -d redis:6.2.6
```


# Autocomplete setup

tcsh:
```bash
eval `register-python-argcomplete --shell tcsh pycomando`
```
bash:
```bash
eval "$(register-python-argcomplete pycomando)"
```

# Environment variables

```bash
# DEBUG_LEVEL can be used to set the app logging_level as shown below:
setenv DEBUG_LEVEL INFO
setenv DEBUG_LEVEL DEBUG
setenv DEBUG_LEVEL WARNING

setenv REDIS_SERVER sjs5-015s
setenv REDIS_PORT 7010
```


# Usage Example

A simple usage example is on the folder "examples" (before run it, you should install this package)

# References

- https://es.acervolima.com/como-publicar-el-paquete-python-en-pypi-usando-el-modulo-twine/
- https://programmerclick.com/article/2710482940/
- https://choosealicense.com/
- https://pypi.org/ (here you must register as well if you want to publish packages)
