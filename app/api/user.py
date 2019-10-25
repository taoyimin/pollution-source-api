#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16
from flask_restful import reqparse, Resource, fields, marshal_with
from werkzeug.routing import ValidationError

from app.api import api
from app.model import db, auth
from app.model.user import User
from app.util.common import valid_username, valid_password, valid_email, metric


def username(username_str):
    if valid_username(username_str):
        return username_str
    else:
        raise ValidationError("账号不能小于6位，不能有空字符串")


def password(password_str):
    if valid_password(password_str):
        return password_str
    else:
        raise ValidationError("密码不能小于6位，不能有空字符串")


def email(email_str):
    if valid_email(email_str):
        return email_str
    else:
        raise ValidationError("输入的不是有效的邮箱！")


user_fields = {
    'userId': fields.Integer,
    'userName': fields.String,
    'realName': fields.String,
    'passWord': fields.String,
    'globalLevel': fields.String,
    'userLevel': fields.String,
    'districts': fields.String(attribute=lambda user: ','.join(user.get_district_code_list())),
}

user_collection_fields = {
    'total': fields.Integer,
    'items': fields.List(fields.Nested(user_fields)),
    'page': fields.Integer,
    'per_page': fields.Integer,
    'has_next': fields.Boolean
}

login_fields = {
    'message': fields.String,
    'token': fields.String,
    'user': fields.Nested(user_fields)
}


class UserResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=username, help='用户名验证错误')
        self.parser.add_argument('password', type=password, help='密码验证错误')
        self.parser.add_argument('email', type=email)
        self.parser.add_argument('nickname', type=str)
        super(UserResource, self).__init__()

    @metric
    @marshal_with(user_fields)
    def get(self, id=None, username=None):
        if id is not None:
            user = User.query.get(id)
        else:
            user = User.query.filter_by(username=username).first()
        return user

    @metric
    @marshal_with(user_fields)
    def put(self, id):
        args = self.parser.parse_args()
        user = User.query.get(id)
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user


class UserCollectionResource(Resource):

    @metric
    @marshal_with(user_collection_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()
        pagination = User.query.paginate(args['page'], args['per_page'], False)
        return {'total': pagination.total, 'page': pagination.page, 'per_page': pagination.per_page, 'has_next': pagination.has_next,
                'items': pagination.items}

    @metric
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=username, required=True)
        parser.add_argument('password', type=password, required=True)
        parser.add_argument('email', type=email)
        args = parser.parse_args()
        user = User()
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user


class UserLoginResource(Resource):
    @metric
    @marshal_with(login_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=username, required=True)
        parser.add_argument('passWord', type=password, required=True)
        args = parser.parse_args()
        user = User.query.filter_by(userName=args['userName']).first()
        if user is None:
            return {'message': '账号不存在'}, 400
        else:
            if user.passWord == args['passWord']:
                # print(user)
                token = user.generate_auth_token()
                # print(token)
                return {'message': '登录成功', 'token': token, 'user': user}, 200
            else:
                return {'message': '密码错误'}, 400


api.add_resource(UserResource, '/users/<int:id>', '/users/<string:username>')
api.add_resource(UserCollectionResource, '/users')
api.add_resource(UserLoginResource, '/login')
