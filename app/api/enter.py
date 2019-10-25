#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
from flask import g
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.api.monitor import monitor_fields
from app.model import auth, db
from app.model.district import District
from app.model.enter import Enter
from app.model.user import User
from app.util.common import metric

enter_fields = {
    'enterId': fields.Integer,
    'enterName': fields.String,
    'enterAddress': fields.String
    # 'monitors': fields.List(fields.Nested(monitor_fields)),
}

enter_collection_fields = {
    'total': fields.Integer,
    'items': fields.List(fields.Nested(enter_fields)),
    'page': fields.Integer,
    'per_page': fields.Integer,
    'has_next': fields.Boolean
}


class EnterResource(Resource):

    @metric
    @marshal_with(enter_fields)
    def get(self, enter_id):
        """
        查询单个企业的信息
        :param enter_id:
        :return: 企业实体类
        """
        return Enter.query.get(enter_id)


class EnterCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(enter_collection_fields)
    def get(self):
        """
        获取企业集合信息
        :return: 企业集合
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()
        pagination = Enter.query.filter(Enter.areaCode.in_(g.user['districts'].split(','))).paginate(
            args['page'], args['per_page'], False)
        return {'total': pagination.total, 'page': pagination.page, 'per_page': pagination.per_page,
                'has_next': pagination.has_next,
                'items': pagination.items}


api.add_resource(EnterResource, '/enters/<int:enter_id>')
api.add_resource(EnterCollectionResource, '/enters')
