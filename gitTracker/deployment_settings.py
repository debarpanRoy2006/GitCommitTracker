import os
import dj_database_url
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)

ALLOWED_HOSTS = ["gitcommittracker.onrender.com", "localhost", "127.0.0.1"]

# STATIC files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tracker", "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MIDDLEWARE.insert(
    1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

# Templates location
TEMPLATES[0]["DIRS"] = [
    os.path.join(BASE_DIR, "tracker", "templates"),
]

# Database config
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
    )
}
