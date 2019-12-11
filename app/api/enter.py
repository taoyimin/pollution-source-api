#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.model import auth
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.model.order import Order
from app.model.report import Report, DischargeReport, FactorReport, LongStopReport

enter_detail_fields = {
    'enterId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'enterTel': fields.String,
    'contactPerson': fields.String,
    'contactPersonTel': fields.String,
    'legalPerson': fields.String,
    'legalPersonTel': fields.String,
    'districtName': fields.String,
    'attentionLevelStr': fields.String,
    'enterTypeStr': fields.String,
    'industryTypeStr': fields.String,
    'creditCode': fields.String,
    'orderCompleteCount': fields.String,
    'orderTotalCount': fields.String,
    'longStopReportTotalCount': fields.String,
    'dischargeReportTotalCount': fields.String,
    'factorReportTotalCount': fields.String,
    'monitorTotalCount': fields.String,
    'monitorOnlineCount': fields.String,
    'monitorAlarmCount': fields.String,
    'monitorOverCount': fields.String,
    'monitorOfflineCount': fields.String,
    'monitorStopCount': fields.String,
    'licenseNumber': fields.String
}

enter_item_fields = {
    'enterId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'attentionLevel': fields.String,
    'enterType': fields.String,
    'industryTypeStr': fields.String
}

enter_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(enter_item_fields), attribute=lambda p: p.items)
}


class EnterResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(enter_detail_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None, order_id=None, report_id=None,
            long_stop_report_id=None, discharge_report_id=None, factor_report_id=None):
        if enter_id:
            return Enter.query.get_or_abort(enter_id)
        elif discharge_id:
            return Discharge.query.get_or_abort(discharge_id).enter
        elif monitor_id:
            return Monitor.query.get_or_abort(monitor_id).enter
        elif order_id:
            return Order.query.get_or_abort(order_id).enter
        elif report_id:
            return Report.query.get_or_abort(report_id).enter
        elif long_stop_report_id:
            return LongStopReport.query.get_or_abort(long_stop_report_id).enter
        elif discharge_report_id:
            return DischargeReport.query.get_or_abort(discharge_report_id).enter
        elif factor_report_id:
            return FactorReport.query.get_or_abort(factor_report_id).enter


class EnterCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(enter_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterName', default=None)
        parser.add_argument('enterType', default=None)
        parser.add_argument('attentionLevel', default=None)
        parser.add_argument('cityCode', default=None)
        parser.add_argument('areaCode', default=None)
        parser.add_argument('countyCode', default=None)
        parser.add_argument('state', type=str, default='')
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        return Enter.query.filter_by_user() \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(EnterResource, '/enters/<int:enter_id>', '/discharges/<int:discharge_id>/enter',
                 '/monitors/<int:monitor_id>/enter', '/orders/<int:order_id>/enter', '/reports/<int:report_id>/enter',
                 '/longStopReports/<int:long_stop_report_id>/enter',
                 '/dischargeReports/<int:discharge_report_id>/enter', '/factorReports/<int:factor_report_id>/enter')
api.add_resource(EnterCollectionResource, '/enters')
