import allure
import pytest

from base.apiutil import RequestBase
from common.generateId import m_id, c_id
from common.readyaml import get_testcase_yaml


@allure.feature(next(m_id) + '商品管理（单接口）')
class TestProductManager:

    @allure.story(next(c_id) + '获取商品列表')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info, testcase', get_testcase_yaml('testcase/Product Manager/getProductList.yaml'))
    def test_get_product_list(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + '获取商品详情')
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info, testcase', get_testcase_yaml('testcase/Product Manager/getProductDetail.yaml'))
    def test_get_product_detail(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)


    @allure.story(next(c_id) + '提交订单')
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info, testcase', get_testcase_yaml('testcase/Product Manager/commitOrder.yaml'))
    def test_get_commit_order(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)