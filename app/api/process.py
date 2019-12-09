#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
import werkzeug
from flask import g
from flask_restful import marshal_with, Resource, fields, reqparse, abort

import app
from app.api import api, upload_return_fields
from app.api.attachment import attachment_detail_fields, attachment_item_fields
from app.model import auth, db
from app.model.attachment import Attachment
from app.model.order import Order
from app.model.process import Process
from app.util.common import metric, valid_not_empty, save_file

process_detail_fields = {
    'processId': fields.String,
    'orderId': fields.String,
    'operatePerson': fields.String,
    'operateTypeStr': fields.String,
    'operateTimeStr': fields.String,
    'operateDesc': fields.String,
    'attachments': fields.List(fields.Nested(attachment_detail_fields))
}

process_item_fields = {
    'processId': fields.String,
    'operatePerson': fields.String,
    'operateTypeStr': fields.String,
    'operateTimeStr': fields.String,
    'operateDesc': fields.String,
    'attachments': fields.List(fields.Nested(attachment_item_fields)),
}

process_list_fields = {
    'total': fields.Integer(attribute=lambda p: p.total),
    'currentPage': fields.Integer(attribute=lambda p: p.page),
    'pageSize': fields.Integer(attribute=lambda p: p.per_page),
    'hasNext': fields.Boolean(attribute=lambda p: p.has_next),
    'list': fields.List(fields.Nested(process_item_fields), attribute=lambda p: p.items)
}


class ProcessResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(process_detail_fields)
    def get(self, process_id):
        return Process.query.get_or_abort(process_id)


class ProcessCollectionResource(Resource):
    decorators = [auth.login_required]

    @metric
    @marshal_with(process_list_fields)
    def get(self, order_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('orderId', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if order_id or args['orderId']:
            query = Order.query.get_or_abort(order_id if order_id else args.pop('orderId')).processes
        else:
            query = Process.query
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)

    # @marshal_with(upload_return_fields)
    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('operatePerson', required=True, type=valid_not_empty)
    #     parser.add_argument('operateType', required=True, type=valid_not_empty)
    #     parser.add_argument('operateDesc', required=True, type=valid_not_empty)
    #     parser.add_argument('orderId', required=True, type=valid_not_empty)
    #     parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=False, action='append')
    #     args = parser.parse_args()
    #     if g.type == app.app.config['ADMIN_USER_TYPE']:
    #         # 环保用户
    #         args['operateUnit'] = g.user.globalLevel
    #     elif g.type == app.app.config['ENTER_USER_TYPE']:
    #         # 企业用户
    #         args['operateUnit'] = 'company'
    #     else:
    #         abort(400, message='未知的用户类型，type=%d' % g.type)
    #     files = args.pop('file')
    #     report = Process(**args)
    #     db.session.add(report)
    #     db.session.flush()
    #     if files:
    #         for file in files:
    #             args = save_file(file)
    #             args['fileModelId'] = report.reportId
    #             args['fileModel'] = app.app.config['DISCHARGE_REPORT_FILE_MODEL']
    #             args['fileType'] = app.app.config['DISCHARGE_REPORT_FILE_TYPE']
    #             attachment = Attachment(**args)
    #             db.session.add(attachment)
    #             db.session.flush()
    #     db.session.commit()
    #     return {'success': True, 'message': '提交成功'}


api.add_resource(ProcessResource, '/processes/<int:process_id>')
api.add_resource(ProcessCollectionResource, '/processes', '/orders/<int:order_id>/processes')
