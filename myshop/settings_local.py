

from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DEBUG = True
ALLOWED_HOSTS =  ['.localhost', '127.0.0.1', '[::1]']
# ...
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
