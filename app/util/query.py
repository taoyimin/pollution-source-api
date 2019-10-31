#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/30 19:25
from flask import g
from flask_restful import abort
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import load_only

from app.util.common import filter_none


class CommonQuery(BaseQuery):
    """
    通用查询类
    """

    def filter_by_args(self, args):
        """
        根据传入的字典过滤数据，忽略value为空的参数
        :param args:
        :return:
        """
        return self.filter_by(**filter_none(args))


class EnterQuery(CommonQuery):
    """
    企业查询类
    """

    def get_or_abort(self, ident):
        """
        根据传入id查询企业
        :param ident:
        :return:
        """
        from app.model.enter import Enter
        enter = self.get_or_404(ident, description='id=%s的企业不存在' % ident)
        return enter if Enter.query.filter_by_user().filter_by(enterId=enter.enterId).one_or_none() \
            else abort(400, message='您没有权限访问id=%s的企业' % ident)

    def filter_by_user(self):
        """
        根据传入的用户筛选出在管辖区域的企业
        :param user:
        :return:
        """
        from app.model.enter import Enter
        if g.user:
            district_code_list = map(lambda d: d.districtCode, g.user.districts)
            if g.user.globalLevel == 'province':
                if g.user.userLevel == '1':
                    return self.filter(Enter.cityCode.in_(district_code_list))
                if g.user.userLevel == '2':
                    return self.filter(Enter.areaCode.in_(district_code_list))
                if g.user.userLevel == '3':
                    return self.filter(Enter.countyCode.in_(district_code_list))
            if g.user.globalLevel == 'city' or 'county':
                return self.filter(Enter.areaCode.in_(district_code_list))
            if g.user.globalLevel == 'industrialPark':
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


class DischargeQuery(CommonQuery):
    """
    排口查询类
    """

    def get_or_abort(self, ident):
        """
        根据传入id查询排口
        :param ident:
        :return:
        """
        from app.model.enter import Enter
        discharge = self.get_or_404(ident, description='id=%s的排口不存在' % ident)
        return discharge if Enter.query.filter_by_user().filter_by(enterId=discharge.enterId).one_or_none() \
            else abort(400, message='您没有权限访问id=%s的排口' % ident)

    def filter_by_user(self):
        """
        根据传入的用户筛选排口
        :return:
        """
        from app.model.enter import Enter
        from app.model.discharge import Discharge
        return self.filter(Discharge.enterId.in_(Enter.query.filter_by_user().options(load_only(Enter.enterId))))

    def filter_by_state(self, state):
        """
        根据传入的状态筛选排口
        :param state:
        :return:
        """
        # TODO 根据状态筛选排口
        return self


class MonitorQuery(CommonQuery):
    """
    监控点查询类
    """

    def get_or_abort(self, ident):
        """
        根据传入id查询监控点
        :param ident:
        :return:
        """
        from app.model.enter import Enter
        monitor = self.get_or_404(ident, description='id=%s的监控点不存在' % ident)
        return monitor if Enter.query.filter_by_user().filter_by(enterId=monitor.enterId).one_or_none() \
            else abort(400, message='您没有权限访问id=%s的监控点' % ident)

    def filter_by_user(self):
        """
        根据传入的用户筛选监控点
        :return:
        """
        from app.model.enter import Enter
        from app.model.monitor import Monitor
        return self.filter(Monitor.enterId.in_(Enter.query.filter_by_user().options(load_only(Enter.enterId))))

    def filter_by_state(self, state):
        """
        根据传入的状态筛选监控点
        :param state:
        :return:
        """
        # TODO 根据状态筛选监控点
        return self


class OrderQuery(CommonQuery):
    """
    报警管理单查询类
    """

    def get_or_abort(self, ident):
        """
        根据传入id查询报警管理单
        :param ident:
        :return:
        """
        from app.model.enter import Enter
        order = self.get_or_404(ident, description='id=%s的报警管理单不存在' % ident)
        return order if Enter.query.filter_by_user().filter_by(enterId=order.enterId).one_or_none() \
            else abort(400, message='您没有权限访问id=%s的报警管理单' % ident)

    def filter_by_user(self):
        """
        根据传入的用户筛选报警管理单
        :return:
        """
        from app.model.enter import Enter
        from app.model.order import Order
        return self.filter(Order.enterId.in_(Enter.query.filter_by_user().options(load_only(Enter.enterId))))

    def filter_by_state(self, state):
        """
        根据传入的状态筛选报警管理单
        :param state:
        :return:
        """
        # TODO 根据状态筛选报警管理单
        return self

    def filter_by_parent(self):
        pass
