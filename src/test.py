# 测试模块

import json

import jsonDataFormatString as jdfs
import log
import util

LOGGER = log.Logger(logName="test", logInConsole=True, logToHistory=False)

# 测试 `jsonDataFormatString.py` 模块


def test_create_TreeNode_of_jsonDataFormatString():
    """
    测试模块 `jsonDataFormatString` 下的类 `getTreeNode` 树形对象的创建
    """
    # 设置
    iterateClearParentProperty = False
    iterateSetProperty_for_JSON_serializable = False
    append_child_treeNode_2_childs = False

    root_treeNode = jdfs.TreeNode(0, "/", None, value="0")
    print("root_treeNode.childs: ", root_treeNode.childs)

    child_treeNode_1 = jdfs.TreeNode(1, "/c0", None, value="0_1")
    print("child_treeNode_1.childs: ", child_treeNode_1.childs)

    # child_treeNode_2 = jdfs.TreeNode(1, "/c1", None, value="0_2")
    # child_treeNode_3 = jdfs.TreeNode(1, "/c2", None, value="0_3")

    root_treeNode.childs.append(child_treeNode_1)
    print("after root_treeNode.childs.append")
    print("root_treeNode.childs: ", root_treeNode.childs)
    print("child_treeNode_1.childs: ", child_treeNode_1.childs)
    print(
        "root_treeNode.childs is child_treeNode_1.childs: ",
        (root_treeNode.childs is child_treeNode_1.childs),
    )

    # root_treeNode.childs.append(child_treeNode_2)
    # root_treeNode.childs.append(child_treeNode_3)

    # root_treeNode.addChild(child_treeNode_1)
    # root_treeNode.addChild(child_treeNode_2)
    # root_treeNode.addChild(child_treeNode_3)

    if append_child_treeNode_2_childs:
        child_treeNode_2_1 = jdfs.TreeNode(2, "/c1/c0", None, value="0_2_1")
        child_treeNode_2_2 = jdfs.TreeNode(2, "/c1/c1", None, value="0_2_2")
        child_treeNode_2_3 = jdfs.TreeNode(2, "/c1/c2", None, value="0_2_3")
        # child_treeNode_2.childs.append(child_treeNode_2_1)
        # child_treeNode_2.childs.append(child_treeNode_2_2)
        # child_treeNode_2.childs.append(child_treeNode_2_3)

    # root_treeNode.deepVisit(True, "111")
    # jdfs.loopDeepVisitTreeNode(root_treeNode)
    # jdfs.twoVisitTreeNode(root_treeNode)

    return

    if iterateClearParentProperty:
        jdfs.TreeNode.iterateClearParentProperty(root_treeNode)

    print("after iterateClearParentProperty")

    # root_treeNode.deepVisit(True, "222")

    if iterateSetProperty_for_JSON_serializable:
        jdfs.TreeNode.iterateSetProperty_for_JSON_serializable(root_treeNode)

    root_treeNode_jsonString = json.dumps(root_treeNode, indent=4)
    util.writeContent(
        "../out/test/test_create_TreeNode/root_treeNode.json", root_treeNode_jsonString
    )

    print("complete")


def test_create_TreeNode_of_jsonDataFormatString_after_fix_bug():
    """
    测试模块 `jsonDataFormatString` 下的类 `getTreeNode` 树形对象的创建

    说明: 在修复了 构造器 默认值参数 `childs` 未进行list类型三元运算符判断复制 bug
    进行的测试
    """
    # 设置
    iterateClearParentProperty = True
    iterateSetProperty_for_JSON_serializable = False
    append_child_treeNode_2_childs = False

    root_treeNode = jdfs.TreeNode(0, "/", None, value="0")

    child_treeNode_1 = jdfs.TreeNode(1, "/c0", root_treeNode, value="0_1")
    child_treeNode_2 = jdfs.TreeNode(1, "/c1", root_treeNode, value="0_2")
    child_treeNode_3 = jdfs.TreeNode(1, "/c2", root_treeNode, value="0_3")

    root_treeNode.childs.append(child_treeNode_1)
    root_treeNode.childs.append(child_treeNode_2)
    root_treeNode.childs.append(child_treeNode_3)

    child_treeNode_2_1 = jdfs.TreeNode(2, "/c1/c0", child_treeNode_2, value="0_2_1")
    child_treeNode_2_2 = jdfs.TreeNode(2, "/c1/c1", child_treeNode_2, value="0_2_2")
    child_treeNode_2_3 = jdfs.TreeNode(2, "/c1/c2", child_treeNode_2, value="0_2_3")
    child_treeNode_2.childs.append(child_treeNode_2_1)
    child_treeNode_2.childs.append(child_treeNode_2_2)
    child_treeNode_2.childs.append(child_treeNode_2_3)

    if iterateClearParentProperty:
        jdfs.TreeNode.iterateClearParentProperty(root_treeNode)

    print("after iterateClearParentProperty")

    if iterateSetProperty_for_JSON_serializable:
        jdfs.TreeNode.iterateSetProperty_for_JSON_serializable(root_treeNode)

    root_treeNode_jsonString = json.dumps(
        root_treeNode, indent=4, default=lambda obj: obj.__dict__
    )
    util.writeContent(
        "../out/test/test_create_TreeNode/root_treeNode.json", root_treeNode_jsonString
    )

    print("complete")


def test_TreeNode_toDict_getTreeNode_of_jsonDataFormatString():
    """
    测试模块 `jsonDataFormatString` 下的类 `TreeNode` 中的
    方法 `toDict` 和 函数 `getTreeNode`
    """
    # 设置
    show_treeNode_dictData = False

    dict_2 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "二", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
        "abc": ("三", [1, {"二", 3}, (4, (5, 6)), False]),
    }

    dict_3 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "two", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_zhangsan",
        "pass_mima_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
        "abc": ("three", [1, {"two", 3}, (4, (5, 6)), False]),
    }

    # 包含set对象 TypeError: Object of type set is not JSON serializable
    dict_4 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": [1, "two", 3]}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_zhangsan",
        "pass_mima_word": "246810",
        "members_2": [1, 2, ["3", [5, 6]]],
        "abc": ["three", [1, {"two", 3}, [4, [5, 6]], False]],
    }

    dict_5 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "二", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
        "abc": ("三", [1, ["二", 3], (4, (5, 6)), False]),
    }

    # treeNode = jdfs.getTreeNode(dict_2)
    # treeNode = jdfs.getTreeNode(dict_3)
    # treeNode = jdfs.getTreeNode(dict_4)
    treeNode = jdfs.getTreeNode(dict_5)
    treeNode_dictData = treeNode.toDict(True)

    if show_treeNode_dictData:
        print("treeNode_dictData type: ", type(treeNode_dictData))
        print("treeNode_dictData: ", treeNode_dictData)

    util.writeJson(
        "../out/test/TreeNode_toDict_getTreeNode/treeNode_dictData.json",
        treeNode_dictData,
        indent=4,
    )
    print("complete")


def test_getTreeNode_of_jsonDataFormatString():
    """
    测试模块 `jsonDataFormatString` 下的函数 `getTreeNode`
    """
    # 设置
    deepVisitTreeNode = True
    iterateClearParentProperty = True
    iterateSetProperty_for_JSON_serializable = False
    use_writeJson = False

    outDir = "../out/test/jsonDataFormatString/test_getTreeNode"

    # 1|2
    run = 2

    dict_1 = {"type": "file", "filepath": "D:/book/Python", "value": 3}

    dict_2 = {
        "remote-pc": {
            "server": {"ip": "192.168.0.102", "port": "10086", "members": (1, "二", 3)}
        },
        "duration": "5 * 60 * 1000",
        "username": "user_张三",
        "pass_密码_word": "246810",
        "members_2": (1, 2, ("3", (5, 6))),
        "abc": ("三", [1, {"二", 3}, (4, (5, 6)), False]),
    }

    dict_data = None
    outPath = None

    if run == 1:
        dict_data = dict_1
        outPath = outDir + "/treeNode_1.json"

    elif run == 2:
        dict_data = dict_2
        outPath = outDir + "/treeNode_2.json"

    treeNode = jdfs.getTreeNode(dict_data)
    print("treeNode type: ", type(treeNode))
    print("treeNode: ", treeNode)
    print()

    if deepVisitTreeNode:
        print("ready for  treeNode.deepVisit(): ")
        treeNode.deepVisit(True, "111")
        print("treeNode.deepVisit() end")

    if iterateClearParentProperty:
        jdfs.TreeNode.iterateClearParentProperty(treeNode)

    if iterateSetProperty_for_JSON_serializable:
        jdfs.TreeNode.iterateSetProperty_for_JSON_serializable(treeNode)

    print("after iterateClearParentProperty")
    print()

    if deepVisitTreeNode:
        print("ready for  treeNode.deepVisit(): ")
        treeNode.deepVisit(True, "222")
        print("treeNode.deepVisit() end")

    if use_writeJson:
        util.writeJson(
            outPath,
            treeNode,
            indent=4,
        )

    else:
        treeNode_json_string = json.dumps(
            treeNode, ensure_ascii=False, default=lambda obj: obj.__dict__
        )
        util.writeContent(
            outPath,
            treeNode_json_string,
        )

    print("complete")


def test_TreeNode_toString_of_jsonDataFormatString():
    """
    测试模块 `jsonDataFormatString` 下的类 `TreeNode` 中的
    方法 `toString`
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
    treeNode = jdfs.getTreeNode(dict_1)
    treeNode_formatString = treeNode.toString()

    util.writeContent(
        "../out/test/TreeNode_toString/treeNode_formatString.data",
        treeNode_formatString,
    )
    print("complete")


def test_TreeNode_toString_style_of_jsonDataFormatString():
    """
    测试模块 `jsonDataFormatString` 下的类 `TreeNode` 中的
    方法 `toString`. 通关 设置 `TreeNode` 类样式属性: `Every_Indent_Space_Count` 和 `Key_Wrap`
    来生成对应样式的格式化字符串
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

    # 设置 `TreeNode` 类样式属性: `Every_Indent_Space_Count` 和 `Key_Wrap`
    styles = [[3, ""], [5, "'"], [6, "`"]]
    count = 1
    for style in styles:
        jdfs.TreeNode.Every_Indent_Space_Count = style[0]
        jdfs.TreeNode.Key_Wrap = style[1]

        treeNode = jdfs.getTreeNode(dict_1)
        treeNode_formatString = treeNode.toString()

        util.writeContent(
            "../out/test/TreeNode_toString_style/treeNode_formatString_style_{0}.data".format(
                count
            ),
            treeNode_formatString,
        )
        count += 1

    print("complete")


# run
# test_create_TreeNode_of_jsonDataFormatString()
# test_create_TreeNode_of_jsonDataFormatString_after_fix_bug()
# test_TreeNode_toDict_getTreeNode_of_jsonDataFormatString()
# test_getTreeNode_of_jsonDataFormatString()
# test_TreeNode_toString_of_jsonDataFormatString()
test_TreeNode_toString_style_of_jsonDataFormatString()
