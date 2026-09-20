import allure
import pytest

from base.apiutil import RequestBase
from common.readyaml import get_testcase_yaml


@allure.feature('用户管理模块（单接口）')
class TestUserManager:

    @allure.story("新增用户")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('testcase/Single Interface/addUser.yaml'))
    def test_add_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story("查询用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info, testcase', get_testcase_yaml('testcase/Single Interface/queryUser.yaml'))
    def test_query_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)