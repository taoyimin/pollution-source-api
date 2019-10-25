#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/25 10:01
from . import db


class District(db.Model):
    __bind_key__ = 'enterprise_home'

    __tablename__ = 't_user_district'

    id = db.Column('id', primary_key=True)
    districtCode = db.Column('districtId')
    userId = db.Column('userId', db.ForeignKey('t_user.id'))

    def __repr__(self):
        return '<District %r>' % self.districtCode
