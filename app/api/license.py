#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:23
from flask_restful import marshal_with, Resource, fields, reqparse

from app.api import api
from app.api.attachment import attachment_item_fields
from app.model import auth
from app.model.enter import Enter
from app.model.license import License, LicenseFactor

license_factor_detail_fields = {
    'factorId': fields.String,
    'licenseId': fields.String,
    'factorName': fields.String,
    'yearAllowDischargeTotal': fields.String,
    'dayAllowDischargeTotal': fields.String,
    'allowDischargeDensity': fields.String,
}

license_factor_item_fields = {
    'factorId': fields.String,
    'factorName': fields.String,
    'yearAllowDischargeTotal': fields.String,
    'dayAllowDischargeTotal': fields.String,
    'allowDischargeDensity': fields.String,
}

license_factor_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(license_factor_item_fields), attribute=lambda pagination: pagination.items)
}

license_detail_fields = {
    'licenseId': fields.String,
    'enterName': fields.String,
    'issueUnitStr': fields.String,
    'issueTimeStr': fields.String,
    'licenseTimeStr': fields.String,
    'validTimeStr': fields.String,
    'licenseManagerTypeStr': fields.String,
    'licenseNumber': fields.String,
    'dischargeMode': fields.String,
    'dischargeCode': fields.String,
    'yearWaterDischargeTotal': fields.String,
    'dayWaterDischargeTotal': fields.String,
    'firstYearDischargeTotal': fields.String,
    'secondYearDischargeTotal': fields.String,
    'thirdYearDischargeTotal': fields.String,
    'allowSewage': fields.String,
    'notApproveReason': fields.String,
    'remark': fields.String,
    'attachments': fields.List(fields.Nested(attachment_item_fields)),
    'licenseFactors': fields.List(fields.Nested(license_factor_item_fields)),
}

license_item_fields = {
    'licenseId': fields.String,
    'enterName': fields.String,
    'issueUnitStr': fields.String,
    'issueTimeStr': fields.String,
    'licenseTimeStr': fields.String,
    'validTimeStr': fields.String,
    'licenseManagerTypeStr': fields.String,
    'licenseNumber': fields.String,
}

license_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(license_item_fields), attribute=lambda pagination: pagination.items)
}


class LicenseResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(license_detail_fields)
    def get(self, license_id=None, factor_id=None):
        if license_id:
            return License.query.get_or_abort(license_id)
        elif factor_id:
            return LicenseFactor.query.get_or_abort(factor_id).license


class LicenseCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(license_list_fields)
    def get(self, enter_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('enterId', default=enter_id)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['enterId']:
            query = Enter.query.get_or_abort(args.pop('enterId')).licenses
        else:
            query = License.query.filter_by_user()
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)


class LicenseFactorResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(license_factor_detail_fields)
    def get(self, factor_id):
        return LicenseFactor.query.get_or_abort(factor_id)


class LicenseFactorCollectionResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(license_factor_list_fields)
    def get(self, license_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        parser.add_argument('licenseId', default=license_id)
        args = parser.parse_args()
        current_page = args.pop('currentPage')
        page_size = args.pop('pageSize')
        if args['licenseId']:
            query = License.query.get_or_abort(args.pop('licenseId')).licenseFactors
        else:
            query = LicenseFactor.query
        return query.filter_by_args(args) \
            .paginate(current_page, page_size, False)


api.add_resource(LicenseResource, '/licenses/<int:license_id>', '/licenseFactors/<int:factor_id>/license')
api.add_resource(LicenseCollectionResource, '/licenses', '/enters/<int:enter_id>/licenses')
api.add_resource(LicenseFactorResource, '/licenseFactors/<int:factor_id>')
api.add_resource(LicenseFactorCollectionResource, '/licenseFactors', '/licenses/<int:license_id>/licenseFactors')
