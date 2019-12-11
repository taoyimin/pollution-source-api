#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
import werkzeug
from flask_restful import marshal_with, Resource, fields, reqparse

import app
from app.api import api, upload_return_fields
from app.api.attachment import attachment_item_fields
from app.model import auth, db
from app.model.attachment import Attachment
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.model.report import Report, DischargeReport, FactorReport, LongStopReport
from app.util.common import valid_not_empty, save_file

report_detail_fields = {
    'reportId': fields.String,
    'enterId': fields.String,
    'dischargeId': fields.String,
    'monitorId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'dischargeName': fields.String,
    'monitorName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'dataType': fields.String,
    'alarmType': fields.String,
    'state': fields.String,
}

report_item_fields = {
    'reportId': fields.String,
    'enterName': fields.String,
    'dischargeName': fields.String,
    'monitorName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'dataType': fields.String,
    'alarmType': fields.String,
}

report_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(report_item_fields), attribute=lambda p: p.items)
}

long_stop_report_detail_fields = {
    'reportId': fields.String,
    'enterId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String,
    'remark': fields.String
}

long_stop_report_item_fields = {
    'reportId': fields.String,
    'enterName': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String
}

long_stop_report_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(long_stop_report_item_fields), attribute=lambda p: p.items)
}

discharge_report_detail_fields = {
    'reportId': fields.String,
    'enterId': fields.String,
    'dischargeId': fields.String,
    'monitorId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'dischargeName': fields.String,
    'monitorName': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String,
    'stopTypeStr': fields.String,
    'stopReason': fields.String,
    'state': fields.String,
    'attachments': fields.List(fields.Nested(attachment_item_fields))
}

discharge_report_item_fields = {
    'reportId': fields.String,
    'enterName': fields.String,
    'monitorName': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String,
    'stopTypeStr': fields.String,
}

discharge_report_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(discharge_report_item_fields), attribute=lambda p: p.items)
}

factor_report_detail_fields = {
    'reportId': fields.String,
    'enterId': fields.String,
    'dischargeId': fields.String,
    'monitorId': fields.String,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'dischargeName': fields.String,
    'monitorName': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String,
    'alarmTypeStr': fields.String,
    'factorCodeStr': fields.String,
    'exceptionReason': fields.String,
    'state': fields.String,
    'attachments': fields.List(fields.Nested(attachment_item_fields))
}

factor_report_item_fields = {
    'reportId': fields.String,
    'enterName': fields.String,
    'monitorName': fields.String,
    'districtName': fields.String,
    'startTimeStr': fields.String,
    'endTimeStr': fields.String,
    'reportTimeStr': fields.String,
    'alarmTypeStr': fields.String,
    'factorCodeStr': fields.String,
}

factor_report_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(factor_report_item_fields), attribute=lambda p: p.items)
}


class ReportResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(report_detail_fields)
    def get(self, report_id):
        return Report.query.get_or_abort(report_id)


class ReportCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(report_list_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', type=str, default=enter_id)
        parser.add_argument('dischargeId', default=discharge_id)
        parser.add_argument('monitorId', default=monitor_id)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).reports
        elif args['dischargeId']:
            query = Discharge.query.get_or_abort(args.pop('dischargeId')).reports
        elif args['monitorId']:
            query = Monitor.query.get_or_abort(args.pop('monitorId')).reports
        else:
            query = Report.query.filter_by_user()
        return query.filter_by_args(args).paginate(current_page, page_size, False)


class LongStopReportResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(long_stop_report_detail_fields)
    def get(self, report_id):
        return LongStopReport.query.get_or_abort(report_id)


class LongStopReportCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(long_stop_report_list_fields)
    def get(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=enter_id)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).longStopReports
        else:
            query = LongStopReport.query.filter_by_user()
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)

    @marshal_with(upload_return_fields)
    def post(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('startTime', required=True, type=valid_not_empty)
        parser.add_argument('endTime', required=True, type=valid_not_empty)
        parser.add_argument('remark', required=True, type=valid_not_empty)
        # parser.add_argument('enterId', required=True, type=valid_not_empty)
        parser.add_argument('enterId', required=enter_id is None, default=enter_id, type=valid_not_empty)
        args = parser.parse_args()
        args['dataType'] = 'L'
        report = LongStopReport(**args)
        db.session.add(report)
        db.session.commit()
        return {'success': True, 'message': '提交成功'}


class DischargeReportResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(discharge_report_detail_fields)
    def get(self, report_id):
        return DischargeReport.query.get_or_abort(report_id)


class DischargeReportCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(discharge_report_list_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=enter_id)
        parser.add_argument('dischargeId', default=discharge_id)
        parser.add_argument('monitorId', default=monitor_id)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).dischargeReports
        elif args['dischargeId']:
            query = Discharge.query.get_or_abort(args.pop('dischargeId')).dischargeReports
        elif args['monitorId']:
            query = Monitor.query.get_or_abort(args.pop('monitorId')).dischargeReports
        else:
            query = DischargeReport.query.filter_by_user()
        return query.filter_by_args(args).paginate(current_page, page_size, False)

    @marshal_with(upload_return_fields)
    def post(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('alarmType', required=True, type=valid_not_empty)
        parser.add_argument('startTime', required=True, type=valid_not_empty)
        parser.add_argument('endTime', required=True, type=valid_not_empty)
        parser.add_argument('stopReason', required=True, type=valid_not_empty)
        # parser.add_argument('enterId', required=True, type=valid_not_empty)
        # parser.add_argument('dischargeId', required=True, type=valid_not_empty)
        # parser.add_argument('monitorId', required=True, type=valid_not_empty)
        parser.add_argument('enterId', required=enter_id is None, default=enter_id, type=valid_not_empty)
        parser.add_argument('dischargeId', required=discharge_id is None, default=discharge_id, type=valid_not_empty)
        parser.add_argument('monitorId', required=monitor_id is None, default=monitor_id, type=valid_not_empty)
        parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=False, action='append')
        args = parser.parse_args()
        args['dataType'] = 'S'
        files = args.pop('file')
        report = DischargeReport(**args)
        db.session.add(report)
        db.session.flush()
        if files:
            for file in files:
                file_args = save_file(file)
                file_args['fileModelId'] = report.reportId
                file_args['fileModel'] = app.app.config['DISCHARGE_REPORT_FILE_MODEL']
                file_args['fileType'] = app.app.config['DISCHARGE_REPORT_FILE_TYPE']
                attachment = Attachment(**file_args)
                db.session.add(attachment)
        db.session.commit()
        return {'success': True, 'message': '提交成功'}


class FactorReportResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(factor_report_detail_fields)
    def get(self, report_id):
        return FactorReport.query.get_or_abort(report_id)


class FactorReportCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(factor_report_list_fields)
    def get(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=enter_id)
        parser.add_argument('dischargeId', default=discharge_id)
        parser.add_argument('monitorId', default=monitor_id)
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).factorReports
        elif args['dischargeId']:
            query = Discharge.query.get_or_abort(args.pop('dischargeId')).factorReports
        elif args['monitorId']:
            query = Monitor.query.get_or_abort(args.pop('monitorId')).factorReports
        else:
            query = FactorReport.query.filter_by_user()
        return query.filter_by_args(args).paginate(current_page, page_size, False)

    @marshal_with(upload_return_fields)
    def post(self, enter_id=None, discharge_id=None, monitor_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('alarmType', required=True, type=valid_not_empty)
        parser.add_argument('factorCode', required=True, type=valid_not_empty)
        parser.add_argument('startTime', required=True, type=valid_not_empty)
        parser.add_argument('endTime', required=True, type=valid_not_empty)
        parser.add_argument('exceptionReason', required=True, type=valid_not_empty)
        # parser.add_argument('enterId', required=True, type=valid_not_empty)
        # parser.add_argument('dischargeId', required=True, type=valid_not_empty)
        # parser.add_argument('monitorId', required=True, type=valid_not_empty)
        parser.add_argument('enterId', required=enter_id is None, default=enter_id, type=valid_not_empty)
        parser.add_argument('dischargeId', required=discharge_id is None, default=discharge_id, type=valid_not_empty)
        parser.add_argument('monitorId', required=monitor_id is None, default=monitor_id, type=valid_not_empty)
        parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=False, action='append')
        args = parser.parse_args()
        args['dataType'] = 'A'
        files = args.pop('file')
        report = FactorReport(**args)
        db.session.add(report)
        db.session.flush()
        if files:
            for file in files:
                file_args = save_file(file)
                file_args['fileModelId'] = report.reportId
                file_args['fileModel'] = app.app.config['FACTOR_REPORT_FILE_MODEL']
                file_args['fileType'] = app.app.config['FACTOR_REPORT_FILE_TYPE']
                attachment = Attachment(**file_args)
                db.session.add(attachment)
        db.session.commit()
        return {'success': True, 'message': '提交成功'}


api.add_resource(ReportResource, '/reports/<int:report_id>')
api.add_resource(ReportCollectionResource, '/reports', '/enters/<int:enter_id>/reports',
                 '/discharges/<int:discharge_id>/reports', '/monitors/<int:monitor_id>/reports')
api.add_resource(LongStopReportResource, '/longStopReports/<int:report_id>')
api.add_resource(LongStopReportCollectionResource, '/longStopReports', '/enters/<int:enter_id>/longStopReports')
api.add_resource(DischargeReportResource, '/dischargeReports/<int:report_id>')
api.add_resource(DischargeReportCollectionResource, '/dischargeReports', '/enters/<int:enter_id>/dischargeReports',
                 '/discharges/<int:discharge_id>/dischargeReports', '/monitors/<int:monitor_id>/dischargeReports')
api.add_resource(FactorReportResource, '/factorReports/<int:report_id>')
api.add_resource(FactorReportCollectionResource, '/factorReports', '/enters/<int:enter_id>/factorReports',
                 '/discharges/<int:discharge_id>/factorReports', '/monitors/<int:monitor_id>/factorReports')
