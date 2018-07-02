from flask import Flask, render_template
from flask_googletrans import translator
from googletrans import Translator
from os import path, mkdir, remove
from shutil import rmtree
from pytest import fixture
from atexit import register
from random import randint
from tempfile import TemporaryFile
from json import loads
from sys import version_info as V


text = 'something to say'
new_text = 'something new'
src = 'en'
dest = 'it'
dirs = ['templates', 'static']
translation = 'qualcosa da dire'
translation_es = 'algo que decir'

def toCleanUp():
    for d in dirs:
        if path.isdir(d):
            rmtree(d)

register(toCleanUp)

def toMimic(data):
    for d in dirs:
        if not path.isdir(d):
            mkdir(d)
    while True:
        tFile = str(randint(1, 9999999)) + '.html'
        if not path.isfile(tFile):
            break
    with open(path.join(dirs[0], tFile), 'w+') as file:
        file.write(data)
    return tFile


app = Flask(__name__)
eng = translator(app=app, route=True, cache=True)

@app.route('/translate')
def tran():
    return render_template(
        toMimic(
            '{{ translate(text="%s", src="%s", dest=["%s"]) }}' % (
                text, src, dest 
            )
        )
    )

@fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    yield client


def test_translate_template_initApp(client):
    eng.init_app(app)
    client.get('/translate').data
    resp = client.get('/translate').data
    assert resp.decode('utf8') == translation

def test__GtranRoute(client):
    resp = loads(client.get(
        '/gtran/%s/%s/%s' % (
            src, dest, text
        )).data
    )['translation']
    assert resp == translation

def test_translate_single_new_dest(client):
    resp = eng.translate(
        text=text,
        src=src,
        dest=['es']
    )
    assert resp == translation_es

def test_translate_multi(client):
    def toDoRaise():
        try:
            resp = eng.translate(
                text=text,
                src=src,
                dest=[
                    'en',
                    'it',
                    'es'
                ]
            )
            assert resp == {
                'en': text,
                'it': translation,
                'es': translation_es
            }
        except Exception as e:
            assert type(e) == AssertionError
    toDoRaise()
    eng.cache = False
    eng.fail_safe = True
    toDoRaise()
    eng.cache = True
    eng.fail_safe = False

def test_cache_translation(client):
    with open(eng.file_name, 'w+') as f:
        f.write('{"": {}}')
    if path.isfile(eng.file_name):
        remove(eng.file_name)
    resp = client.get('/translate').data
    assert resp.decode('utf8') == eng.STORAGE[text][dest]

def test_cache_tanslation_false(client):
    try:
        eng.file_name = '200'
        eng.loadCache()
    except Exception as e:
        assert type(e) == IOError

def test_translate_multi_new_mod(client):
    eng.STORAGE[text] = {'en': 'falsely modified'}
    resp = eng.translate(
        text=text,
        dest=[dest, 'es'],
        src=src
    )
    assert resp == {
        dest: translation,
        'es': translation_es
    }


def test_translate_false_input(client):
    try:
        eng.translate(text=False)
    except Exception as e:
        assert type(e) == AttributeError
    try:
        eng.translate(text=text, src=False)
    except Exception as e:
        assert type(e) == TypeError
    try:
        eng.translate(text=text, src=src, dest=False)
    except Exception as e:
        assert type(e) == AttributeError
    try:
        eng.translate(text=text, src=src, dest=['200'])
    except Exception as e:
        assert type(e) == AttributeError
    eng.fail_safe = True
    try:
        eng.translate(text=text, src=src, dest=['200'])
    except Exception as e:
        assert type(e) == AttributeError

def test_translator_false_input(client):
    try:
        translator(app=None)
    except Exception as e:
        assert type(e) == AttributeError
    try:
        translator(app=app, cache=200)
    except Exception as e:
        assert type(e) == AttributeError
    remove(eng.file_name)