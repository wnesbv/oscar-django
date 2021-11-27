

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import CharField, DecimalField
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from oscar.core import validators
from oscar.forms import fields
from oscar.models.fields.autoslugfield import AutoSlugField

AutoSlugField = AutoSlugField
PhoneNumberField = PhoneNumberField


# https://github.com/django/django/blob/64200c14e0072ba0ffef86da46b2ea82fd1e019a/django/db/models/fields/subclassing.py#L31-L44
class Creator(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class ExtendedURLField(CharField):
    description = _("URL")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get("max_length", 200)
        CharField.__init__(self, *args, **kwargs)
        self.validators.append(validators.ExtendedURLValidator())

    def formfield(self, **kwargs):
        defaults = {
            "form_class": fields.ExtendedURLField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.max_length == 200:
            del kwargs["max_length"]
        return name, path, args, kwargs


class PositiveDecimalField(DecimalField):
    def formfield(self, **kwargs):
        return super().formfield(min_value=0)


class UppercaseCharField(CharField):
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, Creator(self))

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        val = super().to_python(value)
        if isinstance(val, str):
            return val.upper()
        else:
            return val


class NullCharField(CharField):
    description = "CharField that stores '' as None and returns None as ''"

    def __init__(self, *args, **kwargs):
        if not kwargs.get("null", True) or not kwargs.get("blank", True):
            raise ImproperlyConfigured("NullCharField implies null==blank==True")
        kwargs["null"] = kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, Creator(self))

    def from_db_value(self, value, *args, **kwargs):
        value = self.to_python(value)
        return value if value is not None else ""

    def get_prep_value(self, value):
        prepped = super().get_prep_value(value)
        return prepped if prepped != "" else None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs
