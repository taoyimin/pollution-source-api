#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 15:44

from flask import Flask

from app import model
from app.api import api_blueprint

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8'
app.config['SQLALCHEMY_BINDS'] = {
    'enterprise_archives': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8',
    'enterprise_home': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_home?charset=utf8',
    'pollution_report': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/pollution_report?charset=utf8'
}
app.config['SECRET_KEY'] = 'taoyimin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.register_blueprint(api_blueprint)
model.init_app(app)

# def create_app():
#     app = Flask(__name__)
#     app.config[
#         'SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8'
#     app.config['SQLALCHEMY_BINDS'] = {
#         'enterprise_archives': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8',
#         'enterprise_home': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_home?charset=utf8',
#         'pollution_report': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/pollution_report?charset=utf8'
#     }
#     app.config['SECRET_KEY'] = 'taoyimin'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.register_blueprint(api_blueprint)
#     model.init_app(app)
#     return app
