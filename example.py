from flask import Flask, render_template
from flask_googletrans import translator
from atexit import register
from os import remove


app = Flask(__name__, template_folder='.')
ts = translator(app=app, cache=True, fail_safe=True)

def cleanUp():
    try:
        remove('index.html')
    except Exception:
        pass

register(cleanUp)

@app.route('/')
def root():
    # for m in flashMessages:
    #     ts.translate(text=m, src='en', dest=['fr', 'es', 'ar', 'it'])
    with open('index.html', 'w+') as file:
        file.write("<h1 align='center'>{{ translate(text='the new thing which is a long one jus to see', dest=['fr', 'it', 'es', 'ar'])['ar'] }}</h1>")
        file.write("<h1 align='center'>{{ translate(text='nothing', dest=['fr', 'it', 'es', 'ar'])['ar'] }}</h1>")
        file.write("<h1 align='center'>{{ translate(text='the real thing', dest=['fr', 'ar'])['fr'] }}</h1>")
    return render_template('index.html')


app.run(debug=True, port=4000)