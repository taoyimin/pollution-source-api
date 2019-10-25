#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16
from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from app.config import Config
from app.model.district import District
from app.model.enter import Enter

from . import db, auth


class AuthFailed(Exception):
    def __init__(self, msg):
        self.msg = msg


class User(db.Model):
    __bind_key__ = 'enterprise_home'

    __tablename__ = 't_user'

    userId = db.Column('id', primary_key=True)
    userName = db.Column('userName')
    realName = db.Column('realName')
    passWord = db.Column('plaintextPassword')
    globalLevel = db.Column('gobalLevel')
    userLevel = db.Column('user_level')
    districts = db.relationship('District')

    def __repr__(self):
        return '<User %r>' % self.userName

    def generate_auth_token(self, expiration=3600):
        """
        生成token,默认有效时间一小时
        :param expiration: 有效时间
        :return: token
        """
        s = Serializer(Config.SECRET_KEY, expiration)
        # return s.dumps({'username': self.username}).decode('utf-8')
        return s.dumps({'userId': self.userId, 'userName': self.userName, 'realName': self.realName,
                        'passWord': self.passWord, 'globalLevel': self.globalLevel,
                        'userLevel': self.userLevel, 'districts': ','.join(self.get_district_code_list())}).decode('utf-8')

    @staticmethod
    @auth.verify_token
    def verify_token(token):
        if not token:
            return False
        g.user = None
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
        except SignatureExpired:
            raise AuthFailed(msg='token过期')
        except BadSignature:
            raise AuthFailed(msg='token无效')
        if data:
            g.user = data
            return True
        return False

    def get_district_code_list(self):
        return map(lambda d: d.districtCode, self.districts)

    @staticmethod
    def get_district_criterion(user):
        if user['globalLevel'] == 'province':
            if user['userLevel'] == '1':
                return Enter.cityCode.in_(user['districts'].split(','))
                # return Enter.cityCode == user['districts']
            if user['userLevel'] == '2':
                return Enter.areaCode.in_(user['districts'].split(','))
                # return Enter.areaCode == user['districts']
            if user['userLevel'] == '3':
                return Enter.countyCode.in_(user['districts'].split(','))
                # return Enter.countyCode == user['districts']
        if user['globalLevel'] == 'city' or 'county':
            return Enter.areaCode.in_(user['districts'].split(','))
            # return Enter.areaCode == user['districts']
        if user['globalLevel'] == 'industrialPark':
            return Enter.countyCode.in_(user['districts'].split(','))
            # return Enter.countyCode == user['districts']
