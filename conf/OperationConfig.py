import configparser
import sys
import traceback

from common.recordlog import logs
from conf import setting


class OperationConfig:
    """封装读取*.ini配置文件模块"""

    def __init__(self, filepath=None):
        """
        初始化方法，用于创建配置文件解析器对象
        参数:
            filepath (str, optional): 配置文件的路径。如果未提供，则使用默认配置文件路径
        属性:
            __filepath (str): 配置文件的路径
            conf (configparser.ConfigParser): 配置文件解析器对象
            type (str): 报告类型，通过调用get_report_type方法获取
        """
        if filepath is None:
        # 如果未提供文件路径，则使用默认配置文件路径
            self.__filepath = setting.FILE_PATH['CONFIG']
        else:
        # 如果提供了文件路径，则使用提供的路径
            self.__filepath = filepath

        # 创建配置文件解析器对象
        self.conf = configparser.ConfigParser()
        try:
        # 尝试读取配置文件，使用UTF-8编码
            self.conf.read(self.__filepath, encoding='utf-8')
        except Exception as e:
        # 捕获并记录异常信息
            exc_type, exc_value, exc_obj = sys.exc_info()
            logs.error(str(traceback.print_exc(exc_obj)))

        # 获取报告类型
        self.type = self.get_report_type('type')

    def get_section_for_data(self, section, option):
        """
        从配置文件中获取指定section和option对应的值
        :param section: ini文件头部值，用于标识配置文件中的特定段落
        :param option:头部值下面的选项，用于标识段落中的具体配置项
        :return: 返回获取到的配置值，如果发生异常则返回空字符串
        """
        try:
        # 尝试从配置文件中获取指定section和option对应的值
            values = self.conf.get(section, option)
        # 返回获取到的值
            return values
        except Exception as e:
        # 发生异常时打印错误堆栈信息（注释部分为日志记录方式）
            logs.error(str(traceback.format_exc()))
        # 发生异常时返回空字符串
            return ''

    def get_report_type(self, option):
        return self.get_section_for_data('REPORT_TYPE', option)

    def get_section_mysql(self, option):
        return self.get_section_for_data('MYSQL', option)