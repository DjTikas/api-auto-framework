# 接口自动化测试框架

基于 **Pytest + Requests + YAML 数据驱动 + Allure + Jenkins** 的接口自动化测试框架，支持接口关联、业务场景编排、多维度断言、数据库校验，并集成钉钉通知与邮件报告。

## 项目结构

```
my_api_test/
├── run.py                    # 统一入口
├── conftest.py               # 全局 fixture（登录前置、清理、结果通知）
├── pytest.ini                # pytest 配置
├── environment.xml            # Allure 报告环境信息
├── conf/                     # 配置层
│   ├── config.ini            #   环境/数据库/报告类型配置
│   ├── setting.py            #   全局路径与开关
│   └── OperationConfig.py    #   配置读取（支持环境变量覆盖）
├── common/                  # 公共组件
│   ├── sendrequest.py        #   请求封装（Session + Cookie 持久化）
│   ├── readyaml.py           #   YAML 用例读写 + 变量池
│   ├── assertions.py         #   五种断言（contains/eq/ne/any/db）
│   ├── debugtalk.py          #   热加载函数库
│   ├── connection.py         #   MySQL 操作
│   ├── recordlog.py          #   日志（滚动备份 + 自动清理）
│   └── dingRobot.py          #   钉钉机器人通知
├── base/                     # 引擎层
│   ├── apiutil.py            #   单接口执行引擎
│   ├── apiutil_business.py   #   业务链路执行引擎
│   └── generateId.py         #   Allure 模块/用例编号生成器
├── data/                     # 全局测试数据
├── testcase/                 # 测试用例（YAML + Python）
│   ├── Single Interface/     #   单接口测试
│   ├── Business Interface/   #   业务场景测试
│   └── Product Manager/      #   商品模块测试
└── report/                   # 测试报告
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

敏感信息通过环境变量注入，不在代码中硬编码：

```bash
# 钉钉机器人通知（可选）
export DINGTALK_ACCESS_TOKEN="你的access_token"
export DINGTALK_SECRET="SEC你的加签密钥"

# MySQL 密码（使用数据库断言时需要）
export MYSQL_PASSWORD="你的数据库密码"
```

### 3. 修改配置

编辑 `conf/config.ini`，设置被测服务地址：

```ini
[api_envi]
host = http://127.0.0.1:8787
```

### 4. 运行测试

```bash
# 运行全部用例
python run.py

# 指定模块运行
python run.py -vs testcase/Single\ Interface/

# 冒烟回归（通过 marker 筛选）
python run.py -m smoke
```

### 5. 查看报告

```bash
allure serve ./report/temp
```

## 编写测试用例

用例以 YAML 文件维护，无需修改框架代码。一个 YAML 文件包含 `base_info`（接口信息）和 `test_case`（多组测试数据）：

```yaml
- base_info:
    api_name: 新增用户
    url: /dar/user/addUser
    method: POST
    headers:
      Content-Type: application/x-www-form-urlencoded;charset=UTF-8
  test_case:
    - case_name: 正常新增用户
      data:
        username: testuser
        password: 123456
        token: ${get_extract_data(token)}   # 引用登录提取的 token
      validation:
        - eq: { status_code: 200 }
        - contains: { msg: '新增成功' }
      extract:
        user_id: $.user_id                  # 提取返回值供下游接口使用
```

### 核心特性

| 特性 | 语法 | 说明 |
| --- | --- | --- |
| 变量引用 | `${get_extract_data(token)}` | 引用 extract.yaml 变量池中的值 |
| 动态参数 | `${timestamp()}` | 通过反射调用 debugtalk.py 中的函数 |
| 变量提取 | `extract: { key: $.jsonpath }` | jsonpath 或正则提取响应值 |
| 批量提取 | `extract_list: { key: $.list[*].id }` | 提取列表数据 |
| 断言 | `eq` / `contains` / `ne` / `any` / `db` | 五种断言模式，可组合使用 |

## Jenkins 集成

1. Jenkins 安装 **Allure Plugin** 和 **JUnit Plugin**
2. 创建 Pipeline 项目，构建命令：
   ```bash
   python run.py
   ```
3. 构建后操作：
   - Allure 报告：指向 `report/temp`
   - 邮件通知：解析 `report/results.xml`
   - 钉钉通知：自动推送测试摘要（需配置环境变量）

## 技术栈

- **Python 3.8+** / Pytest / Requests
- **YAML** 数据驱动（PyYAML）
- **Allure** 测试报告
- **PyMySQL** 数据库断言
- **jsonpath** 响应提取
- **Jenkins** 持续集成
