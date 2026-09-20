import allure
import pytest
from common.readyaml import get_testcase_yaml
from base.apiutil import RequestBase
from common.recordlog import logs


@pytest.fixture(autouse=True)
def start_test_and_end():
    logs.info('-------------接口测试开始--------------')
    yield
    logs.info('-------------接口测试结束--------------')


@pytest.fixture(scope="session", autouse=True)
@allure.story("登录")
def system_login():
    try:
        api_info = get_testcase_yaml('./data/loginName.yaml')
        RequestBase().specification_yaml(api_info[0][0], api_info[0][1])
    except Exception as e:
        logs.error(f'登录接口出现异常，导致后续接口无法继续运行，请检查程序！，{e}')
        pass