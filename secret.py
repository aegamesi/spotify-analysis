import os

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', '') == '1'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' if DEBUG else '0'
