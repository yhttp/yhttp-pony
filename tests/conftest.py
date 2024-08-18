import functools

import bddrest
import pytest

from yhttp.core import Application
from yhttp.dev.fixtures import freshdb


@pytest.fixture
def app():
    app = Application()
    yield app
    app.shutdown()


@pytest.fixture
def Given(app):
    return functools.partial(bddrest.Given, app)
