#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.model import auth
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.factor import Factor
from app.model.monitor import Monitor

factor_detail_fields = {
    'factorId': fields.String,
    'factorCode': fields.String,
    'factorName': fields.String,
}

factor_item_fields = {
    'factorName': fields.String,
}

factor_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(factor_item_fields), attribute=lambda p: p.items)
}


class FactorResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(factor_detail_fields)
    def get(self, factor_id):
        return Factor.query.get_or_abort(factor_id)


class FactorCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(factor_list_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('factorCode', default=None)
        parser.add_argument('enterId', default=enter_id)
        parser.add_argument('dischargeId', default=discharge_id)
        parser.add_argument('monitorId', default=monitor_id)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).factors
        elif args['dischargeId']:
            query = Discharge.query.get_or_abort(args.pop('dischargeId')).factors
        elif args['monitorId']:
            query = Monitor.query.get_or_abort(args.pop('monitorId')).factors
        else:
            query = Factor.query
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(FactorResource, '/factors/<int:factor_id>')
api.add_resource(FactorCollectionResource, '/factors', '/enters/<int:enter_id>/factors',
                 '/discharges/<int:discharge_id>/factors', '/monitors/<int:monitor_id>/factors')
