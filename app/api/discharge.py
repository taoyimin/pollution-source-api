#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask import g
from flask_restful import marshal_with, Resource, fields, reqparse, abort

from app.api import api
from app.api.enter import enter_detail_fields
from app.model import auth
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.util.common import metric, filter_none

discharge_detail_fields = {
    'dischargeId': fields.Integer,
    'dischargeName': fields.String,
    'dischargeAddress': fields.String,
    'enter': fields.Nested(enter_detail_fields)
}

discharge_item_fields = {
    'dischargeId': fields.Integer,
    'dischargeName': fields.String,
    'dischargeAddress': fields.String,
    # 'enter': fields.Nested(enter_detail_fields)
}

discharge_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(discharge_item_fields), attribute=lambda pagination: pagination.items)
}


class DischargeResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(discharge_detail_fields)
    def get(self, discharge_id):
        return Discharge.query.get_or_abort(discharge_id)


class DischargeCollectionResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(discharge_list_fields)
    def get(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id:
            query = Enter.query.get_or_abort(enter_id).discharges
        else:
            query = Discharge.query.filter_by_user()
        return query.order_by(Discharge.dischargeId) \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(DischargeResource, '/discharges/<int:discharge_id>')
api.add_resource(DischargeCollectionResource, '/discharges', '/enters/<int:enter_id>/discharges')
