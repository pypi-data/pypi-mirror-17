# -*- coding: utf-8 -*-
"""
   The Eefesto Resources module.

   Copyright (C) 2016 Jacopo Cascioli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
from datetime import datetime
import falcon


from peewee import FieldDescriptor, RelationDescriptor
from .Auth import (authenticate_by_password, authenticate_by_token,
                   generate_token)
from .Models import EternalTokens
from .Siren import hinder


def model_columns(model):
    columns = []
    for i in model.__dict__:
        if isinstance(model.__dict__[i], FieldDescriptor):
            if not isinstance(model.__dict__[i], RelationDescriptor):
                columns.append(i)
    return columns


def build_fields(request):
    fields = ['id']
    if '_fields' in request.params:
        if request.params['_fields'] != 'all':
            fields = request.params['_fields'].split(',')
            fields.append('id')
        else:
            fields = 'all'
    return fields


def build_query(model, params):
    query = model.select()
    for key, argument in params.items():
        if argument[0] == '<':
            query = query.where(getattr(model, key) <= argument[1:])
        elif argument[0] == '>':
            query = query.where(getattr(model, key) >= argument[1:])
        elif argument[0] == '!':
            query = query.where(getattr(model, key) != argument[1:])
        else:
            query = query.where(getattr(model, key) == argument)
    return query


def build_item(columns, fields, currrent_item):
    item = {}
    for column in columns:
        if column in fields or fields == 'all':
            item[column] = getattr(currrent_item, column)
    return item


def build_order(model, query, order):
    if order[0] == '<':
        query = query.order_by(getattr(model, order[1:]).desc())
    elif order[0] == '>':
        query = query.order_by(getattr(model, order[1:]).asc())
    else:
        query = query.order_by(getattr(model, order).asc())
    return query


def build_link_headers(request, response, count, items, page):
    domain = '{}://{}?page=%s&items={}'.format(request.protocol,
                                               request.host, items)
    last_page = int(count / items)

    if page != 1:
        prev_page = page - 1
        url = domain % (prev_page)
        response.add_link(url, rel='prev')

    if page != last_page:
        last_url = domain % (last_page)
        response.add_link(last_url, rel='last')
        next_page = page + 1
        if next_page != last_page:
            next_url = domain % (next_page)
            response.add_link(next_url, rel='next')


def item_to_dictionary(model, item):
    item_dict = {}
    for k in model.__dict__:
        if isinstance(model.__dict__[k], FieldDescriptor):
            if not isinstance(model.__dict__[k], RelationDescriptor):
                item_dict[k] = getattr(item, k)
    return item_dict


def last_page(count, items):
    pages = int(count / items)
    if pages == 0:
        return 1
    return pages


def on_get(self, request, response):
    user = None
    if request.auth:
        user = authenticate_by_token(request.auth)

    if user is None:
        raise falcon.HTTPUnauthorized('Login required', 'Please login',
                                      ['Basic realm="Login Required"'])

    columns = model_columns(self.model)
    params = {}
    for i in columns:
        if i in request.params:
            params[i] = request.params[i]

    page = 1
    if 'page' in request.params:
        page = int(request.params['page'])

    items = 20
    if 'items' in request.params:
        items = int(request.params['items'])

    order = None
    if 'order_by' in request.params:
        order = request.params['order_by']

    fields = build_fields(request)

    query = build_query(self.model, params)
    if order is not None:
        query = build_order(self.model, query, order)
    count = query.count()

    body = []
    for i in query.paginate(page, items):
        if user.can('read', i):
            item = build_item(columns, fields, i)
            body.append(item)

    if len(body) == 0:
        raise falcon.HTTPNotFound()

    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError('Type not serializable')
    pages = last_page(count, items)
    s = hinder(body, path=request.path, page=page, last_page=pages)
    response.body = json.dumps(s, default=json_serial)

    if count > items:
        build_link_headers(request, response, count, items, page)


def on_post(self, request, response):
    request._parse_form_urlencoded()
    user = None
    if request.auth:
        user = authenticate_by_token(request.auth)

    if user is None:
        raise falcon.HTTPUnauthorized('Login required', 'Please login',
                                      ['Basic realm="Login Required"'])

    new_item = self.model(**request.params)
    if user.can('read', new_item):
        new_item.save()
        response.status = falcon.HTTP_CREATED
        path = '{}/{}'.format(request.path, new_item.id)
        s = hinder(new_item.__dict__['_data'], path=path)
        response.body = json.dumps(s)
    else:
        raise falcon.HTTPForbidden('forbidden', 'forbidden')


def on_get_resource(self, request, response, id=0):
    user = None
    if request.auth:
        user = authenticate_by_token(request.auth)

    if user is None:
        raise falcon.HTTPUnauthorized('Login required', 'Please login',
                                      ['Basic realm="Login Required"'])

    try:
        item = self.model.get(getattr(self.model, 'id') == id)
    except:
        raise falcon.HTTPNotFound()

    if user.can('read', item):
        item_dict = item_to_dictionary(self.model, item)

        def json_serial(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError('Type not serializable')
        s = hinder(item_dict, path=request.path)
        response.body = json.dumps(s, default=json_serial)
    else:
        raise falcon.HTTPForbidden('forbidden', 'forbidden')


def on_patch_resource(self, request, response, id=0):
    user = None
    if request.auth:
        user = authenticate_by_token(request.auth)

    if user is None:
        raise falcon.HTTPUnauthorized('Login required', 'Please login',
                                      ['Basic realm="Login Required"'])

    try:
        item = self.model.get(getattr(self.model, 'id') == id)
    except:
        raise falcon.HTTPNotFound()

    if user.can('edit', item):
        stream = request.stream.read().decode('UTF-8')
        if len(stream) > 0:
            for i in stream.split('&'):
                arg = i.split('=')
                setattr(item, arg[0], arg[1])
            item.save()

        item_dict = item_to_dictionary(self.model, item)
        s = hinder(item_dict, path=request.path)
        response.body = json.dumps(s)
    else:
        raise falcon.HTTPForbidden('forbidden', 'forbidden')


def on_delete_resource(self, request, response, id=0):
    user = None
    if request.auth:
        user = authenticate_by_token(request.auth)

    if user is None:
        raise falcon.HTTPUnauthorized('Login required', 'Please login',
                                      ['Basic realm="Login Required"'])

    try:
        item = self.model.get(getattr(self.model, 'id') == id)
    except:
        raise falcon.HTTPNotFound()

    if user.can('eliminate', item):
        item.delete_instance()
        response.status = falcon.HTTP_NO_CONTENT
    else:
        raise falcon.HTTPForbidden('forbidden', 'forbidden')


def make_collection(model):
    """
    The make_collection function acts as generator of collection for models.
    """
    attributes = {
        'model': model,
        'on_get': on_get,
        'on_post': on_post
    }
    return type('mycollection', (object, ), attributes)


def make_resource(model):
    attributes = {
        'model': model,
        'on_get': on_get_resource,
        'on_patch': on_patch_resource,
        'on_delete': on_delete_resource
    }
    return type('mycollection', (object, ), attributes)


class TokensResource:
    """
    The TokensResource resource handles tokens requests.
    """
    def on_post(self, request, response):
        request._parse_form_urlencoded()
        if ('password' not in request.params or
                'username' not in request.params):
            raise falcon.HTTPBadRequest('', '')

        authentication = authenticate_by_password(request.params['username'],
                                                  request.params['password'])
        if authentication is None:
            raise falcon.HTTPUnauthorized('Login required', 'Pleas login',
                                          ['Basic realm="Login Required"'])

        if 'token_name' in request.params:
            try:
                t = EternalTokens.get(
                    EternalTokens.name == request.params['token_name'],
                    EternalTokens.user == authentication.id
                ).token
            except:
                raise falcon.HTTPNotFound()
            token = generate_token(token=t)
        else:
            token = generate_token(user=request.params['username'])
        response.status = falcon.HTTP_OK
        response.body = json.dumps({'token': token})


class RootResource:
    """
    The RootResource resource handles requests made to the root endpoint.
    """
    def __init__(self, data):
        self.data = data

    def on_get(self, request, response):
        response.body = json.dumps(self.data)
