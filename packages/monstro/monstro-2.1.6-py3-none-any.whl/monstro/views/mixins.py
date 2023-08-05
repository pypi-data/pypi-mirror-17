# coding=utf-8

import tornado.gen

import bson
import bson.errors

from monstro.orm import Or, Regex


class RedirectResponseMixin(object):

    redirect_url = None
    permanent = True

    def get_redirect_url(self):
        assert self.redirect_url, (
            'RedirectResponseMixin requires either a definition of '
            '"redirect_url" or an implementation of "get_redirect_url()"'
        )

        return self.redirect_url


class ModelResponseMixin(object):

    model = None

    def get_model(self):
        assert self.model, (
            'ModelResponseMixin requires either a definition of '
            '"model" or an implementation of "get_model()"'
        )

        return self.model


class QuerysetResponseMixin(ModelResponseMixin):

    queryset = None

    @tornado.gen.coroutine
    def get_queryset(self):
        model = self.get_model()

        assert self.queryset or model, (
            'QuerysetResponseMixin requires either a definition of '
            '"queryset" or an implementation of "get_queryset()"'
        )

        return self.queryset or model.objects.filter()


class ListResponseMixin(QuerysetResponseMixin):

    pagination = None
    search_fields = None
    search_query_argument = 'q'

    def get_search_fields(self):
        return self.search_fields or []

    def get_pagination(self):
        return self.pagination

    @tornado.gen.coroutine
    def paginate(self):
        queryset = yield self.get_queryset()
        pagination = self.get_pagination()
        search_fields = self.get_search_fields()
        search_query = self.get_query_argument(self.search_query_argument, '')

        if search_fields and search_query:
            query = Or(Regex({f: search_query for f in search_fields}))
            queryset = queryset.filter(**query)

        if pagination:
            pagination.bind(**self.request.GET)
            return (yield pagination.paginate(queryset))

        return queryset


class DetailResponseMixin(QuerysetResponseMixin):

    lookup_field = '_id'

    @tornado.gen.coroutine
    def get_object(self):
        value = self.path_kwargs.get(self.lookup_field)

        if self.lookup_field == '_id':
            try:
                value = bson.objectid.ObjectId(value)
            except bson.errors.InvalidId:
                return self.send_error(404, reason='Object not found')

        query = {self.lookup_field: value}
        queryset = yield self.get_queryset()

        try:
            return (yield queryset.get(**query))
        except queryset.model.DoesNotExist:
            return self.send_error(404, reason='Object not found')
