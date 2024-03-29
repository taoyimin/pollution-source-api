#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16
from flask import g
from flask_restful import reqparse, Resource, fields, marshal_with, abort

from app.api import api
from app.model import db, auth
from app.model.user import AdminUser, EnterUser
from app.util.common import valid_user_name, valid_pass_word, valid_not_empty

user_detail_fields = {
    'userId': fields.Integer,
    'userName': fields.String,
    'realName': fields.String,
    'globalLevel': fields.String,
    'userLevel': fields.String,
    'orgId': fields.String,
    'districts': fields.String(attribute=lambda user: ','.join(map(lambda d: d.districtCode, user.districts)))
}

user_item_fields = {
    'userId': fields.Integer,
    'userName': fields.String,
    'realName': fields.String,
    'globalLevel': fields.String,
    'userLevel': fields.String
}

user_list_fields = {
    'total': fields.Integer(attribute=lambda pagination: pagination.total),
    'currentPage': fields.Integer(attribute=lambda pagination: pagination.page),
    'pageSize': fields.Integer(attribute=lambda pagination: pagination.per_page),
    'hasNext': fields.Boolean(attribute=lambda pagination: pagination.has_next),
    'list': fields.List(fields.Nested(user_item_fields), attribute=lambda pagination: pagination.items)
}


class AdminUserResource(Resource):
    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('userName', type=valid_user_name)
    #     self.parser.add_argument('passWord', type=valid_pass_word)
    #     self.parser.add_argument('realName', default=None)
    #     self.parser.add_argument('globalLevel', default=None)
    #     self.parser.add_argument('userLevel', default=None)
    #     super(UserResource, self).__init__()

    @marshal_with(user_detail_fields)
    def get(self, id=None, user_name=None):
        if id:
            user = AdminUser.query.get_or_404(id, description='id=%d的用户不存在' % id)
        else:
            user = AdminUser.query.filter_by(userName=user_name).first_or_404(description='用户名%s的用户不存在' % user_name)
        return user

    @auth.login_required
    @marshal_with(user_detail_fields)
    def put(self, id):
        user = AdminUser.query.get_or_404(id, description='id=%d的用户不存在' % id)
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=valid_user_name)
        parser.add_argument('passWord', type=valid_pass_word)
        parser.add_argument('realName')
        parser.add_argument('orgId')
        parser.add_argument('globalLevel')
        parser.add_argument('userLevel')
        args = parser.parse_args()
        if g.user.userId != id:
            abort(400, message='当前token与id=%d的用户不匹配，您只能修改当前token所属的用户信息' % id)
        for key, value in args.items():
            if value is not None:
                if key == 'userName' and AdminUser.query.filter(AdminUser.userId != id,
                                                                AdminUser.userName == value).scalar():
                    abort(400, message='用户名%s已经存在' % value)
                setattr(user, key, value)
        db.session.commit()
        return user


class AdminUserCollectionResource(Resource):
    @marshal_with(user_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('currentPage', type=int, default=1)
        parser.add_argument('pageSize', type=int, default=20)
        args = parser.parse_args()
        return AdminUser.query.paginate(args['currentPage'], args['pageSize'], False)

    @marshal_with(user_detail_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', required=True, type=valid_user_name)
        parser.add_argument('passWord', required=True, type=valid_pass_word)
        parser.add_argument('realName', required=True, type=valid_not_empty)
        parser.add_argument('orgId', required=True, type=valid_not_empty)
        parser.add_argument('globalLevel', required=True, type=valid_not_empty)
        parser.add_argument('userLevel', required=True, type=valid_not_empty)
        args = parser.parse_args()
        user = AdminUser(**args)
        if AdminUser.query.filter_by(userName=user.userName).scalar():
            abort(400, message='用户名%s已经存在' % user.userName)
        else:
            db.session.add(user)
            db.session.commit()
            return user


class AdminTokenResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=valid_user_name, required=True)
        parser.add_argument('passWord', type=valid_pass_word, required=True)
        args = parser.parse_args()
        user = AdminUser.query.filter_by(userName=args['userName']).first_or_404(
            description='用户名%s不存在' % args['userName'])
        if user.passWord == args['passWord']:
            token = user.generate_auth_token()
            return {'token': token}
        else:
            abort(400, message='密码错误')


class EnterTokenResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=valid_user_name, required=True)
        parser.add_argument('passWord', type=valid_pass_word, required=True)
        args = parser.parse_args()
        user = EnterUser.query.filter_by(userName=args['userName']).first_or_404(
            description='用户名%s不存在' % args['userName'])
        if user.passWord == args['passWord']:
            token = user.generate_auth_token()
            return {'token': token, 'enterId': user.enterId}
        else:
            abort(400, message='密码错误')


class IndexResource(Resource):
    decorators = [auth.login_required]

    def get(self):
        return {
            'code': 1,
            'message': 'success',
            'data':
                {
                    "34": "1, 6*, 80*, 96*, 88.89*",
                    "80": "1,42*,15*,8*",
                    "60": "1, %s,%s,%s" %
                          (g.user.totalOrderCount, g.user.totalDischargeReportCount, g.user.totalFactorReportCount),
                    "70": "1,1452*,785*,452*,15*,23*,1*",
                    "50": "1,%s,0*,%s" % (g.user.rainEnterCount, g.user.rainDischargeCount),
                    "40": "1,%s,%s,257*,%s,%s,%s,%s,%s,0*" %
                          (g.user.totalEnterCount, g.user.importantEnterCount, g.user.waterEnterCount,
                           g.user.airEnterCount, g.user.waterAirEnterCount, g.user.waterDischargeCount,
                           g.user.airDischargeCount),
                    "30": "1, 16*, 93.75*, 92.75*, 100*",
                    "20": "1,41*, 28*, 30*",
                    "31": "1, 10*, 100*, 100*, 88.89*",
                    "10": "1,南昌市*,2019年08月10日 09时*,67*,良*,PM2.5 SO2*,80*,72*,12*,22*,20*,0.32*",
                    "21": "1, 91.4*, 96.19*, 202*"
                }
        }


api.add_resource(AdminUserResource, '/admin/users/<int:id>', '/admin/users/<string:user_name>')
api.add_resource(AdminUserCollectionResource, '/admin/users')
api.add_resource(AdminTokenResource, '/admin/token')
api.add_resource(EnterTokenResource, '/enter/token')
api.add_resource(IndexResource, '/index')
