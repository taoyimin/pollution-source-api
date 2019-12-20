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


class BaseUser:
    """
    所有类型用户的父类
    继承验证token方法
    """

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
            if data['type'] == app.app.config['ADMIN_USER_TYPE']:
                # 环保用户
                g.type = data['type']
                g.user = AdminUser.query.get_or_404(data['id'], description='token验证错误，id=%d的环保用户不存在' % data['id'])
                return True
            elif data['type'] == app.app.config['ENTER_USER_TYPE']:
                # 企业用户
                g.type = data['type']
                g.user = EnterUser.query.get_or_404(data['id'], description='token验证错误，id=%d的企业用户不存在' % data['id'])
                return True
            else:
                abort(401, message='token验证错误，未知的用户类型！type=%d' % data['type'])
        return False


class AdminUser(db.Model, BaseUser):
    """
    环保用户实体类
    attributes:
        userId: 自增长主键
        orgId: 组织id
        userName: 用户名（不可重复）
        realName: 真实名称
        passWord: 明文密码
        globalLevel:
        userLevel: 用户级别 1：省 2：地市 3：区县 4：园区
        isDelete: 是否删除
        districts: 用户的管辖区域集合
    """
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
        return '<AdminUser %r>' % self.userId

    def generate_auth_token(self, expiration=36000):
        """
        生成token,默认有效时间10小时
        :param expiration: 有效时间
        :return: token
        """
        s = Serializer(app.app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.userId, 'type': app.app.config['ADMIN_USER_TYPE']}).decode('utf-8')

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

    # @property
    # def dealOrderCount(self):
    #     return Order.query.filter_by_user().filter_by_state('2').count()

    # @property
    # def noPassOrderCount(self):
    #     return Order.query.filter_by_user().filter_by_state('4').count()
    #
    # @property
    # def completeOrderCount(self):
    #     return Order.query.filter_by_user().filter_by_state('5').count()
    #
    @property
    def totalOrderCount(self):
        return Order.query.filter_by_user().count()

    @property
    def totalDischargeReportCount(self):
        return DischargeReport.query.filter_by_user().count()

    @property
    def totalFactorReportCount(self):
        return FactorReport.query.filter_by_user().count()


class EnterUser(db.Model, BaseUser):
    """
    企业用户实体类
    attributes:
        userId: 自增长主键
        enterId: 企业id
        userName: 用户名（不可重复）
        passWord: 明文密码
        isDelete: 是否删除
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_Enterprise_Account'

    userId = db.Column(db.Integer, name='id', primary_key=True, autoincrement=True)
    enterId = db.Column('enter_id')
    userName = db.Column('account_Name', unique=True)
    passWord = db.Column('password_text')
    isDelete = db.Column('is_deleted', default=0)

    __mapper_args__ = {
        "order_by": userId
    }

    def __repr__(self):
        return '<EnterUser %r>' % self.userId

    def generate_auth_token(self, expiration=36000):
        """
        生成token,默认有效时间10小时
        :param expiration: 有效时间
        :return: token
        """
        s = Serializer(app.app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.userId, 'type': app.app.config['ENTER_USER_TYPE']}).decode('utf-8')
