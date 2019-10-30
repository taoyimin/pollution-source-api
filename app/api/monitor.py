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
from app.util.common import metric, filter_none

monitor_detail_fields = {
    'monitorId': fields.Integer,
    'monitorName': fields.String,
    'monitorAddress': fields.String,
    # 'enter': fields.Nested(enter_detail_fields)
}

monitor_item_fields = {
    'monitorId': fields.Integer,
    'monitorName': fields.String,
    'monitorAddress': fields.String,
    # 'enter': fields.Nested(enter_detail_fields)
}

monitor_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(monitor_item_fields), attribute=lambda pagination: pagination.items)
}


class MonitorResource(Resource):

    @metric
    @marshal_with(monitor_detail_fields)
    def get(self, monitor_id):
        return Monitor.query.get_or_404(monitor_id, description='id=%d的监控点不存在' % monitor_id)


class MonitorCollectionResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(monitor_list_fields)
    def get(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id:
            query = Enter.query.get_or_404(enter_id, description='id=%d的企业不存在' % enter_id).monitors
        else:
            query = Monitor.query.join(Enter).filter(g.user.get_district_criterion())
        return query.filter_by(**filter_none(args)).paginate(current_page, page_size, False)


api.add_resource(MonitorResource, '/monitors/<int:monitor_id>')
api.add_resource(MonitorCollectionResource, '/monitors', '/enters/<int:enter_id>/monitors')
