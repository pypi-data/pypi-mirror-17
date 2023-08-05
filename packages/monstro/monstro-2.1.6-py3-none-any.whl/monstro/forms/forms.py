# coding=utf-8

import copy
import collections

import tornado.gen

from . import exceptions
from .fields import Field


class MetaForm(type):

    @classmethod
    def __prepare__(mcs, *args, **kwargs):
        return collections.OrderedDict()

    def __new__(mcs, name, bases, attributes):
        fields = collections.OrderedDict()

        for parent in bases:
            if hasattr(parent, '__fields__'):
                fields.update(parent.__fields__)

        for name, field in attributes.items():
            if isinstance(field, Field):
                fields[name] = field

        for field in fields:
            attributes.pop(field, None)

        cls = type.__new__(mcs, name, bases, attributes)

        cls.__fields__ = fields
        cls.ValidationError = exceptions.ValidationError

        for name, field in cls.__fields__.items():
            field.bind(name=name)

        return cls


class Form(object, metaclass=MetaForm):

    def __init__(self, *, instance=None, data=None):
        self.__instance__ = instance
        self.__values__ = {name: None for name in self.__fields__.keys()}

        if self.__instance__ is not None:
            for name in self.__fields__.keys():
                self.__values__[name] = getattr(self.__instance__, name, None)

        if data is not None:
            for name in self.__fields__.keys():
                self.__values__[name] = data.get(name, self.__values__[name])

    def __getattr__(self, attribute):
        if attribute in self.__fields__:
            field = self.__fields__[attribute]
            return self.__values__.get(attribute, field.default)

        raise AttributeError(attribute)

    def __setattr__(self, attribute, value):
        if attribute in self.__fields__:
            self.__values__[attribute] = value
        else:
            return super().__setattr__(attribute, value)

    @tornado.gen.coroutine
    def to_internal_value(self):
        data = {}

        for name, field in self.__fields__.items():
            value = self.__values__.get(name, field.default)
            data[name] = yield field.to_internal_value(value)

        return data

    @classmethod
    @tornado.gen.coroutine
    def get_metadata(cls):
        metadata = []

        for field in cls.__fields__.values():
            metadata.append((yield field.get_metadata()))

        return metadata

    @tornado.gen.coroutine
    def serialize(self):
        data = {}

        for name, field in self.__fields__.items():
            value = self.__values__.get(name, field.default)
            data[name] = yield field.to_representation(value)

        return data

    @tornado.gen.coroutine
    def construct(self):
        for name, field in self.__fields__.items():
            value = self.__values__.get(name, field.default)
            self.__values__[name] = yield field.to_python(value)

    @tornado.gen.coroutine
    def validate(self):
        errors = {}

        for name, field in self.__fields__.items():
            try:
                value = self.__values__.get(name, field.default)

                if field.read_only and value != field.default:
                    if not self.__instance__:
                        field.fail('read_only')

                self.__values__[name] = yield field.validate(value, self)
            except exceptions.ValidationError as e:
                errors[name] = e.error

        if errors:
            raise exceptions.ValidationError(errors)

        return copy.copy(self.__values__)

    @tornado.gen.coroutine
    def save(self):
        pass
