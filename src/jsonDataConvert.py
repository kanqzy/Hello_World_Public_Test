# json数据类型转换


def test_convert_dictData_to_listData():
    """
    测试将字典数据转换为列表
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

    list_1 = list(dict_1)
    print("list_1: ")
    print(list_1)
    print()


def test_convert_listData_to_tupleData():
    """
    测试将列表数据转换为元组数据
    """
    list_1 = [1, 2, ("3", (5, 6))]

    tuple_1 = tuple(list_1)
    print("tuple_1: ")
    print(tuple_1)
    print()

def test_convert_listData_to_setData():
    """
    测试将列表数据转换为元组数据
    """
    list_1 = [1, 2, ("3", (5, 6))]

    set_1 = set(list_1)
    print("set_1: ")
    print(set_1)
    print()


# run
# test_convert_dictData_to_listData()
# test_convert_listData_to_tupleData()
test_convert_listData_to_setData()
