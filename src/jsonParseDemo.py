# json解析示例

import json
import os
import traceback

import util


def parseConsoleInputJsonDataAndSave():
    """
    解析控制台输入的json数据并保存到本地
    """
    jsonString = input("please input JSONString: ")
    jsonDict = json.loads(jsonString)
    for key in jsonDict:
        print("key: %s, value: %s" % (key, jsonDict[key]))

    with open("../out/jsonDict.json", "w") as f:
        json.dump(jsonDict, f)


def parse_json_data(jsonFilePath):
    """
    从文件中解析出JSON数据

    返回:
        是否成功解析, 解析后的JSON数据
    """
    if not util.isFile(jsonFilePath):
        return None
    jsonString = util.readContent(jsonFilePath)

    jsonData = None
    try:
        jsonData = json.loads(jsonString)
    except Exception as e:
        print("json.load err")
        traceback.print_exc()
        return False, None

    return True, jsonData


def test_parse_json_data():
    """
    测试函数 `parse_json_data`
    """
    json_root_dir = "../in/json"
    for subFileName in os.listdir(json_root_dir):
        subFilePath = json_root_dir + "/" + subFileName
        success, json_data = parse_json_data(subFilePath)
        print("subFileName: ", subFileName)
        print("parse success:", success)
        if success:
            print("json_data type: ", type(json_data))
            print("json_data: ", json_data)
        print()

    print("test complete")


def test_create_set_data_compare():
    """
    测试创建set集合数据并比较
    """
    set_1 = set()
    set_2 = {"apple", "orange", 1, 2, 3}
    set_3 = set([4, 5, 6, 7])
    # set_4 = {"apple", 1, set_3}
    # set_5 = {1, "apple", set_3, set_4}
    print("set_1: ", set_1)
    print("set_2: ", set_2)
    print("set_3: ", set_3)
    # print("set_4: ", set_4)
    # print("set_5: ", set_5)
    print()

    # print("set_4 == set_5: ", (set_4 == set_5))
    # print()

    # list_4 = ["apple", 1, set_3, set_4]
    list_4 = ["apple", 1, set_3]
    print("list_4: ", list_4)
    print()

    set_6 = set(list_4)
    print("set_6: ", set_6)
    print()

    # print("set_4 == set_6: ", (set_4 == set_6))
    # print()


def test_create_set_by_set_nest_set():
    """
    测试通过集合嵌套集合的方式创建一个集合

    测试结果:
    ```
    TypeError: unhashable type: 'set'
    ```
    """
    set_1 = {"apple", "orange", 1, 2, 3, {"四", "五", "六"}}
    print("set_1: ", set_1)


def test_create_set_by_set_nest_list_tuple_or_dict():
    """
    测试通过集合嵌套列表, 元组或字典的方式创建一个集合

    测试结果:
    ```
    TypeError: unhashable type: 'list'
    ```
    """
    set_1 = {
        "apple",
        "orange",
        1,
        2,
        3,
        ["四", "五", "六", {"a": 1, "b": (1, 2, ("五", {"a": 1, "b": 2}))}],
    }
    print("set_1: ", set_1)


def test_create_set_by_set_nest_list_or_tuple():
    """
    测试通过集合嵌套列表或元组的方式创建一个集合

    测试结果:
    ```
    TypeError: unhashable type: 'list'
    ```
    """
    set_1 = {
        "apple",
        "orange",
        1,
        2,
        3,
        ["四", "五", "六"],
        (7, 8, 9),
    }
    print("set_1: ", set_1)


def test_create_set_by_set_nest_tuple():
    """
    测试通过集合嵌套列表或元组的方式创建一个集合

    多次测试运行结果如下:
    ```
    set_1:  {1, 2, 3, (7, 8, 9), 'orange', 'apple'}
    set_1:  {1, 2, 3, 'apple', (7, 8, 9), 'orange'}
    ```
    """
    set_1 = {
        "apple",
        "orange",
        1,
        2,
        3,
        (7, 8, 9),
    }
    print("set_1: ", set_1)


def test_create_set_by_set_nest_tuple_2():
    """
    测试通过集合嵌套列表或元组的方式创建一个集合

    测试结果:
    ```
    set_1:  {'apple', 2, 3, 1, (7, 8, 9), 'orange', (10, 11, 12, (7, 8, 9))}
    ```
    """
    set_1 = {
        "apple",
        "orange",
        1,
        2,
        3,
        (7, 8, 9),
        (10, 11, 12, (7, 8, 9)),
    }
    print("set_1: ", set_1)


def test_create_set_by_set_nest_tuple_3():
    """
    测试通过集合嵌套列表或元组的方式创建一个集合

    测试结果:
    ```
    TypeError: unhashable type: 'list'
    ```
    """
    set_1 = {
        "apple",
        "orange",
        1,
        2,
        3,
        (7, 8, 9),
        (10, 11, 12, (7, 8, 9, [1, 2])),
    }
    print("set_1: ", set_1)


# run
# parseConsoleInputJsonDataAndSave()
# test_parse_json_data()
# test_create_set_data_compare()
# test_create_set_by_set_nest_set()
# test_create_set_by_set_nest_list_tuple_or_dict()
# test_create_set_by_set_nest_list_or_tuple()
# test_create_set_by_set_nest_tuple()
# test_create_set_by_set_nest_tuple_2()
test_create_set_by_set_nest_tuple_3()
