from googletrans import Translator as google_translator
from json import dumps
from os.path import isfile
from os import name as OSName


class translator (object):
    def __init__(
        self,
        app=None,
        cache=False,
        file_name='gt_cached.py'):
        """
        Googletrans flask extension with caching translation in .py file
        @param: app Instance of the Flask app (default: False)
        @param: cache To enable or disable caching translation (default: False)
        @param: file_name Name of the python file to store the cached translation in
        (default: 'gt_cached.py')
        """
        self.app = app
        self.cache = cache
        self.file_name = file_name
        self.full_path = __path__[0]
        self.full_path += "\\" if OSName == 'nt' else '/' + self.file_name
        self.STORAGE = {'': {}}
        self.languages = [
            'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs',
            'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs',
            'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl',
            'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'he',
            'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km',
            'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms',
            'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ps', 'fa', 'pl',
            'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si',
            'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th',
            'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'fil']
        if self.app is None:
            raise(AttributeError('must pass app instance to Translator(app=)'))
        if not isinstance(self.cache, bool):
            raise(AttributeError('must pass boolean to Translator(cache=)'))
        if isinstance(self.file_name, str):
            if self.cache:
                if isfile(self.file_name):
                    self.loadCache()
                else:
                    self.cacheIt()
        else:
            raise(AttributeError('must pass string path to Translator(file_path=)'))
        @self.app.context_processor
        def inject_vars():
            """ to inject translate function into the template """
            return dict(translate=self.translate)


    def translate(
        self,
        text='translation !',
        src='en',
        dest=['fr']):
        """
        To pass text to googletrans.Translator() and return translated and cache it if so
        @param: text Text to be translated (default: 'translation !')
        @param: src Language to translate text from (default: 'en')
        @param: dest List of languages to return translated text in (default: ['fr'])
        """
        if not isinstance(text, str):
            raise(AttributeError('translate(text=) you must pass string of text to be translated'))
        if src not in self.languages:
            raise(AttributeError('translate(src=) passed language is not supported: ' + src))
        if not isinstance(dest, list):
            raise(AttributeError('translate(dest=) you must pass list of strings of supported languages'))
        for dl in dest:
            if dl not in self.languages:
                raise(AttributeError('translate(dest=[]) passed language is not supported: ' + dl))
        translator = google_translator()
        if self.cache and text in self.STORAGE.keys():
            if len(dest) > 1:
                toReturn = {}
                for dl in dest:
                    if dl in self.STORAGE[text].keys():
                        toReturn[dl] = self.STORAGE[text][dl].decode('utf8')
                    else:
                        toReturn[dl] = translator.translate(
                            text,
                            dl,
                            src
                        ).text
                if toReturn != self.STORAGE[text]:
                    self.STORAGE[text] = toReturn
                    self.cacheIt()
                return toReturn
            else:
                return self.STORAGE[text][dest[0]].decode('utf8')
        else:
            toStore = {text: {
                src: text
            }}
            for dl in dest:
                translation = translator.translate(
                    text,
                    dl,
                    src
                )
                toStore[text][dl] = translation.text
            if self.cache:
                self.STORAGE[text] = toStore[text]
                self.cacheIt()
            if len(dest) > 1:
                return toStore[text]
            else:
                return toStore[text][dest[0]]


    def loadCache(self):
        """
        function to try loading cache file
        """
        try:
            self.STORAGE = __import__(self.file_name.split('.py')[0]).STORAGE
        except Exception:
            raise(IOError('Translator() failed to load cached file ' + self.file_name))


    def cacheIt(self):
        """
        function to overwrite the cached translation file
        """
        with open(self.file_name, 'w+') as file:
            file.write("# -*- coding: utf-8 -*-\n" + "STORAGE = " + dumps(self.STORAGE
            ).decode('unicode-escape').encode('utf8') + "\n")
        self.loadCache()