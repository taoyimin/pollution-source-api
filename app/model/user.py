#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16
from flask import g
from flask_restful import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

import app
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.order import Order
from app.model.report import DischargeReport, FactorReport
from . import db, auth


class User(db.Model):
    # __bind_key__ = 'enterprise_home'

    __table_args__ = {'schema': 'enterprise_home.dbo'}
    __tablename__ = 't_user'

    userId = db.Column(db.Integer, name='id', primary_key=True, autoincrement=True)
    orgId = db.Column('orgId')
    userName = db.Column('userName', unique=True)
    realName = db.Column('realName')
    passWord = db.Column('plaintextPassword')
    globalLevel = db.Column('gobalLevel')
    userLevel = db.Column('user_level')
    isDelete = db.Column('status', default=0)
    districts = db.relationship('District')

    __mapper_args__ = {
        "order_by": userId
    }

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<User %r>' % self.userName

    def generate_auth_token(self, expiration=36000):
        """
        生成token,默认有效时间10小时
        :param expiration: 有效时间
        :return: token
        """
        # s = Serializer(Config.SECRET_KEY, expiration)
        s = Serializer(app.app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.userId}).decode('utf-8')

    @staticmethod
    @auth.verify_token
    def verify_token(token):
        """
        验证token
        :param token:
        :return:
        """
        if not token:
            return False
        g.user = None
        # s = Serializer(Config.SECRET_KEY)
        s = Serializer(app.app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except SignatureExpired:
            abort(401, message='token过期')
            return False
        except BadSignature:
            abort(401, message='token无效')
            return False
        if data:
            g.user = User.query.get_or_404(data['id'], description='token验证错误，id=%d的用户不存在' % data['id'])
            return True
        return False

    @property
    def totalEnterCount(self):
        return Enter.query.filter_by_user().count()

    @property
    def importantEnterCount(self):
        return Enter.query.filter_by_user().filter_by(attentionLevel='1').count()

    @property
    def waterEnterCount(self):
        return Enter.query.filter_by_user().filter_by(enterType='EnterType1').count()

    @property
    def airEnterCount(self):
        return Enter.query.filter_by_user().filter_by(enterType='EnterType2').count()

    @property
    def waterAirEnterCount(self):
        return Enter.query.filter_by_user().filter_by(enterType='EnterType1,EnterType2').count()

    @property
    def rainEnterCount(self):
        return Enter.query.filter_by_user().filter_by(enterType='EnterType3').count()

    @property
    def waterDischargeCount(self):
        return Discharge.query.filter_by_user().filter_by(dischargeType='outletType2').count()

    @property
    def airDischargeCount(self):
        return Discharge.query.filter_by_user().filter_by(dischargeType='outletType3').count()

    @property
    def rainDischargeCount(self):
        return Discharge.query.filter_by_user().filter_by(dischargeType='outletType1').count()

    @property
    def dealOrderCount(self):
        return Order.query.filter_by_user().filter_by_state('2').count()

    # @property
    # def noPassOrderCount(self):
    #     return Order.query.filter_by_user().filter_by_state('4').count()
    #
    # @property
    # def completeOrderCount(self):
    #     return Order.query.filter_by_user().filter_by_state('5').count()
    #
    # @property
    # def totalOrderCount(self):
    #     return Order.query.filter_by_user().count()

    @property
    def dealDischargeReportCount(self):
        return DischargeReport.query.filter_by_user().filter_by(state='0').count()

    @property
    def dealFactorReportCount(self):
        return FactorReport.query.filter_by_user().filter_by(state='0').count()

    # def get_district_criterion(self):
    #     """
    #     获取用户管辖区域企业的过滤条件
    #     :return:
    #     """
    #     district_code_list = map(lambda d: d.districtCode, self.districts)
    #     if self.globalLevel == 'province':
    #         if self.userLevel == '1':
    #             return Enter.cityCode.in_(district_code_list)
    #         if self.userLevel == '2':
    #             return Enter.areaCode.in_(district_code_list)
    #         if self.userLevel == '3':
    #             return Enter.countyCode.in_(district_code_list)
    #     if self.globalLevel == 'city' or 'county':
    #         return Enter.areaCode.in_(district_code_list)
    #     if self.globalLevel == 'industrialPark':
    #         return Enter.countyCode.in_(district_code_list)
