import pymysql

from common.recordlog import logs
from conf.OperationConfig import OperationConfig

conf = OperationConfig()

class ConnectMysql:

    def __init__(self):

        mysql_conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('username'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database'),
        }

        try:
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # cursor=pymysql.cursors.DictCursor,将数据库表字段显示，以key-value形式展示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到mysql---
            host：{host}
            port：{port}
            db：{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(f"except:{e}")

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True

    def query_all(self, sql):
        """查询结果，将结果转换为 value list"""
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()

            if not res:
                return None

            # keys = res[0].keys()
            values = []
            lst_format = []
            for item in res:
                values.append(list(item.values()))

            for val in values:
                # lst_format = [
                #     keys,
                #     val
                # ]
                lst_format.append(list(val))

            return lst_format

        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def execute_write(self, sql, params=None):
        """
        执行 INSERT / UPDATE / DELETE 写操作
        :param sql: 带占位符的sql，例: insert into t(name) values(%s)
        :param params: 参数元组，防止注入
        :return: bool True成功 / False失败
        """
        params = params or ()
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            logs.info(f"执行SQL成功：{sql}")
            return True
        except Exception as e:
            self.conn.rollback()
            logs.error(f"SQL执行失败，sql={sql}, err={str(e)}")
            return False
        finally:
            self.close()


if __name__ == '__main__':
    connect = ConnectMysql()
    res = connect.query_all('select * from customer_info')
    logs.info(f'数据库查询结果{res}')

    sql = 'insert into customer_info(CustomerName, Sex, Age) values(%s, %s, %s)'
    res = connect.execute_write(sql, ('小明', '男', '35'))
    logs.info(f'数据库添加结果{res}')

    res = connect.query_all("select * from customer_info where CustomerName='小明'")
    logs.info(f'数据库查询结果{res}')

    sql = "delete from customer_info where CustomerName=%s"
    res = connect.execute_write(sql, ('小明',))
    logs.info(f'数据库删除结果{res}')

    res = connect.query_all("select * from customer_info where CustomerName='小明'")
    logs.info(f'数据库查询结果{res}')
