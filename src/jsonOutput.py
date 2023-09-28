# json输出示例
# 参考:
#       https://blog.csdn.net/weixin_42375356/article/details/110440666

import json

import util


def stringfy_list_or_tuple(data):
    openSymbol = None
    closeSymbol = None
    emptySymbol = None
    if isinstance(data, list):
        openSymbol = "["
        closeSymbol = "]"
        emptySymbol = "[]"

    else:
        openSymbol = "("
        closeSymbol = ")"
        emptySymbol = "()"

    dataLen = len(data)
    if dataLen == 0:
        return emptySymbol
    elements = []
    elements.append(openSymbol)
    count = 1
    for element in data:
        elementStr = stringfy(element)
        elements.append(elementStr)
        if count < dataLen:
            elements.append(", ")
        count += 1
    elements.append(closeSymbol)
    return "".join(elements)


def stringfy_set(setData):
    setDataLen = len(setData)
    if setDataLen == 0:
        return "{,}"
    elements = []
    elements.append("{")
    count = 1
    for element in setData:
        elementStr = stringfy(element)
        elements.append(elementStr)
        if count < setDataLen:
            elements.append(", ")
        count += 1
    elements.append("}")
    return "".join(elements)


def stringfy_dict(dictData):
    dictLen = len(dictData.keys())
    if dictLen == 0:
        return "{}"
    elements = []
    elements.append("{")
    count = 1
    for key, value in dictData.items():
        valueStr = stringfy(value)
        if count < dictLen:
            elements.append('"{0}":{1}, '.format(key, valueStr))
        else:
            elements.append('"{0}":{1}'.format(key, valueStr))
        count += 1
    elements.append("}")
    return "".join(elements)


def stringfy(obj):
    """
    将对象转换为字符串
    """
    if isinstance(obj, (list, tuple)):
        return stringfy_list_or_tuple(obj)
    elif isinstance(obj, set):
        return stringfy_set(obj)
    elif isinstance(obj, dict):
        return stringfy_dict(obj)
    elif isinstance(obj, str):
        return '"{0}"'.format(str(obj))

    return str(obj)


def test_json_output():
    # 设置
    # 1|2|3|4
    run = 4
    use_utf8_encoding = True

    jsonDict = {
        "remote-pc": {"server": {"ip": "192.168.0.102", "port": "10086"}},
        "server": {"maxConnect": "2"},
        "duration": "5 * 60 * 1000",
        "username": "user",
        "password": "246810",
    }

    jsonDict_2 = {
        "remote-pc": {"server": {"ip": "192.168.0.102", "port": "10086"}},
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
    }

    jsonString = ""
    if run == 1:
        jsonString = json.dumps(jsonDict)
    elif run == 2:
        jsonString = json.dumps(
            jsonDict,
            # 缩进显示
            indent=4,
            # 排序 a-z
            sort_keys=True,
            # 防止中文乱码
            ensure_ascii=False,
            # #去掉‘，’和‘：’的前后空格。打印以方便阅读时不建议使用
            # separators=(',', ':')
        )
    elif run == 3:
        jsonString = json.dumps(jsonDict_2)
    elif run == 4:
        jsonString = json.dumps(
            jsonDict_2,
            # 缩进显示
            indent=4,
            # 排序 a-z
            sort_keys=True,
            # 防止中文乱码
            ensure_ascii=False,
            # #去掉‘，’和‘：’的前后空格。打印以方便阅读时不建议使用
            # separators=(',', ':')
        )

    if jsonString:
        print("jsonString:")
        print(jsonString)
        print()
        # 如果不指定编码格式, 默认ANSI
        fo = None
        if use_utf8_encoding:
            fo = open("../out/json_out", "w", encoding="utf-8")
        else:
            fo = open("../out/json_out", "w")
        fo.write(jsonString)
        fo.close()
        print("jsonString write complete")


def test_data_of_nest_tuple_jsonStringfy_and_write():
    """
    测试嵌套元组的Python 数据 JSON字符化并写入到本地文件中

    测试结果:
    ```
    嵌套的元组在进行JSON序列化后转为列表输出
    ```
    """
    dict_1 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "二", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
    }
    util.writeJson(
        "../out/jsonOuput/test_data_of_nest_tuple_jsonStringfy_and_out/dict_1.json",
        dict_1,
        indent=4,
    )

    print("write complete")


def test_stringfy():
    """
    测试函数 `stringfy`
    """
    dict_1 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "二", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
        "abc": ("三", [1, {"二", 3}, (4, (5, 6)), False]),
    }
    content = stringfy(dict_1)
    util.writeContent("../out/jsonOuput/test_stringfy/content.data", content)
    print("write complete")


# run
# test_json_output()
# test_data_of_nest_tuple_jsonStringfy_and_write()
# test_stringfy()
