#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 15:45
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth = HTTPTokenAuth(scheme='Bearer')


def init_app(app):
    db.init_app(app)
