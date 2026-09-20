import os

import pytest

if __name__ == '__main__':
    pytest.main([ '-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])
    os.system(f'allure serve ./report/temp')