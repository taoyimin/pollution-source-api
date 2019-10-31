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
from app.model.report import Report
from app.util.common import metric

report_detail_fields = {
    'reportId': fields.Integer,
    'enterId': fields.Integer,
    'dischargeId': fields.Integer,
    'monitorId': fields.Integer,
    'enterName': fields.String(attribute=lambda r: r.enter.enterName),
    'enterAddress': fields.String(attribute=lambda r: r.enter.enterAddress),
    'dischargeName': fields.String(attribute=lambda r: r.discharge.dischargeName),
    'monitorName': fields.String(attribute=lambda r: r.monitor.monitorName),
    'reason': fields.String
}

report_item_fields = {
    'reportId': fields.Integer,
    'enterId': fields.Integer,
    'dischargeId': fields.Integer,
    'monitorId': fields.Integer,
    'enterName': fields.String(attribute=lambda r: r.enter.enterName),
    'dischargeName': fields.String(attribute=lambda r: r.discharge.dischargeName),
    'monitorName': fields.String(attribute=lambda r: r.monitor.monitorName),
    'reason': fields.String
}

report_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(report_item_fields), attribute=lambda p: p.items)
}


class ReportResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(report_detail_fields)
    def get(self, report_id):
        return Report.query.get_or_abort(report_id)


class ReportCollectionResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(report_list_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if enter_id:
            query = Enter.query.get_or_abort(enter_id).reports
        elif discharge_id:
            query = Discharge.query.get_or_abort(discharge_id).reports
        elif monitor_id:
            query = Monitor.query.get_or_abort(monitor_id).reports
        else:
            query = Report.query.filter_by_user()
        return query.order_by(Report.reportId) \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(ReportResource, '/reports/<int:report_id>')
api.add_resource(ReportCollectionResource, '/reports', '/enters/<int:enter_id>/reports',
                 '/discharges/<int:discharge_id>/reports', '/monitors/<int:monitor_id>/reports')
