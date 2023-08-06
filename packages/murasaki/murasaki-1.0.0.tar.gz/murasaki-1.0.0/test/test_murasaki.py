import os
from murasaki import Murasaki
import pytest
from dotenv import load_dotenv
load_dotenv()


user = os.environ.get("MURASAKI_USER")
pwd = os.environ.get("MURASAKI_PWD")

def test_init():
    """Make the constructor returns a Murasaki object."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/")
    assert type(murasaki) == Murasaki
    assert str(murasaki) == "Murasaki: https://jplusplus-murasaki.herokuapp.com/"

def test_connect_and_render():
    """Return a string."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/", user=user, password=pwd)
    assert murasaki.pug({}, "| Hello World") == "Hello World"

def test_autodiscover_credentials():
    """Load user and pwd from .env."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/")
    assert murasaki.pug({}, "| Hello World") == "Hello World"

def test_mustache():
    """Return a string from Mustache tpl."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/", user=user, password=pwd)
    assert murasaki.mustache({'Name': "World"}, "Hello {{ Name }}!") == "Hello World!"

def test_unauthorized():
    """Should raise."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/", user="foo", password="bar")
    with pytest.raises(Exception):
        assert murasaki.pug({}, "| Hello World") == "Hello World"

def test_scary():
    """Should raise."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/", user="foo", password="bar")
    with pytest.raises(Exception):
        assert murasaki.javascript({}, "global.process.env") == "Hello World"
    with pytest.raises(Exception):
        assert murasaki.javascript({}, "eval(\"null\")") == "Hello World"

def test_chaining():
    """Chained functions should work."""
    murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/")
    context = {'name': "World"}
    assert murasaki.pug(context, "| Hello #{ upper(name).lower() }") == "Hello world"
    assert murasaki.javascript(context, "Hello ${ upper(name).lower() }") == "Hello world"
