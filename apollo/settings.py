# -*- coding: utf-8 -*-
import ast
import os
import string
from urlparse import urlparse

SECRET_KEY = os.environ.get('SECRET_KEY', 'SOMETHING_SECURE')
DEBUG = ast.literal_eval(
    os.environ.get('DEBUG', 'False'))
PAGE_SIZE = 25

if os.environ.get('container') == 'lxc':
    MONGO_ENV_NAME = 'MONGODB_PORT'
else:
    MONGO_ENV_NAME = 'MONGO_DATABASE_HOST'

MONGODB_SETTINGS = {
    'DB': os.environ.get('MONGO_DATABASE_NAME', 'apollo'),
    'HOST': urlparse(
        os.environ.get(MONGO_ENV_NAME, 'mongodb://localhost')).netloc
}

SECURITY_PASSWORD_HASH = 'pbkdf2_sha256'
SECURITY_PASSWORD_SALT = SECRET_KEY
SECURITY_URL_PREFIX = '/accounts'
SECURITY_LOGIN_USER_TEMPLATE = 'frontend/login_user.html'
SECURITY_EMAIL_SENDER = 'no-reply@apollo.la'
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'az': 'Azərbaycanca',
    'ar': 'العربية',
    'de': 'Deutsch',
}

ALLOWED_PUNCTUATIONS = '!'
CHARACTER_TRANSLATIONS = (
    ('i', '1'),
    ('I', '1'),
    ('o', '0'),
    ('O', '0'),
    ('l', '1'),
    ('L', '1'),
)
PUNCTUATIONS = filter(lambda s: s not in ALLOWED_PUNCTUATIONS,
                      string.punctuation) + ' '
TRANS_TABLE = dict((ord(char_from), ord(char_to))
                   for char_from, char_to in
                   CHARACTER_TRANSLATIONS)
MESSAGING_OUTGOING_GATEWAY = {
    'type': 'kannel',
    'gateway_url': 'http://localhost:13013/cgi-bin/sendsms',
    'username': 'foo',
    'password': 'bar'
}
