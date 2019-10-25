#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/4/28 17:16

import functools
import re
import time


def valid_username(username):
    # 账号不能小于6位，不能有空字符串
    if len(username) < 6 or ' ' in username:
        return False
    else:
        return True


def valid_password(password):
    # 密码不能小于6位，不能有空字符串
    if len(password) < 6 or ' ' in password:
        return False
    else:
        return True


def valid_email(email):
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return True
    else:
        return False


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


if __name__ == '__main__':
    valid_email(input('please input a email address:'))
