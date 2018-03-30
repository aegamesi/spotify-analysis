from flask import Flask, session, redirect, url_for, abort
import flask_dance.contrib.spotify
import json
import secret
import spotipy
import string
import random

app = Flask(__name__)
app.debug = secret.DEBUG
app.secret_key = secret.SECRET_KEY

blueprint = flask_dance.contrib.spotify.make_spotify_blueprint(
    client_id=secret.SPOTIFY_CLIENT_ID,
    client_secret=secret.SPOTIFY_CLIENT_SECRET,
    scope='user-library-read',
    redirect_to='index')
app.register_blueprint(blueprint, url_prefix='/login')

def make_spotipy():
    return spotipy.Spotify(auth=flask_dance.contrib.spotify.spotify.token['access_token'])

@app.route('/auth')
def auth():
    if not flask_dance.contrib.spotify.spotify.authorized:
        return redirect(url_for('spotify.login'))

@app.route('/go')
def go():
    if 'spotify_id' not in session:
        return redirect(url_for('index'))
    sp = make_spotipy()
    me = sp.current_user()
    filename = 'db/%s.json' % me['id']

    # Fetching saved tracks
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Fetching Audio Features
    audio_features = []
    start = 0
    while start < len(tracks):
        ids = [t['track']['id'] for t in tracks[start:start+50]]
        results = sp.audio_features(ids)
        audio_features.extend(results)
        start += len(results)

    key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(32)).lower()
    data = {'tracks': tracks, 'audio_features': audio_features, 'me': me, 'key': key}
    with open(filename, 'w') as f:
        json.dump(data, f)

    return redirect(url_for('analysis', user_id=me['id'], key=key))

@app.route('/analysis')
def analysis_redirect():
    if 'spotify_id' not in session:
        return redirect(url_for('index'))
    try:
        filename = 'db/%s.json' % session['spotify_id']
        with open(filename) as f:
            data = json.load(f)
            return redirect(url_for('analysis', user_id=session['spotify_id'], key=data['key']))
    except FileNotFoundError:
        return redirect(url_for('go'))
    return '?'

@app.route('/analysis/<user_id>/<key>')
def analysis(user_id, key):
    filename = 'db/%s.json' % user_id
    try:
        with open(filename) as f:
            data = json.load(f)
            if key.strip().lower() != data['key']:
                abort(404)
    except FileNotFoundError:
        abort(404)

    return '<pre>%s</pre>' % json.dumps(data, indent=4)

@app.route('/')
def index():
    if not flask_dance.contrib.spotify.spotify.authorized:
        return 'Please <a href="%s">authenticate with Spotify</a>.' % url_for('spotify.login')
    
    if 'spotify_id' not in session:
        sp = make_spotipy()
        me = sp.current_user()
        session['spotify_id'] = me['id']
    return 'Hi %s' % session['spotify_id']

