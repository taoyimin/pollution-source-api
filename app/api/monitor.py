#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.model import auth
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.util.common import metric

monitor_detail_fields = {
    'monitorId': fields.Integer,
    'monitorName': fields.String,
    'monitorAddress': fields.String
}

monitor_item_fields = {
    'monitorId': fields.Integer,
    'monitorName': fields.String,
    'monitorAddress': fields.String
}

monitor_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(monitor_item_fields), attribute=lambda p: p.items)
}


class MonitorResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(monitor_detail_fields)
    def get(self, monitor_id):
        return Monitor.query.get_or_abort(monitor_id)


class MonitorCollectionResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(monitor_list_fields)
    def get(self, enter_id=None, discharge_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id:
            query = Enter.query.get_or_abort(enter_id).monitors
        elif discharge_id:
            query = Discharge.query.get_or_abort(discharge_id).monitors
        else:
            query = Monitor.query.filter_by_user()
        return query.order_by(Monitor.monitorId) \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(MonitorResource, '/monitors/<int:monitor_id>')
api.add_resource(MonitorCollectionResource, '/monitors', '/enters/<int:enter_id>/monitors',
                 '/discharges/<int:discharge_id>/monitors')
