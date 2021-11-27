

import datetime
import secrets
from string import ascii_letters, digits
from django.utils import timezone


def generate_nonce():
    alphabet = ascii_letters + digits
    nonce = "".join(secrets.choice(alphabet) for _ in range(40))
    return nonce

def get_datetime_now():
    try:
        return timezone.now()  # pragma: no cover
    except ImportError:  # pragma: no cover
        return datetime.datetime.now()