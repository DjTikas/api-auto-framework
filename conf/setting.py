import logging
import os
import sys

# 根目录
DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

# log日志输出级别
LOG_LEVEL = logging.DEBUG  # 文件
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台


# 接口超时时间，单位/s
API_TIMEOUT = 60

# 是否发送钉钉消息
dd_msg = False

# 文件路径
FILE_PATH = {
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'YAML': os.path.join(DIR_BASE),
    # 'TEMP': os.path.join(DIR_BASE, 'report/temp'),
    # 'TMR': os.path.join(DIR_BASE, 'report/tmreport'),
    'EXTRACT': os.path.join(DIR_BASE, 'extract.yaml'),
    # 'XML': os.path.join(DIR_BASE, 'data/sql'),
    # 'RESULTXML': os.path.join(DIR_BASE, 'report'),
    # 'EXCEL': os.path.join(DIR_BASE, 'data', '测试数据.xls')
}