#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 15:44

from flask import Flask

from app import model
from app.api import api_blueprint

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# 配置数据库连接
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8'
app.config['SQLALCHEMY_BINDS'] = {
    'enterprise_archives': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_archives?charset=utf8',
    'enterprise_home': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/enterprise_home?charset=utf8',
    'pollution_report': 'mssql+pymssql://admin:jxhb#2019@182.106.189.190:1433/pollution_report?charset=utf8'
}
# 生成token用的密钥
app.config['SECRET_KEY'] = 'taoyimin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 接口返回中文，而不是Unicode编码
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
# APP上报时data source的默认值
# app.config['DATA_SOURCE'] = 'wryapp'
# 设置文件保存的根目录
app.config['UPLOAD_ROOT_DIRECTORY'] = 'D:/pollution_source/files'
# 设置文件保存的子目录
app.config['UPLOAD_SUB_DIRECTORY'] = 'wryapp'
# 排口异常申报附件的file model
app.config['DISCHARGE_REPORT_FILE_MODEL'] = 'dischargeReport'
# 排口异常申报附件的file type
app.config['DISCHARGE_REPORT_FILE_TYPE'] = 'enterStopApply'
# 因子异常申报附件的file model
app.config['FACTOR_REPORT_FILE_MODEL'] = 'factorReport'
# 因子异常申报附件的file type
app.config['FACTOR_REPORT_FILE_TYPE'] = 'enterAbnormalApply'
# 报警管理单处理流程附件的file model
app.config['ORDER_PROCESS_FILE_MODEL'] = 'process'
# 报警管理单处理流程附件的file type
app.config['ORDER_PROCESS_FILE_TYPE'] = 'provinceSupervise'
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
