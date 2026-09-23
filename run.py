import os
import shutil
import sys

import pytest

if __name__ == '__main__':
    pytest.main([ '-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])

    # 外部传入的所有参数交给pytest，不再写死参数
    # pytest.main(sys.argv[1:])
    shutil.copy('./environment.xml', './report/temp')

    # os.system(f'allure serve ./report/temp')