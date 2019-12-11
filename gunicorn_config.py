#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/12/11 9:17
import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

sys.path.insert(0, path_of_current_dir)

worker_class = 'sync'
workers = multiprocessing.cpu_count() * 2 + 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

# 开启后台运行
daemon = True
reload = True
debug = False

bind = "%s:%s" % ("0.0.0.0", 5000)
pidfile = '%s/run/gunicorn.pid' % (path_of_current_dir)
errorlog = '%s/logs/error.log' % (path_of_current_dir)
accesslog = '%s/logs/access.log' % (path_of_current_dir)
