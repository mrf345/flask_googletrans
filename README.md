<h1 align='center'> flask_googletrans </h1>
<p align='center'>
<a href='https://travis-ci.com/mrf345/flask_googletrans'><img src='https://travis-ci.com/mrf345/flask_googletrans.svg?branch=master' /></a><a href='https://coveralls.io/github/mrf345/flask_googletrans?branch=master'><img src='https://coveralls.io/repos/github/mrf345/flask_googletrans/badge.svg?branch=master' alt='Coverage Status' /></a>
</p>
<h3 align='center'>
    A Flask extension to add Googletrans google translation to the template with ability to cache translation to external pretty .json file.
</h3>

## Install:
#### - With pip
> - `pip install Flask-Googletrans` <br />

#### - From the source:
> - `git clone https://github.com/mrf345/flask_googletrans.git`<br />
> - `cd flask_googletrans` <br />
> - `python setup.py install`

## Setup:
#### - Inside Flask app:
```python
from flask import Flask, render_template
from flask_googletrans import translator

app = Flask(__name__)
ts = translator(app)
```

#### - Inside jinja template:
```jinja
<h1>{{ translate(text='translation !', src='en', dest=['fr']) }}</h1>
```

## Settings:
#### - Options:
> The accepted arguments to be passed to the `translator.translate()` function are as follow:
```python
def translate(
        self,
        text='translation !', # Text to be translated
        src='en', # Language to be translated from
        dest=['fr']): # Languages to translate to
```
> If more than one language is used, the returning value will be a dictionary instead of a text string
```python
# assuming
translate(text='something', src='en', dest=['fr', 'it', 'es'])
# this will return 
{"en": "nothing", "fr": "rien", "it": "Niente", "es": "nada"}
```

#### - Caching:
> Caching stores all the translated text in one big dictionary with the translated text as a key in a separate .json file
```python
ts = translator(
    app=app,
    cache=True, # To enable caching by default is disabled
    fail_safe=False, # returns original text if fetching translation failed
    skip_app=False, # to skip checking app for .init_app()
    file_name='gt_cache.json', # To change the default name of the cache file
    route=False # opens up a route on /gtran/<fromL>/<toL>/<text> to fetch translation as json response {translation: 'text ...'}
)
```

#### - Useful functions:

Function | Does
---------|----------
 ts.translate() | To translate as shown in template example
 ts.loadCache() | To load the cache file
 ts.cacheIt() | To store the current saved translation to the cache file


#### - List of supported languages:
`{
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}`

## Credit:
> - [Googletrans][1311353e]: Awesome free and unlimited python library that implements Google Translate API

  [1311353e]: https://github.com/ssut/py-googletrans "Googletrans repo"
