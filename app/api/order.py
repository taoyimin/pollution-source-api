#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask import g
from flask_restful import marshal_with, Resource, fields, reqparse, abort

from app.api import api
from app.api.enter import enter_detail_fields
from app.model import auth
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.model.order import Order
from app.util.common import metric, filter_none

order_detail_fields = {
    'enterName': fields.String(attribute=lambda order: order.enter.enterName),
    'enterAddress': fields.String(attribute=lambda order: order.enter.enterAddress),
    'monitorName': fields.String(attribute=lambda order: order.monitor.monitorName),
    'orderId': fields.Integer,
    'enterId': fields.Integer,
    'monitorId': fields.Integer,
    'alarmRemark': fields.String,
    # 'enter': fields.Nested(enter_detail_fields)
}

order_item_fields = {
    'enterName': fields.String(attribute=lambda order: order.enter.enterName),
    'monitorName': fields.String(attribute=lambda order: order.monitor.monitorName),
    'orderId': fields.Integer,
    'alarmRemark': fields.String,
    # 'enter': fields.Nested(enter_detail_fields)
}

order_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(order_item_fields), attribute=lambda pagination: pagination.items)
}


class OrderResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(order_detail_fields)
    def get(self, order_id):
        # return Order.query.get_or_404(order_id, description='id=%d的报警管理单不存在' % order_id)
        return Order.query.get_or_abort(order_id)


class OrderCollectionResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(order_list_fields)
    def get(self, enter_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id:
            # query = Enter.query.get_or_404(enter_id, description='id=%d的企业不存在' % enter_id).orders
            query = Enter.query.get_or_abort(enter_id).orders
        elif monitor_id:
            # query = Monitor.query.get_or_404(monitor_id, description='id=%d的监控点不存在' % monitor_id).orders
            query = Monitor.query.get_or_abort(monitor_id).orders
        else:
            query = Order.query.filter_by_user()
        return query.order_by(Order.orderId) \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(OrderCollectionResource, '/orders', '/enters/<int:enter_id>/orders',
                 '/monitors/<int:monitor_id>/orders')
