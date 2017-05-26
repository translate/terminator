from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


# test_data.json contains a SHA1 hashed password
PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.SHA1PasswordHasher',
]

