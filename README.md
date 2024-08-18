# yhttp-pony

[![PyPI](http://img.shields.io/pypi/v/yhttp-pony.svg)](https://pypi.python.org/pypi/yhttp-pony)
[![Build](https://github.com/yhttp/yhttp-pony/actions/workflows/build.yml/badge.svg)](https://github.com/yhttp/yhttp-pony/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/yhttp/yhttp-pony/badge.svg?branch=master)](https://coveralls.io/github/yhttp/yhttp-pony?branch=master)


Pony ORM extension for [yhttp](https://github.com/yhttp/yhttp).


## Install

```bash
sudo apt`install python3-dev libpq-dev postgresql  # Postgresql
pip install yhttp-pony
```

## Usage

This is how to use the extension.


```python
from yhttp import Appliation, json
from yhttp.ext import pony as ponyext 
from pony.orm import db_session as dbsession, PrimaryKey, Required


app = Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/foo
''')
db = ponyext.install(app)


class Foo(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)


@app.route()
@json
@dbsession
def get(req):
    return {f.id:f.title for f in Foo.select()}


app.ready()
```

### Command line interface

There is some command line interfaces which will be automatically added to
your application when you call `dbmanager.install(app, ...)` and 
`ponyext.install(app, ...)`.


```bash
myapp db create
myapp db objects create
myapp db drop
```


#### Extending db sub-command

```python
import easycli
from yhttp.ext import dbmanager, ponyext

from mypackage import app  # yhttp application


class InsertMockupCommand(easycli.SubCommand):
    __command__ = 'insert-mockup'

    def __call__(self, args):
        ponyext.initialize(app.db, app.settings.db)

        # Insert mockup data

        ponyext.deinitialize(app.db)


class VerifyObjectsCommand(easycli.SubCommand):
    __command__ = 'verify'
    __aliases__ = ['v']

    def __call__(self, args):
        ponyext.initialize(app.db, app.settings.db)

        # Verify database objects

        ponyext.deinitialize(app.db)

...

dbmanager.install(app, cliarguments=[InsertMockupCommand])
db = ponyext.install(app, cliarguments=[VerifyObjectsCommand])
```

Use it as:

```bash
myapp db create
myapp db insert-mockup
myapp db objects create
myapp db objects verify
myapp db drop
```


## Contribution

### Dependencies
Install `postgresql` brefore use of this project.
```bash
apt install postgresql
```

### Prepare

Create and grant the `postgresql` role with `createdb` permission to 
authenticate the current `unix` user within `postgresql` using the peer 
authentication.
```bash
echo "CREATE USER ${USER} WITH CREATEDB" | sudo -u postgres psql
# Or
echo "ALTER USER ${USER} CREATEDB" | sudo -u postgres psql
```

### Virtualenv

Create virtual environment:
```bash
make venv
```

Delete virtual environment:
```bash
make venv-delete
```

Activate the virtual environment:
```bash
source ./activate.sh
```


### Install (editable mode)
Install this project as editable mode and all other development dependencies:
```bash
make env
```


### Tests
Execute all tests:
```bash
make test
```

Execute specific test(s) using wildcard:
```bash
make test F=tests/test_db*
make test F=tests/test_form.py::test_querystringform
```

*refer to* [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html#how-to-invoke-pytest)
*for more info about invoking tests.*

Execute tests and report coverage result:
```bash
make cover
make cover F=tests/test_static.py
make cover-html
```


### Lint
```bash
make lint
```


### Distribution
Execute these commands to create `Python`'s standard distribution packages
at `dist` directory:
```bash
make sdist
make wheel
```

Or 
```bash
make dist
```
to create both `sdidst` and `wheel` packages.


### Clean build directory
Execute: 
```bash
make clean
```
to clean-up previous `dist/*` and `build/*` directories.


### PyPI

> **_WARNING:_** Do not do this if you'r not responsible as author and 
> or maintainer of this project.

Execute
```bash
make clean
make pypi
```
to upload `sdists` and `wheel` packages on [PyPI](https://pypi.org).
