from flask import Flask
from flask import abort, redirect, send_from_directory, render_template, g, request
import readFirefox
import argparse

app = Flask(__name__)
localData = {'profilePath': None, 'browserData': None}

# Serve static content
@app.route('/bootstrap/<path:path>')
def send_static_files(path):
    return send_from_directory('bootstrap', path)

def filterFunc(_q):
    q = _q # TODO regex + ignore case
    return lambda o: q in o.text

@app.route('/')
def main_page():
    return render_template('base.html', info = get_data().browserInfo)

@app.route('/inputdata')
def input_data():
    q = request.args.get('q')
    t = None
    if q :
        filtered = filter(filterFunc(q), get_data().formInput)
        t = render_template('inputdata.html', items = filtered, q = q)
    else:
        t = render_template('inputdata.html', items = get_data().formInput, q = '')
    return t

@app.route('/places')
def places_data():
    q = request.args.get('q') or ''
    hq = request.args.get('hq') or ''
    filtered = get_data().places
    if q :
        filtered = filter(filterFunc(q), filtered)
    if hq:
        filtered = filter(lambda o: hq in o.url, filtered)    
    
    return render_template('places.html', items = filtered, q = q, hq = hq)

@app.route('/cookies')
def cookies_data():
    q = request.args.get('q') or ''
    filtered = get_data().cookies
    if q:
        filtered = filter(lambda o: q in o.host, filtered)
    return render_template('cookies.html', items = filtered, q = q)

@app.route('/reload')
def reload_data():
    localData['browserData'] = readFirefox.readAll(localData['profilePath'])
    return redirect('/')

def get_data():
    return localData['browserData']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start Browser Info. If started with no arguments active directory will be used as profile. By default http://localhost:5000 is used.')
    parser.add_argument('--path', help='Path to browser profile')
    parser.add_argument('--debug', help='Debug mode', action='store_true')
    args = parser.parse_args()
    localData['profilePath'] = args.path if args.path else ''
    localData['browserData'] = readFirefox.readAll(localData['profilePath'])
    app.debug = args.debug is True
    app.run()
