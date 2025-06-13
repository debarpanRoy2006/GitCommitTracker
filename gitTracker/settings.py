import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dummysecretkey'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gitTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gitTracker.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CORS_ALLOWED_ORIGINS = [
    "https://debarpanroy2006.github.io",
]
# settings.py
# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week in seconds (60 seconds * 60 minutes * 24 hours * 7 days)


# --- AUTHENTICATION SETTINGS ---
# Where Django redirects after a successful login (e.g., your dashboard or profile)
LOGIN_REDIRECT_URL = '/profile/'

# Where Django redirects after logout
LOGOUT_REDIRECT_URL = '/home/' # Or your home page URL name


# --- GITHUB OAuth SETTINGS ---
# Get these from environment variables in production, NEVER hardcode them.
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

# This is your application's public callback URL on Heroku (or your custom domain)
# Make sure this matches exactly what you registered on GitHub.
# Example for Heroku: 'https://your-app-name.herokuapp.com/callback/github/'
# Example for custom domain: 'https://www.yourdomain.com/callback/github/'
GITHUB_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI')

# If you use a personal access token for higher API rate limits for `get_commits_api`
# GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')