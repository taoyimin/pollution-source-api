#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:05
from flask_restful import marshal_with, Resource, fields, reqparse
from sqlalchemy import func

from app.api import api
from app.model import auth, db
from app.model.enter import Enter
from app.util.common import metric

enter_detail_fields = {
    'enterId': fields.Integer,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'attentionLevel': fields.String,
    'enterType': fields.String,
    'industryTypeStr': fields.String(
        attribute=lambda enter:
        db.session.query(func.enterprise_archives.dbo.getAreaOrInstulyName(enter.industryType, 'industry')).first()[0])
}

enter_item_fields = {
    'enterId': fields.Integer,
    'enterName': fields.String,
    'enterAddress': fields.String,
    'attentionLevel': fields.String,
    'enterType': fields.String,
    'industryTypeStr': fields.String(
        attribute=lambda enter:
        db.session.query(func.enterprise_archives.dbo.getAreaOrInstulyName(enter.industryType, 'industry')).first()[0])
}

enter_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(enter_item_fields), attribute=lambda pagination: pagination.items)
}


class EnterResource(Resource):

    @metric
    @auth.login_required
    @marshal_with(enter_detail_fields)
    def get(self, enter_id):
        return Enter.query.get_or_abort(enter_id)


class EnterCollectionResource(Resource):

    @metric
    @auth.login_required
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
        parser.add_argument('state', default=None)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        return Enter.query \
            .order_by(Enter.enterId) \
            .filter_by_user() \
            .filter_by_state(args.pop('state')) \
            .filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(EnterResource, '/enters/<int:enter_id>')
api.add_resource(EnterCollectionResource, '/enters')
