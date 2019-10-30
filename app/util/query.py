#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/30 19:25
from flask_restful import abort
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import load_only


class EnterQuery(BaseQuery):
    """
    企业查询类
    """

    def filter_by_user(self, user):
        """
        根据传入的用户筛选出在管辖区域的企业
        :param user:
        :return:
        """
        from app.model.enter import Enter
        if user:
            district_code_list = map(lambda d: d.districtCode, user.districts)
            if user.globalLevel == 'province':
                if user.userLevel == '1':
                    return self.filter(Enter.cityCode.in_(district_code_list))
                if user.userLevel == '2':
                    return self.filter(Enter.areaCode.in_(district_code_list))
                if user.userLevel == '3':
                    return self.filter(Enter.countyCode.in_(district_code_list))
            if user.globalLevel == 'city' or 'county':
                return self.filter(Enter.areaCode.in_(district_code_list))
            if user.globalLevel == 'industrialPark':
                return self.filter(Enter.countyCode.in_(district_code_list))
        else:
            abort(400, message='根据用户过滤掉不在管辖区域的企业失败，因为用户信息为空')

    def filter_by_state(self, state):
        """
        根据传入的状态筛选企业
        :param state:
        :return:
        """
        if state == 'online':
            # TODO 把在线企业过滤出来
            return self
        else:
            return self


class MonitorQuery(BaseQuery):
    """
    监控点查询类
    """

    def filter_by_user(self, user):
        """
        根据传入的用户筛选监控点
        :param user:
        :return:
        """
        from app.model.enter import Enter
        from app.model.monitor import Monitor
        return self.filter(Monitor.enterId.in_(Enter.query.filter_by_user(user).options(load_only(Enter.enterId))))

    def filter_by_state(self, state):
        """
        根据传入的状态筛选监控点
        :param state:
        :return:
        """
        # TODO 根据状态筛选监控点
        return self


class OrderQuery(BaseQuery):
    """
    报警管理单查询类
    """

    def filter_by_user(self, user):
        """
        根据传入的用户筛选报警管理单
        :param user:
        :return:
        """
        from app.model.enter import Enter
        from app.model.order import Order
        return self.filter(Order.enterId.in_(Enter.query.filter_by_user(user).options(load_only(Enter.enterId))))

    def filter_by_state(self, state):
        """
        根据传入的状态筛选报警管理单
        :param state:
        :return:
        """
        # TODO 根据状态筛选报警管理单
        return self
