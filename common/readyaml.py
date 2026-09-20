import os
import traceback

import yaml

from common.recordlog import logs
from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    """读取测试用例"""
    testcase_list = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if len(data) <= 1:
                yaml_data = data[0]
                base_info = yaml_data.get('base_info')
                for ts in yaml_data.get('test_case'):
                    param = [base_info, ts]
                    testcase_list.append(param)
                return testcase_list
            else:
                return data
    except UnicodeDecodeError:
        logs.error(f"[{file}]文件编码格式错误，--尝试使用utf-8编码解码YAML文件时发生了错误，请确保你的yaml文件是UTF-8格式！")
    except FileNotFoundError:
        logs.error(f'[{file}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f'获取【{file}】文件数据时出现未知错误: {str(e)}')


class ReadYamlData:
    """读写接口的YAML格式测试数据"""

    def write_yaml_data(self, value):
        """
        写入数据需为dict，allow_unicode=True表示写入中文，sort_keys按顺序写入
        写入YAML文件数据,主要用于接口关联
        """
        file_path = FILE_PATH['EXTRACT']
        dir_path = os.path.dirname(file_path)
        # 1. 判断目录是否存在，不存在创建目录
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 2. 校验入参
        if not isinstance(value, dict):
            logs.info('写入[extract.yaml]的数据必须为dict格式')
            return False

        # 3. 先读取原有数据，不存在则空字典
        old_data = {}
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    old_data = yaml.safe_load(f) or {}
            except Exception as e:
                logs.error(f"读取yaml失败：{traceback.format_exc()}")
                return False

        # 4. 更新字典，合并新老数据（不是覆盖整个文件，也不是追加）
        old_data.update(value)

        # 5. 写回文件
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(old_data, f, allow_unicode=True, sort_keys=False)
            # logs.info(f"写入yaml成功：{value}")
            return True
        except Exception:
            logs.error(f"写入yaml失败：{traceback.format_exc()}")
            return False

    def clear_yaml_data(self):
        """
        清空extract.yaml文件数据
        :param filename: yaml文件名
        :return:
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()

    def get_extract_yaml(self, node_name, second_node_name=None):
        """
        用于读取接口提取的变量值
        :param node_name:
        :return:
        """
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            logs.error('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            logs.info('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            logs.error(f"【extract.yaml】没有找到：{node_name},--%s" % e)