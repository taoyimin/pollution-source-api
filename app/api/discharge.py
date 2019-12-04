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
from app.model.report import Report, DischargeReport, FactorReport
from app.util.common import metric

discharge_detail_fields = {
    'dischargeId': fields.String,
    'enterId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'dischargeName': fields.String,
    'dischargeShortName': fields.String,
    'dischargeAddress': fields.String,
    'dischargeNumber': fields.String,
    'dischargeTypeStr': fields.String,
    'outTypeStr': fields.String,
    'denoterInstallTypeStr': fields.String,
    'dischargeRuleStr': fields.String,
    'dischargeCategoryStr': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
    'dischargeReportTotalCount': fields.String,
    'factorReportTotalCount': fields.String,
}

discharge_item_fields = {
    'dischargeId': fields.String,
    'enterName': fields.String,
    'dischargeName': fields.String,
    'dischargeCategoryStr': fields.String,
    'dischargeTypeStr': fields.String,
    'dischargeRuleStr': fields.String,
    'dischargeAddress': fields.String
}

discharge_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(discharge_item_fields), attribute=lambda p: p.items)
}


class DischargeResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(discharge_detail_fields)
    def get(self, discharge_id=None, monitor_id=None, report_id=None, discharge_report_id=None, factor_report_id=None):
        if discharge_id:
            return Discharge.query.get_or_abort(discharge_id)
        elif monitor_id:
            return Monitor.query.get_or_abort(monitor_id).discharge
        elif report_id:
            return Report.query.get_or_abort(report_id).discharge
        elif discharge_report_id:
            return DischargeReport.query.get_or_abort(discharge_report_id).discharge
        elif factor_report_id:
            return FactorReport.query.get_or_abort(factor_report_id).discharge


class DischargeCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(discharge_list_fields)
    def get(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=None)
        parser.add_argument('dischargeType', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id or args['enterId']:
            query = Enter.query.get_or_abort(enter_id if enter_id else args.pop('enterId')).discharges
        else:
            query = Discharge.query.filter_by_user()
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(DischargeResource, '/discharges/<int:discharge_id>', '/monitors/<int:monitor_id>/discharge',
                 '/reports/<int:report_id>/discharge', '/dischargeReports/<int:discharge_report_id>/discharge',
                 '/factorReports/<int:factor_report_id>/discharge')
api.add_resource(DischargeCollectionResource, '/discharges', '/enters/<int:enter_id>/discharges')
