import yaml
# Patch Yaml due github actions error
yaml.CLoader = yaml.Loader

import functools

import bddrest
import pytest

from yhttp import Application
from yhttp_devutils.fixtures import freshdb


@pytest.fixture
def app():
    return Application()


@pytest.fixture
def Given(app):
    return functools.partial(bddrest.Given, app)
