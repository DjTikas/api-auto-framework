import json

import allure
import requests

from common.readyaml import ReadYamlData
from common.recordlog import logs
from conf import setting


class SendRequest:
    """发送接口请求"""

    def __init__(self):
        self.read = ReadYamlData()

    def send_request(self, **kwargs):
        """底层方法"""
        session = requests.session()
        cookies = {}
        result = session.request(**kwargs)
        set_cookies = requests.utils.dict_from_cookiejar(result.cookies)
        # cookies写入yaml，持久化
        if set_cookies:
            cookies['Cookies'] = set_cookies
            self.read.write_yaml_data(cookies)
        return result

    def run_main(self, name, url, case_name, headers, method, cookies=None, file=None, **kwargs):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param headers:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param file: 上传文件接口
        :param kwargs: 请求参数，根据yaml文件的参数类型
        :return:
        """

        try:
            # 收集报告日志
            logs.info('接口名称：%s' % name)
            logs.info('请求地址：%s' % url)
            logs.info('请求方式：%s' % method)
            logs.info('测试用例名称：%s' % case_name)
            logs.info('请求头：%s' % headers)
            logs.info('Cookies：%s' % cookies)
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if "data" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        # time.sleep(0.5)
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = self.send_request(method=method,
                                     url=url,
                                     headers=headers,
                                     cookies=cookies,
                                     files=file,
                                     timeout=setting.API_TIMEOUT,
                                     verify=False,
                                     **kwargs)
        return response