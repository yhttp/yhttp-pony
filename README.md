# yhttp-pony

[![PyPI](http://img.shields.io/pypi/v/yhttp-pony.svg)](https://pypi.python.org/pypi/yhttp-pony)
[![Build Status](https://travis-ci.org/yhttp/yhttp-pony.svg?branch=master)](https://travis-ci.org/yhttp/yhttp-pony)
[![Coverage Status](https://coveralls.io/repos/github/yhttp/yhttp-pony/badge.svg?branch=master)](https://coveralls.io/github/yhttp/yhttp-pony?branch=master)


Pony ORM extension for [yhttp](https://github.com/yhttp/yhttp).


## Install

```bash
sudo apt install python3-dev libpq-dev postgresql  # Postgresql
pip install yhttp-pony
```

## Usage

This is how to use the extension.


```python
from yhttp import Appliation, json
from yhttp.extensions import pony as ponyext 
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
your application when you call `ponyext.install(app)`.


```bash

myapp db create
myapp db drop
```

### Running tests

```bash
echo "ALTER USER postgres PASSWORD 'postgres'" | sudo -u postgres psql
make test
make cover
```
