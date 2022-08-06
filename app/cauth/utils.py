import datetime
from django.conf import settings
from django.http import HttpResponse


from django.core.exceptions import ValidationError
from django import forms


def valid_email(email: str):
    try:
        f = forms.EmailField()
        f.clean(email)
    except ValidationError as ve:
        print("ve", email, ve)
        return False
    return True

def set_cookie(response: HttpResponse, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )
