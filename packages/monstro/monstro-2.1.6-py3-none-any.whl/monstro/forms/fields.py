# coding=utf-8

import re
import json
import urllib.parse
import datetime

import tornado.gen

from . import widgets
from .exceptions import ValidationError


class Field(object):

    widget = None
    default_error_messages = {
        'required': 'Value is required',
        'invalid': 'Value is invalid',
        'unique': 'Value must be unique',
        'read_only': 'Read-only value'
    }

    def __init__(self, *, name=None, required=True, default=None, label=None,
                 unique=False, help_text=None, read_only=False,
                 validators=None, error_messages=None, widget=None):

        """Initialization instance.

        :param required (optional): value is required flag.
        :type required: bool.
        :param default (optional): default value.
        :type default: type.
        :param validators (optional): additional validators.
        :type validators: iterable of callable.
        :param error_messages (optional): custom error messages.
        :type error_messages: dict.
        """
        self.name = name
        self.required = required
        self.default = default
        self.label = label
        self.unique = unique
        self.help_text = help_text
        self.read_only = read_only
        self.validators = validators or []
        self.widget = widget or self.widget

        messages = {}

        for cls in reversed(self.__class__.__mro__):
            messages.update(getattr(cls, 'default_error_messages', {}))

        messages.update(error_messages or {})

        self.error_messages = messages

    def bind(self, **kwargs):
        self.__dict__.update(kwargs)

    @tornado.gen.coroutine
    def validate(self, value=None, model=None):
        if value is None:
            if callable(self.default):
                value = self.default()
            else:
                value = self.default

        if value is None:
            if self.required:
                self.fail('required')
            else:
                return None

        yield self.is_valid(value)

        for validator in self.validators:
            yield validator(value)

        if self.unique and hasattr(self, 'model'):
            try:
                instance = yield self.model.objects.get(**{self.name: value})
            except self.model.DoesNotExist:
                instance = None

            if instance and model and instance._id != model._id:
                self.fail('unique')

        return (yield self.to_internal_value(value))

    def fail(self, error_code, **kwargs):
        raise ValidationError(
            self.error_messages[error_code].format(self, **kwargs), self.name
        )

    @tornado.gen.coroutine
    def is_valid(self, value):
        raise NotImplementedError()

    @tornado.gen.coroutine
    def to_representation(self, value):
        return value

    @tornado.gen.coroutine
    def to_python(self, value):
        return value

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        return value

    @tornado.gen.coroutine
    def get_metadata(self):
        metadata = {
            'name': self.name,
            'label': self.label or (self.name and self.name.title()),
            'help_text': self.help_text,
            'required': self.required,
            'read_only': self.read_only,
        }

        if not (self.default is None or callable(self.default)):
            metadata['default'] = yield self.to_internal_value(self.default)
        else:
            metadata['default'] = None

        if self.widget:
            metadata['widget'] = self.widget.get_metadata()
        else:
            metadata['widget'] = None

        return metadata


class Type(Field):

    type = type
    widget = widgets.Input('text')
    default_error_messages = {
        'invalid': 'Value must be a valid {0.type.__name__}'
    }

    @tornado.gen.coroutine
    def is_valid(self, value):
        if not isinstance(value, self.type):
            self.fail('invalid')


class Boolean(Type):

    type = bool
    widget = widgets.Input('checkbox')
    default_error_messages = {
        'invalid': 'Value must be a valid boolean'
    }


class String(Type):

    type = str
    default_error_messages = {
        'invalid': 'Value must be a valid string',
        'min_length': 'String must be greater {0.min_length} characters',
        'max_length': 'String must be less {0.max_length} characters'
    }

    def __init__(self, *, min_length=None, max_length=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(**kwargs)

    @tornado.gen.coroutine
    def is_valid(self, value):
        yield super().is_valid(value)

        if self.min_length is not None and len(value) < self.min_length:
            self.fail('min_length')

        if self.max_length is not None and len(value) > self.max_length:
            self.fail('max_length')

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        if value is not None:
            return str(value)


class Numeric(Type):

    default_error_messages = {
        'invalid': 'Value must be a valid integer or float',
        'min_value': 'Number must be greater {0.min_value} characters',
        'max_value': 'Number must be less {0.max_value} characters'
    }

    def __init__(self, *, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(**kwargs)

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        try:
            return self.type(value)
        except (TypeError, ValueError):
            return None

    @tornado.gen.coroutine
    def to_python(self, value):
        return (yield self.to_internal_value(value))

    @tornado.gen.coroutine
    def to_representation(self, value):
        return (yield self.to_internal_value(value))

    @tornado.gen.coroutine
    def is_valid(self, value):
        value = yield self.to_internal_value(value)

        if value is None:
            self.fail('invalid')

        if self.min_value is not None and value < self.min_value:
            self.fail('min_value')

        if self.max_value is not None and value > self.max_value:
            self.fail('max_value')


class Integer(Numeric):

    type = int
    default_error_messages = {
        'invalid': 'Value must be a valid integer',
    }


class Float(Numeric):

    type = float
    default_error_messages = {
        'invalid': 'Value must be a valid float',
    }


class Choice(Field):

    default_error_messages = {
        'invalid': 'Value must be in {choices}',
    }

    def __init__(self, *, choices, **kwargs):
        """Initialization instance.

        :param choices: choices.
        :type choices: iterable.
        """
        self.choices = list(choices)
        self.widget = widgets.Select(self.choices)
        super().__init__(**kwargs)

    @tornado.gen.coroutine
    def is_valid(self, value):
        choices = [choice[0] for choice in self.choices]

        if value not in choices:
            self.fail('invalid', choices=choices)


class Array(Type):

    type = list
    widget = widgets.TextArea()
    default_error_messages = {
        'invalid': 'Value must be a valid array',
        'child': '{index}: {message}'
    }

    def __init__(self, *, field=None, **kwargs):
        self.field = field
        super().__init__(**kwargs)

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        try:
            yield self.is_valid(value)
        except ValidationError:
            return None

        if self.field:
            values = []

            for item in value:
                values.append((yield self.field.to_internal_value(item)))

            return values

        return value

    @tornado.gen.coroutine
    def to_python(self, value):
        try:
            yield self.is_valid(value)
        except ValidationError:
            return None

        if self.field:
            values = []

            for item in value:
                values.append((yield self.field.to_python(item)))

            return values

        return value

    @tornado.gen.coroutine
    def to_representation(self, value):
        try:
            yield self.is_valid(value)
        except ValidationError:
            return None

        if self.field:
            values = []

            for item in value:
                values.append((yield self.field.to_representation(item)))

            return values

        return value

    @tornado.gen.coroutine
    def is_valid(self, value):
        yield super().is_valid(value)

        if self.field:
            for index, item in enumerate(value):
                try:
                    yield self.field.validate(item)
                except ValidationError as e:
                    self.fail('child', index=index, message=e.error)


class MultipleChoice(Array, Choice):

    default_error_messages = {
        'choices': 'All values must be in {choices}',
    }

    def __init__(self, **kwargs):
        Choice.__init__(self, **kwargs)
        Array.__init__(self, **kwargs)

        self.widget.attributes['multiple'] = True

    @tornado.gen.coroutine
    def is_valid(self, value):
        yield Array.is_valid(self, value)

        choices = [choice[0] for choice in self.choices]

        if any(choice not in choices for choice in value):
            self.fail('choices', choices=choices)


class Url(String):

    default_error_messages = {
        'url': 'Value must be a valid URL',
    }

    @tornado.gen.coroutine
    def is_valid(self, value):
        yield super().is_valid(value)

        url = urllib.parse.urlparse(value)

        if not (url.scheme and url.netloc):
            self.fail('url')


class RegexMatch(String):

    default_error_messages = {
        'pattern': 'Value must match by {0.pattern}',
    }

    def __init__(self, *, pattern=None, **kwargs):
        self.pattern = re.compile(pattern or self.pattern)
        super().__init__(**kwargs)

    @tornado.gen.coroutine
    def is_valid(self, value):
        yield super().is_valid(value)

        if not self.pattern.match(value):
            self.fail('pattern')


class Host(RegexMatch):

    default_error_messages = {
        'pattern': 'Value must be a valid host',
    }
    pattern = (
        # domain
        r'(?:[\w](?:[\w-]{0,61}[\w])?\.)+'
        r'(?:[A-Za-z]{2,6}\.?|[\w-]{2,}\.?$)'
        # ipv4 address
        r'|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    )


class Slug(RegexMatch):

    default_error_messages = {
        'pattern': 'Value must be a valid slug',
    }
    pattern = r'^[a-zA-Z\d\-_]+$'


class Map(Field):

    widget = widgets.TextArea()
    default_error_messages = {
        'invalid': 'Value must be a map or JSON string',
    }

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                return None

        return value

    @tornado.gen.coroutine
    def to_python(self, value):
        return (yield self.to_internal_value(value))

    @tornado.gen.coroutine
    def is_valid(self, value):
        value = yield self.to_internal_value(value)

        if not isinstance(value, dict):
            self.fail('invalid')


class DateTime(Field):

    widget = widgets.Input('datetime')
    default_error_messages = {
        'invalid': 'Datetime must be in next formats: {0.input_formats}'
    }

    default_format = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, *, input_formats=None, output_format=None,
                 auto_now=False, auto_now_on_create=False, **kwargs):
        super().__init__(**kwargs)
        self.input_formats = [self.default_format] + (input_formats or [])
        self.output_format = output_format or self.default_format
        self.auto_now = auto_now
        self.auto_now_on_create = auto_now_on_create

        if self.auto_now or self.auto_now_on_create or self.default:
            self.required = False

        if (self.auto_now_on_create or self.auto_now) and self.default is None:
            self.default = datetime.datetime.now

    @property
    def available_formats(self):
        return list(set(self.input_formats + [self.output_format]))

    @tornado.gen.coroutine
    def to_internal_value(self, value):
        if self.auto_now:
            value = datetime.datetime.now()

        if isinstance(value, str):
            for input_format in self.available_formats:
                try:
                    value = datetime.datetime.strptime(value, input_format)
                    break
                except ValueError:
                    continue
            else:
                return None

        return value.strftime(self.output_format)

    @tornado.gen.coroutine
    def to_python(self, value):
        for input_format in self.available_formats:
            try:
                return datetime.datetime.strptime(value, input_format)
            except (TypeError, ValueError):
                continue

    @tornado.gen.coroutine
    def is_valid(self, value):
        if self.auto_now:
            return

        if isinstance(value, str):
            for input_format in self.available_formats:
                try:
                    datetime.datetime.strptime(value, input_format)
                    break
                except ValueError:
                    continue
            else:
                self.fail('invalid')
        elif not hasattr(value, 'strftime'):
            self.fail('invalid')

    @tornado.gen.coroutine
    def to_representation(self, value):
        if value is not None:
            return value.strftime(self.output_format)


class Date(DateTime):

    widget = widgets.Input('date')
    default_error_messages = {
        'invalid': 'Date must be in next formats: {0.input_formats}'
    }

    default_format = '%Y-%m-%d'

    @tornado.gen.coroutine
    def to_python(self, value):
        value = yield super().to_python(value)

        if value:
            return value.date()


class Time(DateTime):

    widget = widgets.Input('time')
    default_error_messages = {
        'invalid': 'Time must be in next formats: {0.input_formats}'
    }

    default_format = '%H:%M:%S'

    @tornado.gen.coroutine
    def to_python(self, value):
        value = yield super().to_python(value)

        if value:
            return value.time()
