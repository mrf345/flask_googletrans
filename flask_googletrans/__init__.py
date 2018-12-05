from googletrans import Translator as google_translator
from json import dumps, load
from os.path import isfile
from os import name as OSName
from flask import jsonify
from sys import version_info as V
from threading import Thread
if V.major == 3:
    unicode = bytes


class translator (object):
    def __init__(
        self,
        app=None,
        cache=False,
        fail_safe=False,
        skip_app=False,
        file_name='gt_cached.json',
        route=False
    ):
        """
        Googletrans flask extension with caching translation in .json file
        @param: app Instance of the Flask app (default: False)
        @param: cache To enable or disable caching translation (default: False)
        @param: fail_safe returns original text if fetching translation failed
        (default: False)
        @param: skip_app to skip checking app for .init_app() (default: False)
        @param: file_name Name of the json file to store the cached
        translation in
        (default: 'gt_cached.json')
        @param: route to open up a route on /gtran/<fromL>/<toL>/<text> to
        fetch translation as json response {translation: 'text ...'}
        (default: False)
        """
        self.app = app
        self.cache = cache
        self.fail_safe = fail_safe
        self.skip_app = skip_app
        self.file_name = file_name
        self.full_path = __path__[0]
        self.full_path += "\\" if OSName == 'nt' else '/' + self.file_name
        self.STORAGE = {'': {}}
        self.route = route
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
        if self.app is None and not self.skip_app:
            raise(AttributeError('must pass app instance to Translator(app=)'))
        if not isinstance(self.cache, bool):
            raise(AttributeError('must pass boolean to Translator(cache=)'))
        if isinstance(self.file_name, str):
            if self.cache:
                if isfile(self.file_name):
                    self.loadCache()
                else:
                    self.cacheIt()
        else:  # pragma: nocover
            raise(AttributeError(
                'must pass string path to Translator(file_path=)'))
        if not self.skip_app:
            self.appLoading()
        if self.route:
            self.gtranRoute()

    def init_app(self, app):
        """ to load app after the fact """
        self.app = app
        self.appLoading()

    def translate(
        self,
        text='translation !',
        src='en',
        dest=['fr']
    ):
        """
        To pass text to googletrans.Translator() and return translated and
        cache it if so
        @param: text Text to be translated (default: 'translation !')
        @param: src Language to translate text from
        (default: 'en')
        @param: dest List of languages to return translated text in
        (default: ['fr'])
        """
        if not isinstance(text, str) and not isinstance(text, unicode):
            raise(AttributeError(
                'translate(text=) you must pass string of text to be'
                ' translated'))
        if str(src) not in self.languages:
            raise(AttributeError(
                'translate(src=) passed language is not supported: ' + src))
        if not isinstance(dest, list):
            raise(AttributeError(
                'translate(dest=) you must pass list of strings of supported'
                ' languages'))
        for dl in dest:
            if str(dl) not in self.languages:
                if self.fail_safe:
                    return text
                else:
                    raise(AttributeError(
                        'translate(dest=[]) passed language is not '
                        'supported: ' + str(dl)))
        if self.fail_safe:
            T = google_translator()

            class translatorC(object):
                def translate(self, text, dest, src):
                    try:
                        return T.translate(
                            text=text,
                            dest=dest,
                            src=src
                        )
                    except Exception:  # pragma: nocover
                        return text
            translator = translatorC()
        else:
            translator = google_translator()
        if self.cache and text in self.STORAGE.keys():
            if len(dest) > 1:
                toReturn = {}
                for dl in dest:
                    if dl in self.STORAGE[text].keys():
                        toReturn[dl] = self.STORAGE[text][dl]
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
                if dest[0] not in self.STORAGE[text].keys():
                    toRetTra = translator.translate(
                        text,
                        dest[0],
                        src
                    ).text
                    self.STORAGE[text][dest[0]] = toRetTra
                    self.cacheIt()
                    return toRetTra
                else:
                    return self.STORAGE[text][dest[0]]
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
            with open(self.file_name, 'r+') as file:
                self.STORAGE = load(file)
        except Exception:  # pragma: nocover
            raise(IOError(
                'Translator() failed to load cached '
                'file ' + self.file_name))

    def cacheIt(self):
        """
        function to overwrite the cached translation file
        """
        jsonData = dumps(
            self.STORAGE, indent=4, separators=(',', ': '), sort_keys=True
        )
        jsonData = jsonData.decode(
            'unicode-escape').encode('utf8') if V.major == 2 else jsonData
        with open(self.file_name, 'w+') as file:
            file.write(jsonData)
        self.loadCache()

    def gtranRoute(self):
        """ to setup a route on /gtran/<froml>/<tol>/<text> for dynamic
        fetching """

        @self.app.route('/gtran/<froml>/<tol>/<text>')
        def gttsRoute(froml, tol, text):
            return jsonify(translation=self.translate(
                str(text),
                str(froml),
                [str(tol)],
                ).replace('%5C', '/'))

    def appLoading(self):
        """ events to load flask app with """

        @self.app.context_processor
        def inject_vars():
            """ to inject translate function into the template """
            return dict(translate=self.translate)
        if self.cache:

            @self.app.after_request
            def todo(resp):
                """ to cache the new translation after the request is done """
                self.cacheIt()
                return resp
