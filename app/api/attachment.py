#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.model import auth
from app.model.attachment import Attachment
from app.model.process import Process
from app.model.report import DischargeReport, FactorReport
from app.util.common import metric

attachment_detail_fields = {
    'attachmentId': fields.String,
    'fileModelId': fields.String,
    'fileType': fields.String,
    'fileName': fields.String,
    'url': fields.String,
    'size': fields.Integer,
}

attachment_item_fields = {
    'attachmentId': fields.String,
    'fileName': fields.String,
    'url': fields.String,
    'size': fields.Integer,
}

attachment_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(attachment_item_fields), attribute=lambda p: p.items)
}


class AttachmentResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(attachment_detail_fields)
    def get(self, attachment_id):
        return Attachment.query.get_or_abort(attachment_id)


class AttachmentCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(attachment_list_fields)
    def get(self, discharge_report_id=None, factor_report_id=None, process_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('dischargeReportId', default=None)
        parser.add_argument('factorReportId', default=None)
        parser.add_argument('processId', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if discharge_report_id or args['dischargeReportId']:
            query = DischargeReport.query.get_or_abort(
                discharge_report_id if discharge_report_id else args.pop('dischargeReportId')).attachments
        elif factor_report_id or args['factorReportId']:
            query = FactorReport.query.get_or_abort(
                factor_report_id if factor_report_id else args.pop('factorReportId')).attachments
        elif process_id or args['processId']:
            query = Process.query.get_or_abort(process_id if process_id else args.pop('processId')).attachments
        else:
            query = Attachment.query
        if query:
            return query.paginate(current_page, page_size, False)
        else:
            return query


api.add_resource(AttachmentResource, '/attachments/<int:attachment_id>')
api.add_resource(AttachmentCollectionResource, '/attachments',
                 '/dischargeReports/<int:discharge_report_id>/attachments',
                 '/factorReports/<int:factor_report_id>/attachments', '/processes/<int:process_id>/attachments')
