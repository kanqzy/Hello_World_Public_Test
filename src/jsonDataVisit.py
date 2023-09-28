# json数据访问

import json

import util


def json_stringfy_detail_list_or_tuple(data):
    """ """


def isBlockType(obj):
    """
    判断对象是否是块类型: list, tuple, set, dict
    """
    if isinstance(obj, (list, tuple, set, dict)):
        return True
    return False


def loopDeepVisitObj(obj, obj_data):
    """
    递归循环深度访问对象数据
    """
    # 设置
    show_tuple = False

    obj_data["type"] = str(type(obj))
    obj_data["childs"] = []

    if isinstance(obj, dict):
        if len(obj.keys()) == 0:
            return

        count = 1
        for key, child_obj in obj.items():
            child_index = count - 1
            child_name = "cd_{0}".format(key)
            child_deep = obj_data["deep"] + 1

            # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
            # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
            child_treePath = None
            if obj_data["treePath"] == "/":
                child_treePath = "/" + child_name
            else:
                child_treePath = obj_data["treePath"] + "/" + child_name

            # 由于树路径是字母和数字组合, 每一个子路径名短小, 人肉眼读取并记住该树路径, 非常不方便
            # 此处将其进行格式以便肉眼很好的阅读记忆每一个子路径名 每3个元素空2个空格
            # 例如: 原路径 `/c1/c0/c1/c0/c3/c0/c0/c2` 格式化后变为 `/c1/c0/c1  /c0/c3/c0  /c0/c2`
            child_treePath_format = child_treePath
            treePathElements = child_treePath[1:].split("/")
            treePathElements_len = len(treePathElements)
            if treePathElements_len > 3:
                child_treePath_format = ""
                for i in range(treePathElements_len):
                    treePathElement = treePathElements[i]
                    space = "  " if i != 0 and (i + 1) % 3 == 1 else ""
                    child_treePath_format += space + "/" + treePathElement

            child_obj_data = {
                "index": child_index,
                "childKey": key,
                "childName": child_name,
                "deep": child_deep,
                "treePath": child_treePath,
                "treePath_format": child_treePath_format,
            }
            # print("child_obj_data: ", child_obj_data)
            loopDeepVisitObj(child_obj, child_obj_data)
            obj_data["childs"].append(child_obj_data)
            count += 1

    elif isBlockType(obj):
        isTuple = isinstance(obj, tuple)
        if show_tuple:
            if isTuple:
                print("obj => 元组类型")

        if len(obj) == 0:
            return

        count = 1
        for child_obj in obj:
            if show_tuple:
                if isTuple:
                    print("child_obj: ", child_obj)

            child_index = count - 1
            child_name = "c{0}".format(child_index)
            child_deep = obj_data["deep"] + 1

            # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
            # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
            child_treePath = None
            if obj_data["treePath"] == "/":
                child_treePath = "/" + child_name
            else:
                child_treePath = obj_data["treePath"] + "/" + child_name

            # 由于树路径是字母和数字组合, 每一个子路径名短小, 人肉眼读取并记住该树路径, 非常不方便
            # 此处将其进行格式以便肉眼很好的阅读记忆每一个子路径名 每3个元素空2个空格
            # 例如: 原路径 `/c1/c0/c1/c0/c3/c0/c0/c2` 格式化后变为 `/c1/c0/c1  /c0/c3/c0  /c0/c2`
            child_treePath_format = child_treePath
            treePathElements = child_treePath[1:].split("/")
            treePathElements_len = len(treePathElements)
            if treePathElements_len > 3:
                child_treePath_format = ""
                for i in range(treePathElements_len):
                    treePathElement = treePathElements[i]
                    space = "  " if i != 0 and (i + 1) % 3 == 1 else ""
                    child_treePath_format += space + "/" + treePathElement

            child_obj_data = {
                "index": child_index,
                "childName": child_name,
                "deep": child_deep,
                "treePath": child_treePath,
                "treePath_format": child_treePath_format,
            }
            loopDeepVisitObj(child_obj, child_obj_data)
            obj_data["childs"].append(child_obj_data)
            count += 1

    else:
        obj_data["value"] = obj
        return


def get_obj_json_detail_data(obj):
    """
    获取对象的详细json数据
        获取的JSON是一颗树, 每层节点都会包含深度, 和访问路径
    """
    if isBlockType(obj):
        obj_data = {"deep": 0, "treePath": "/"}
        loopDeepVisitObj(obj, obj_data)
        return obj_data

    return {"type": "singleType", "typeName": str(type(obj)), "value": obj}


def test_get_obj_json_detail_data():
    """
    测试 函数 `get_obj_json_detail_data`
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
    dict_detail_data = get_obj_json_detail_data(dict_1)

    util.writeJson(
        "../out/jsonDataVisit/test_get_obj_json_detail_data/dict_detail_data.json",
        dict_detail_data,
        indent=4,
    )

    print("write complete")


# run
# test_get_obj_json_detail_data()
