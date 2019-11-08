#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.api.attachment import attachment_detail_fields, attachment_item_fields
from app.model import auth
from app.model.process import Process
from app.util.common import metric

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
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        return Process.query.paginate(current_page, page_size, False)


api.add_resource(ProcessResource, '/processes/<int:process_id>')
api.add_resource(ProcessCollectionResource, '/processes')
