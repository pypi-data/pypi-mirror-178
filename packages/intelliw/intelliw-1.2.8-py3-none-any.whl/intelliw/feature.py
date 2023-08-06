'''
Author: Hexu
Date: 2022-07-25 10:36:04
LastEditors: Hexu
LastEditTime: 2022-09-09 13:51:51
FilePath: /iw-algo-fx/intelliw/feature.py
Description: 统一功能包入口
'''

from intelliw.interface.apijob import Application
from intelliw.core.linkserver import linkserver
from intelliw.utils.logger import _get_algorithm_logger as get_logger

try:
    from intelliw.utils.dataprocess.spark import Spark
except ImportError:
    pass
