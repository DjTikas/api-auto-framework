import allure
import pytest

from base.apiutil_business import RequestBaseBusiness
from common.generateId import m_id, c_id
from common.readyaml import get_testcase_yaml


@allure.feature(next(m_id) + '用户管理模块（单接口）')
class TestBusinessScenario():

    @allure.story(next(c_id) + '业务场景测试')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("case_info", get_testcase_yaml('testcase/Business Interface/businessScenario.yaml'))
    def test_business_scenario(self, case_info):
        allure.dynamic.title(case_info['base_info']['api_name'])
        RequestBaseBusiness().specification_yaml(case_info)