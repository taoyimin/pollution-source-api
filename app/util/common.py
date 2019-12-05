#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16
import datetime
import functools
import os
import time
import uuid

from sqlalchemy import inspect, event
from sqlalchemy.orm import Query, load_only
from werkzeug.routing import ValidationError

import app


@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    """
    查询前默认把数据库无用的数据过滤掉
    :param query:
    :return:
    """
    from app.model.enter import Enter
    from app.model.discharge import Discharge
    from app.model.monitor import Monitor
    from app.model.order import Order
    from app.model.report import LongStopReport
    from app.model.report import DischargeReport
    from app.model.report import FactorReport
    from app.model.attachment import Attachment
    from app.model.dictionary import Dictionary
    from app.model.license import License
    from app.model.license import LicenseFactor
    from app.model.user import AdminUser
    from app.model.user import EnterUser
    for ent in query.column_descriptions:
        entity = ent['entity']
        if entity is None:
            continue
        insp = inspect(ent['entity'])
        mapper = getattr(insp, 'mapper', None)
        if mapper and issubclass(mapper.class_,
                                 (AdminUser, Enter, EnterUser, Attachment, Dictionary, License, LicenseFactor)):
            # 把isDelete=0的数据保留
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0)
        elif mapper and issubclass(mapper.class_, (Discharge,)):
            # 把isDelete=0的保留，没有对应enterId的Discharge过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0) \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId))))
        elif mapper and issubclass(mapper.class_, (Monitor,)):
            # 把isDelete=0的保留，没有对应enterId、dischargeId的Monitor过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0) \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId)))) \
                .filter(ent['entity'].dischargeId.in_(Discharge.query.options(load_only(Discharge.dischargeId))))
        elif mapper and issubclass(mapper.class_, (Order,)):
            # 把没有对应enterId和monitorId的Order过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId)))) \
                .filter(ent['entity'].monitorId.in_(Monitor.query.options(load_only(Monitor.monitorId))))
        elif mapper and issubclass(mapper.class_, (DischargeReport,)):
            # 把isDelete=0，dataType=S，dischargeMonitorType=1的保留，没有对应enterId,dischargeId,monitorId的Report过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0, ent['entity'].dataType == 'S') \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId)))) \
                .filter(ent['entity'].dischargeId.in_(Discharge.query.options(load_only(Discharge.dischargeId)))) \
                .filter(ent['entity'].monitorId.in_(Monitor.query.options(load_only(Monitor.monitorId)))) \
                .join(Discharge).filter_by(dischargeMonitorType='1')
        elif mapper and issubclass(mapper.class_, (FactorReport,)):
            # 把isDelete=0，dataType=A的保留，没有对应enterId,dischargeId,monitorId的Report过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0, ent['entity'].dataType == 'A') \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId)))) \
                .filter(ent['entity'].dischargeId.in_(Discharge.query.options(load_only(Discharge.dischargeId)))) \
                .filter(ent['entity'].monitorId.in_(Monitor.query.options(load_only(Monitor.monitorId))))
        elif mapper and issubclass(mapper.class_, (LongStopReport,)):
            # 把isDelete=0，dataType=L的保留，没有对应enterId的Report过滤掉
            query = query.enable_assertions(False) \
                .filter(ent['entity'].isDelete == 0, ent['entity'].dataType == 'L') \
                .filter(ent['entity'].enterId.in_(Enter.query.options(load_only(Enter.enterId))))
    return query


def valid_user_name(user_name_str):
    if len(user_name_str) < 6 or ' ' in user_name_str:
        raise ValidationError("账号不能小于6位，不能有空字符串")
    else:
        return user_name_str


def valid_pass_word(pass_word_str):
    if len(pass_word_str) < 6 or ' ' in pass_word_str:
        raise ValidationError("密码不能小于6位，不能有空字符串")
    else:
        return pass_word_str


def valid_not_empty(string):
    if string:
        return string
    else:
        raise ValidationError("参数不能为空值")


# def valid_email(email):
#     if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
#         return True
#     else:
#         return False


def metric(func):
    """
    装饰器：打印函数执行的时间
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('%s() execute in %s ms' % (func.__name__, (end - start) * 1000))
        return result

    return wrapper


def filter_none(data):
    """
    过滤字典中的空值并返回
    :param data: 待过滤的字典
    :return:
    """
    for k in list(data.keys()):
        if not data[k]:
            del data[k]
    return data


def save_file(file):
    """
    保存文件并返回生成attachment实例的args
    :param file:
    :return:
    """
    # url前缀，保存到数据库需要使用
    url_prefix = app.app.config['UPLOAD_SUB_DIRECTORY'] + '/' + app.app.config[
        'DISCHARGE_REPORT_FILE_TYPE'] + '/' + str(datetime.datetime.now().year) + str(
        datetime.datetime.now().month)
    # 存在本地的真实文件名
    local_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    # 文件存放目录
    save_directory = os.path.join(app.app.config['UPLOAD_ROOT_DIRECTORY'], url_prefix)
    if not os.path.exists(save_directory):
        # 如果文件夹不存在则创建
        os.makedirs(save_directory)
    # 文件的完整路径
    full_path = os.path.join(save_directory, local_filename)
    file.save(full_path)
    return {'fileName': file.filename, 'url': url_prefix + '/' + local_filename,
            'size': os.stat(full_path).st_size}
