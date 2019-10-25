#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask import g
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.model import auth
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.model.user import User
from app.util.common import metric

monitor_fields = {
    'monitorId': fields.Integer,
    'monitorName': fields.String,
    'monitorAddress': fields.String,
}

monitor_collection_fields = {
    'total': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'has_next': fields.Boolean,
    'items': fields.List(fields.Nested(monitor_fields))
}


class MonitorResource(Resource):

    @metric
    @marshal_with(monitor_fields)
    def get(self, monitor_id):
        """
        查询单个监控点的信息
        :param monitor_id: 监控点id
        :return: 监控点实体类
        """
        return Monitor.query.get_or_404(monitor_id)


class MonitorCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(monitor_collection_fields)
    def get(self, enter_id=None):
        """
        获取监控点集合信息
        :return: 监控点集合
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()
        if enter_id:
            return Enter.query.get_or_404(enter_id).monitors.paginate(args['page'], args['per_page'], False)
        else:
            return Monitor.query.join(Enter).filter(User.get_district_criterion(g.user)) \
                .paginate(args['page'], args['per_page'], False)


api.add_resource(MonitorResource, '/monitors/<int:monitor_id>')
api.add_resource(MonitorCollectionResource, '/monitors', '/enters/<int:enter_id>/monitors')
