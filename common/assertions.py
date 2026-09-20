import operator

import allure
import jsonpath

from common.recordlog import logs


class Assertions:
    """"
    接口断言模式，支持
    1）响应文本字符串包含模式断言
    2）响应结果相等断言
    3）响应结果不相等断言
    4）响应结果任意值断言
    5）数据库断言

    """

    def contains_assert(self, expected, response, status_code):
        """
        字符串包含断言模式，断言预期结果的字符串是否包含在接口的响应信息中
        :param value: 预期结果，yaml文件的预期结果值
        :param response: 接口实际响应结果
        :param status_code: 响应状态码
        :return: 返回结果的状态标识
        """
        # 断言状态标识，0成功，其他失败
        flag = 0
        for assert_key, assert_value in expected.items():
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, assert_value))
                else:
                    logs.info(f'包含断言成功：状态码={status_code}')
            else:
                resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    if assert_value in resp_list:
                        logs.info("字符串包含断言成功：预期结果【%s】,实际结果【%s】" % (assert_value, resp_list))
                    else:
                        flag = flag + 1
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (assert_value, resp_list))
        return flag

    def equal_assert(self, expected, response, status_code):
        """
        相等断言模式，断言预期结果是否等于接口响应结果
        :param expected: 预期结果，yaml文件的预期结果值
        :param response: 接口实际响应结果
        :return: 返回结果的状态标识
        """
        flag = 0
        # 类型校验
        if isinstance(response, dict) and isinstance(expected, dict):
            for exp_key, exp_val in expected.items():
                if exp_key == 'status_code':
                    if exp_val != status_code:
                        flag += 1
                        allure.attach(f"预期结果：{exp_val}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, exp_val))
                    else:
                        logs.info(f'包含断言成功：状态码={status_code}')
                else:
                    # 预期key在实际响应不存在
                    if exp_key not in response:
                        flag += 1
                        logs.error(f"相等断言失败：实际响应不存在key【{exp_key}】，response：{response}")
                        allure.attach(f"预期key【{exp_key}】不存在", "相等断言结果：失败", allure.attachment_type.TEXT)
                        continue
                    act_val = response[exp_key]
                    eq_assert = operator.eq(exp_val, act_val)
                    if eq_assert:
                        logs.info(f"相等断言成功：key={exp_key},预期={exp_val},实际={act_val}")
                        allure.attach(f"key={exp_key}\n预期结果：{exp_val}\n实际结果：{act_val}",
                                      '相等断言结果：成功', allure.attachment_type.TEXT)
                    else:
                        flag += 1
                        logs.error(f"相等断言失败：key={exp_key}，预期={exp_val}，实际={act_val}")
                        allure.attach(f"key={exp_key}\n预期结果：{exp_val}\n实际结果：{act_val}",
                                      '相等断言结果：失败', allure.attachment_type.TEXT)
        return flag


    def assert_result(self, expected, response, status_code):
        """
        断言，通过断言all_flag标记，all_flag==0表示测试通过，否则为失败
        :param expected: 预期结果
        :param response: 实际响应结果
        :param status_code: 响应code码
        :return:
        """
        all_flag = 0
        try:
            logs.info("yaml文件预期结果：%s" % expected)
            for ep in expected:
                for k, v in ep.items():
                    if k == 'contains':
                        flag = self.contains_assert(v, response, status_code)
                        all_flag = all_flag + flag
                    elif k == 'eq':
                        flag = self.equal_assert(v, response, status_code)
                        all_flag = all_flag + flag
                    else:
                        logs.error("不支持此种断言方式")
        except Exception as exceptions:
            logs.error('接口断言异常，请检查yaml预期结果值是否正确填写!')
            raise exceptions

        if all_flag == 0:
            logs.info("测试成功")
            assert True
        else:
            logs.error("测试失败")
            assert False