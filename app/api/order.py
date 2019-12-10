#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.api.process import process_item_fields
from app.model import auth
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.model.order import Order
from app.model.process import Process
from app.util.common import metric

order_detail_fields = {
    'orderId': fields.String,
    'enterId': fields.String,
    'monitorId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'monitorName': fields.String,
    'alarmDateStr': fields.String,
    'districtName': fields.String,
    'orderLevelStr': fields.String,
    'orderStateStr': fields.String,
    'alarmTypeStr': fields.String,
    'alarmRemark': fields.String,
    'processes': fields.List(fields.Nested(process_item_fields))
}

order_item_fields = {
    'orderId': fields.String,
    'enterName': fields.String,
    'monitorName': fields.String,
    'alarmDateStr': fields.String,
    'districtName': fields.String,
    'orderStateStr': fields.String,
    'alarmTypeStr': fields.String,
    'alarmRemark': fields.String,
}

order_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(order_item_fields), attribute=lambda pagination: pagination.items)
}


class OrderResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(order_detail_fields)
    def get(self, order_id=None, process_id=None):
        if order_id:
            return Order.query.get_or_abort(order_id)
        elif process_id:
            return Process.query.get_or_abort(process_id).order


class OrderCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(order_list_fields)
    def get(self, enter_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=enter_id)
        parser.add_argument('monitorId', default=monitor_id)
        parser.add_argument('state', type=str, default='')
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).orders
        elif args['monitorId']:
            query = Monitor.query.get_or_abort(args.pop('monitorId')).orders
        else:
            query = Order.query.filter_by_user()
        return query.filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(OrderResource, '/orders/<int:order_id>', '/processes/<int:process_id>/order')
api.add_resource(OrderCollectionResource, '/orders', '/enters/<int:enter_id>/orders',
                 '/monitors/<int:monitor_id>/orders')
