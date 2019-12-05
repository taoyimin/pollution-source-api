#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/25 10:01
from app.model.user import AdminUser
from . import db


class District(db.Model):
    # __bind_key__ = 'enterprise_home'

    __table_args__ = {'schema': 'enterprise_home.dbo'}
    __tablename__ = 't_user_district'

    id = db.Column('id', primary_key=True, autoincrement=True)
    districtCode = db.Column('districtId')
    userId = db.Column('userId', db.ForeignKey(AdminUser.userId))

    __mapper_args__ = {
        "order_by": id
    }

    def __repr__(self):
        return '<District %r>' % self.districtCode
