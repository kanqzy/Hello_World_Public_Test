# 将json数据格式成字符串

import common
import json_util
import log

LOGGER = log.Logger(logToHistory=False)


def isBlockType(obj):
    """
    判断对象是否是块类型: list, tuple, set, dict
    """
    if isinstance(obj, (list, tuple, set, dict)):
        return True
    return False


def getBlockEmptyString(blockObj):
    """
    获取块对象空值的字符串
        块对象所属类型: list, tuple, set, dict
    """
    if isinstance(blockObj, list):
        return "[]"
    elif isinstance(blockObj, tuple):
        return "()"
    elif isinstance(blockObj, set):
        return "{,}"
    elif isinstance(blockObj, dict):
        return "{}"
    return None


def getBlockSymbols(blockObj):
    """
    获取块对象的块符号
        块对象所属类型: list, tuple, set, dict

    返回:
        [开块符号, 闭块符号]
    """
    if isinstance(blockObj, list):
        return ["[", "]"]
    elif isinstance(blockObj, tuple):
        return ["(", ")"]
    elif isinstance(blockObj, set):
        return ["{", "}"]
    elif isinstance(blockObj, dict):
        return ["{", "}"]
    return None


def getBlockInfo(blockObj):
    """
    获取块对象的信息
        块对象所属类型: list, tuple, set, dict

    返回:
        ```
        {
            blockType: 块类型(list, tuple, set, dict)
            blockSymbols: [开块符号, 闭块符号],
        }
        ```
    """
    if isinstance(blockObj, list):
        return {"blockType": "list", "blockSymbols": ["[", "]"]}
    elif isinstance(blockObj, tuple):
        return {"blockType": "tuple", "blockSymbols": ["(", ")"]}
    elif isinstance(blockObj, set):
        return {"blockType": "set", "blockSymbols": ["{", "}"]}
    elif isinstance(blockObj, dict):
        return {"blockType": "dict", "blockSymbols": ["{", "}"]}
    return None


def getBlockEmptyData(blockType):
    """
    根据块类型获取对应的空数据
    """
    if blockType == "list":
        return []
    elif blockType == "tuple":
        return ()
    elif blockType == "set":
        return set()
    elif blockType == "dict":
        return {}
    return None


class TreeNode:
    """
    树形节点
    """

    # 每一次缩进空格数 默认4个
    Every_Indent_Space_Count = 4
    # 节点为键值对时, 键的包裹物 通常为单/双引号 默认双引号
    Key_Wrap = '"'

    def __init__(
        self,
        deep,
        treePath,
        parent,
        index=0,
        key=None,
        value=None,
        blockInfo=None,
        childs=[],
    ):
        """
        树形节点构造

        参数:
            deep                节点深度
            treePath            节点路径
                                树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
            parent              父节点 `TreeNode`
            index               节点在父节点下的索引序号
                                只有元组和列表的序号是永远确定的, 集合和字典每次遍历的序号可能不一样
            key                 节点在父节点下的键序号(当且仅当父节点为字典类型时有值)
            value               节点值 必须是单类型的值: int|float|...|str
            blockInfo           节点块信息 {type:"list|tuple|set|dict", "blockSymbols":[开块符号, 闭块符号]}
                                默认 None 表示非块节点
            childs              所有子节点 [TreeNode,...]
        """
        # 初始化赋值属性
        self.deep = deep
        self.treePath = treePath
        self.parent = parent
        self.index = index
        self.key = key
        self.value = value
        self.blockInfo = blockInfo
        self.childs = childs if isinstance(childs, list) and len(childs) > 0 else []

        # 计算属性
        # 格式化的树路径
        self._treePath_format = self.getFormatTreePath(treePath)

    def isBlock(self):
        """
        判断当前节点是否是块节点
        """
        if self.blockInfo and self.blockInfo["type"] in [
            "list",
            "tuple",
            "set",
            "dict",
        ]:
            return True
        return False

    def isDictBlock(self):
        """
        判断当前节点是否是字典块节点
        """
        if self.blockInfo and self.blockInfo["type"] == "dict":
            return True
        return False

    def isParentLastChild(self):
        """
        判断当前节点是否是父节点下的最后一个子节点
            如果当前节点没有父节点(树根), 也返回 `True`
        """
        if self.parent is None:
            return True
        elif isinstance(self.parent, TreeNode):
            if self.parent.lastChild() is self:
                return True
        return False

    def hasChildren(self):
        """
        判断当前节点是否有子节点
        """
        if isinstance(self.childs, list) and len(self.childs) > 0:
            return True
        # return isinstance(self.childs, list) and self.childs != []
        return False

    def child(self, childIndex=0):
        """
        根据子节点索引返回当前节点对应的子节点
            没有子节点或索引超出子节点长度, 返回 `None`
        """
        if not isinstance(childIndex, int):
            childIndex = 0
        if self.hasChildren() and childIndex < len(self.childs):
            return self.childs[childIndex]
        return None

    def addChild(self, child):
        """
        添加一个子节点  `TreeNode`
        """
        if isinstance(child, TreeNode):
            if child.parent is not self:
                child.parent = self
            self.childs.append(child)

    def lastChild(self):
        """
        返回当前节点最后一个子节点, 没有子节点返回 `None`
        """
        if self.hasChildren():
            return self.childs[-1:]
        return None

    def getFormatTreePath(self, treePath):
        """
        获取格式化的树路径
            由于树路径是字母和数字组合, 每一个子路径名短小, 人肉眼读取并记住该树路径, 非常不方便
            此处将其进行格式以便肉眼很好的阅读记忆每一个子路径名 每3个元素空2个空格
            例如: 原路径 `/c1/c0/c1/c0/c3/c0/c0/c2` 格式化后变为 `/c1/c0/c1  /c0/c3/c0  /c0/c2`
        """
        treePath_format = treePath
        treePathElements = treePath[1:].split("/")
        treePathElements_len = len(treePathElements)
        if treePathElements_len > 3:
            treePath_format = ""
            for i in range(treePathElements_len):
                treePathElement = treePathElements[i]
                space = "  " if i != 0 and (i + 1) % 3 == 1 else ""
                treePath_format += space + "/" + treePathElement

        return treePath_format

    def getBlockType(self):
        """
        根据块节点类型(list|tuple|set|dict)
        """
        if self.blockInfo:
            return self.blockInfo["type"]
        return None

    def getIndent(self):
        """
        获取当前节点缩进
            缩进规则: 每增加1层深度, 增加1个缩进(4个空格)
        """
        return common.getSpaceContent(self.deep * TreeNode.Every_Indent_Space_Count)

    def getChildLines(self):
        """
        获取所有子节点内容行
            每个节点格式: `${节点缩进}${格式化的节点内容},\n`
            每个子节点都以缩进开头, 换行结尾, 最后一个子节点内容后不跟逗号
        """
        lines = []
        if self.hasChildren():
            childsLen = len(self.childs)
            count = 1
            for childNode in self.childs:
                comma = ""
                if count < childsLen:
                    comma = ","
                # 子节点行键内容(仅限子节点是键值对时)
                childNode_line_keyContent = (
                    "{0}{1}{2}: ".format(
                        TreeNode.Key_Wrap, childNode.key, TreeNode.Key_Wrap
                    )
                    if childNode.key
                    else ""
                )

                # childNodeLine = (
                #     childNode.getIndent()
                #     + childNode_line_keyContent
                #     + childNode.toString()
                #     + comma
                #     + "\n"
                # )

                if isBlockType(childNode.value):
                    # 块类型 不要在开头加 `childNode_line_keyContent`,
                    # 这是因为 childNode toString() -> getAllLines() 中已经加过
                    childNodeLine = childNode.toString() + comma

                else:
                    childNodeLine = (
                        childNode.getIndent()
                        + childNode_line_keyContent
                        + childNode.toString()
                        + comma
                    )

                lines.append(childNodeLine)
                count += 1
        return lines

    def getAllLines(self):
        """
        获取当前节点的所有内容行
            当前节点及其所有深层的子节点内容行
            每个节点格式: `${节点缩进}${格式化的节点内容},`
            每个子节点都以缩进开头, 换行结尾, 最后一个子节点内容后不跟逗号
        """
        lines = []
        if isBlockType(self.value):
            line_keyContent = (
                "{0}{1}{2}: ".format(TreeNode.Key_Wrap, self.key, TreeNode.Key_Wrap)
                if self.key
                else ""
            )
            lines.append(
                self.getIndent() + line_keyContent + self.blockInfo["blockSymbols"][0]
            )
            lines.extend(self.getChildLines())
            lines.append(self.getIndent() + self.blockInfo["blockSymbols"][1])

        else:
            # comma = None
            # if self.isParentLastChild():
            #     # 父节点下的最后一个子节点后不跟逗号
            #     comma = ""
            # else:
            #     comma = ","
            # line = self.getIndent() + json_util.stringfy(self.value) + comma
            # line = self.getIndent() + json_util.stringfy(self.value)

            # 非块类型
            # 如果, 是根节点缩进为0; 如果是子节点, 缩进在 `getChildLines()` 中遍历子节时是进行添加
            # 故此处, 不要缩进
            # line = json_util.stringfy(self.value)
            line = json_util.stringfy(self.value)
            lines.append(line)

        return lines

    def toString(self, format=True):
        """
        将当前节点转为字符串

        参数:
            format      是否格式化
                        为 `True` 时使用和JSON一样标准的模式进行格式化
        """
        if format:
            return "\n".join(self.getAllLines())
        return json_util.stringfy(self.value)

    def toDict(self, deep=False):
        """
        将当前对象转换为字典
            `deep` 为 `True` 时表示会向下递归遍历每一个子节点并转换成字典,
            为了避免在后面的处理(比如JSON序列化时出现的循环引用问题), 转换时会去掉 `parent` 属性;
            反之, 则表示只将当前节点转换为字典
        """
        if deep:
            dictData = {
                "deep ": self.deep,
                "treePath ": self.treePath,
                "index ": self.index,
                "key ": self.key,
                "value ": self.value,
                "blockInfo ": self.blockInfo,
                "_treePath_format": self._treePath_format,
            }
            dictData["childs"] = []
            if self.hasChildren():
                for child in self.childs:
                    dictData["childs"].append(child.toDict(True))
            return dictData

        return {
            "deep ": self.deep,
            "treePath ": self.treePath,
            "parent ": self.parent,
            "index ": self.index,
            "key ": self.key,
            "value ": self.value,
            "blockInfo ": self.blockInfo,
            "childs": self.childs,
            "_treePath_format": self._treePath_format,
        }

    def showCurentNodeInfo(self):
        """
        展示当前节点信息
        """
        # 设置
        show_parent_value = False
        show_childs_value = False

        print("deep: ", self.deep)
        print("treePath: ", self.treePath)

        if show_parent_value:
            print("parent: ", self.parent)
        print("parent type: ", type(self.parent))

        print("index: ", self.index)
        print("key: ", self.key)
        print("value: ", self.value)
        print("blockInfo: ", self.blockInfo)

        if show_childs_value:
            print("childs: ", self.childs)
        print("childs type: ", type(self.childs))
        print("childs len: ", len(self.childs))
        print()

    def showCurentNodeInfo_in_log(self):
        """
        在日志中展示当前节点信息
        """
        # 设置
        show_parent_value = False
        show_childs_value = False

        LOGGER.info("deep: {0}", self.deep, raw=True)
        LOGGER.info("treePath: {0}", self.treePath, raw=True)

        if show_parent_value:
            LOGGER.info("parent: {0}", self.parent, raw=True)
        LOGGER.info("parent type: {0}", type(self.parent), raw=True)

        LOGGER.info("index: {0}", self.index, raw=True)
        LOGGER.info("key: {0}", self.key, raw=True)
        LOGGER.info("value: {0}", self.value, raw=True)
        LOGGER.info("blockInfo: {0}", self.blockInfo, raw=True)

        if show_childs_value:
            LOGGER.info("childs: {0}", self.childs, raw=True)
        LOGGER.info("childs type: {0}", type(self.childs), raw=True)
        LOGGER.info("childs len: {0}", len(self.childs), raw=True)
        LOGGER.info("", raw=True)
        LOGGER.info("", raw=True)

    def deepVisit(self, firstCall=True, mark=None):
        """
        对当前树形节点进行向下递归深度访问每一个子节点
        """
        # self.showCurentNodeInfo()
        if firstCall and mark:
            LOGGER.info("deepVisit mark[{0}]", mark, raw=True)
        self.showCurentNodeInfo_in_log()
        if self.hasChildren():
            for child in self.childs:
                child.deepVisit(False)
            LOGGER.info("", raw=True)

        else:
            return

    def deepVisit_2(self):
        self.showCurentNodeInfo_in_log()
        if self.hasChildren():
            for child in self.childs:
                child.deepVisit_2()

    def getInfo(self):
        """
        获取当前节点信息
        """
        info = (
            "{"
            + "deep:{0}, treePath:{1}, parent_type:{2}, index:{3}, key:{4}, value:{5}, childs_len:{6}".format(
                self.deep,
                self.treePath,
                type(self.parent),
                self.index,
                self.key,
                self.value,
                len(self.childs),
            )
            + "}"
        )
        return info

    @classmethod
    def iterateClearParentProperty(cls, treeNode):
        """
        从给定树形节点向下递归迭代访问, 每访问一个子节点, 清除其父属性 `parent`
            通常在将当前类的对象进行序列化时, 比如转换为JSON字符串时,
            需要清除 每层节点的父属性 `parent`, 否则会造成循环引用, 出现异常
        """
        if not isinstance(treeNode, TreeNode):
            return
        # print("treeNode: ", treeNode)
        # print("treeNode hasChildren: ", treeNode.hasChildren())
        treeNode.parent = None
        if treeNode.hasChildren():
            for child_treeNode in treeNode.childs:
                TreeNode.iterateClearParentProperty(child_treeNode)

    @classmethod
    def iterateSetProperty_for_JSON_serializable(cls, treeNode):
        """
        从给定树形节点向下递归迭代访问, 每访问一个子节点, 设置属性 以便
        在能当前类的对象进行序列化时, 比如转换为JSON字符串时,
        否则会造成循环引用, 出现异常

        向下递归迭代访问设置每个节点如下:
        ```
        1. `parent` 属性置空
        2. `value` 属性设置为JSON字符串形式
        ```
        """
        if not isinstance(treeNode, TreeNode):
            return
        # print("treeNode: ", treeNode)
        # print("treeNode hasChildren: ", treeNode.hasChildren())
        treeNode.parent = None
        treeNode.value = json_util.stringfy(treeNode.value)
        if treeNode.hasChildren():
            for child_treeNode in treeNode.childs:
                TreeNode.iterateClearParentProperty(child_treeNode)

    @classmethod
    def getDict(cls, treeNode, setNoneKeys=[]):
        """
        根据给定的节点获取对应的字典

        参数:
            setNoneKeys    置空的键
        """
        if not isinstance(treeNode, TreeNode):
            return None
        if not isinstance(setNoneKeys, list) or len(setNoneKeys) == 0:
            setNoneKeys = []
        treeNode_dict = treeNode.getDict()
        treeNode_dict_keys = treeNode_dict.keys()
        for setNoneKey in setNoneKeys:
            if setNoneKey in treeNode_dict_keys:
                treeNode_dict[setNoneKey] = None
        treeNode_dict["childs"] = []
        if treeNode.hasChildren():
            for child in treeNode.childs:
                treeNode_dict["childs"].append()


def loopDeepVisitTreeNode(treeNode):
    print("treeNode: ")
    print(treeNode.getInfo())
    print()
    if treeNode.hasChildren():
        for child in treeNode.childs:
            loopDeepVisitTreeNode(child)


def twoVisitTreeNode(treeNode):
    print("treeNode: ")
    print(treeNode.getInfo())
    print()

    if treeNode.hasChildren():
        for child_treeNode in treeNode.childs:
            print("child_treeNode: ")
            print(child_treeNode.getInfo())
            print()

            child_child_treeNode = child_treeNode.child()
            print("child_child_treeNode: ")
            print(child_child_treeNode.getInfo())
            print()

            print(
                "child_treeNode is child_child_treeNode: ",
                (child_treeNode is child_child_treeNode),
            )


def loopDeepVisitObj(obj, obj_treeNode):
    """
    向下递归深度访问对象数据

    参数:
        obj             每一次递归访问的对象
        obj_treeNode    每一次递归访问的对象创建的对应的树节点
    """
    obj_treeNode.value = obj
    obj_treeNode.childs = []

    if isBlockType(obj):
        obj_treeNode.blockInfo = getBlockInfo(obj)

        if isinstance(obj, dict):
            if len(obj.keys()) == 0:
                return

            count = 1
            for key, child_obj in obj.items():
                child_index = count - 1
                child_name = "cd{0}".format(child_index)
                child_key = key
                child_deep = obj_treeNode.deep + 1

                # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
                child_treePath = None
                if obj_treeNode.treePath == "/":
                    # child_treePath = "/" + child_name
                    child_treePath = "/" + child_key
                else:
                    child_treePath = obj_treeNode.treePath + "/" + child_key

                child_obj_treeNode = TreeNode(
                    child_deep, child_treePath, obj_treeNode, child_index, child_key
                )
                # 创建子树节点后, 递归调用一次当前方法, 然后在将其追加到父树节点下的 `childs`属性中
                loopDeepVisitObj(child_obj, child_obj_treeNode)
                obj_treeNode.childs.append(child_obj_treeNode)
                count += 1

        else:
            if len(obj) == 0:
                return

            count = 1
            for child_obj in obj:
                child_index = count - 1
                child_name = "c{0}".format(child_index)
                child_deep = obj_treeNode.deep + 1

                # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
                child_treePath = None
                if obj_treeNode.treePath == "/":
                    child_treePath = "/" + child_name
                else:
                    child_treePath = obj_treeNode.treePath + "/" + child_name

                child_obj_treeNode = TreeNode(
                    child_deep, child_treePath, obj_treeNode, child_index
                )
                # 创建子树节点后, 递归调用一次当前方法, 然后在将其追加到父树节点下的 `childs`属性中
                loopDeepVisitObj(child_obj, child_obj_treeNode)
                obj_treeNode.childs.append(child_obj_treeNode)
                count += 1

    else:
        return


def getTreeNode(obj):
    """
    获取对象的树形节点 `TreeNode`
    """
    if isBlockType(obj):
        obj_treeNode = TreeNode(0, "/", None, 0)
        loopDeepVisitObj(obj, obj_treeNode)
        return obj_treeNode

    return TreeNode(0, "/", None, 0, value=obj)


def loopDeepVisitTreeNode(tupleTreeNodePaths, treeNode, treeNode_data):
    """
    向下递归深度访问树形节点 `TreeNode` 对象数据, 同时在每一层构建对应的数据.
    如果树形节点是元组块, 将其按列表块进行数据构建, 并将当前层次节点访问路径记入 `tupleTreeNodePaths`

    参数:
        tupleTreeNodePaths  所有次递归访问的树形节点为元组块时的节点路径
        treeNode            每一次递归访问的树形节点 `TreeNode` 对象
        treeNode_data       每一次递归访问的对象创建的对应的节点数据
    """
    # VSCode代码感应区, 写完后面的代码将其注释掉
    # ```
    treeNode = TreeNode()
    # ```

    if isBlockType(treeNode.isBlock()):
        if treeNode.hasChildren():
            treeNode_blockType = treeNode.getBlockType()

            count = 1
            for child_treeNode in treeNode.childs:
                child_treeNode_blockType = child_treeNode.getBlockType()
                child_index = count - 1
                child_key = child_treeNode.key
                child_name = child_key if child_key else "c{0}".format(child_index)

                # 子树当前路径名称
                child_path_name = child_name

                # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
                child_treePath = None
                if treeNode.treePath == "/":
                    child_treePath = "/" + child_path_name
                else:
                    child_treePath = treeNode.treePath + "/" + child_path_name

                child_treeNode_data = None

                if child_treeNode_blockType in ["tuple", "list"]:
                    if child_treeNode_blockType == "tuple":
                        tupleTreeNodePaths.append(child_treePath)
                    child_treeNode_data = []

                elif child_treeNode_blockType == "set":
                    child_treeNode_data = set()

                elif child_treeNode_blockType == "dict":
                    child_treeNode_data = {}

                else:
                    child_treeNode_data = child_treeNode.value

                loopDeepVisitTreeNode(
                    tupleTreeNodePaths, child_treeNode, child_treeNode_data
                )

                if treeNode_blockType in ["tuple", "list"]:
                    treeNode_data.append(child_treeNode_data)
                elif treeNode_blockType == "set":
                    treeNode_data.add(child_treeNode_data)
                elif treeNode_blockType == "dict":
                    treeNode_data[child_key] = child_treeNode_data
                else:
                    pass

                count += 1

    else:
        # 非块节点(单一类型节点)
        return


def loopDeepVisitTreeData_and_convertToTuple(
    target_tupleNodePath,
    treeNode_data,
    treeNode_data_buildData,
):
    """
    向下递归深度访问根据树形节点 `TreeNode` 对象数据创建的数据 `treeNode_data`
    如果递归访问的路径是 `target_tupleNodePath`, 则将当前对象转为元组, 然后返回退出

    参数:
        target_tupleNodePath        目标元组节点路径
        treeNode_data               根据树形节点 `TreeNode` 对象数据创建的数据
        treeNode_data_parent        参数 `treeNode_data` 的父节点
        treeNode_data_parent_key    参数 `treeNode_data` 的父节点, 对子节点的访问键
                                    如果父节点是非字典节点, 键取子节点的遍历序号(集合节点)
        treeNode_data_buildData     在递归访问每层 `treeNode_data` 节点数据时, 构建的数据
                                    构建的数据为字典类型, 且必须包含节点的访问路径
    """
    if isBlockType(treeNode_data):
        treeNode_data_buildData["childs"] = []

        if isinstance(treeNode_data, dict):
            if len(treeNode_data.keys()) == 0:
                return

            source_data = None
            target_tupleData = None
            target_index = -1
            count = 1
            for key, child_treeNode_data in treeNode_data.items():
                child_index = count - 1
                child_name = key

                # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
                child_treePath = None
                if treeNode_data_buildData.treePath == "/":
                    child_treePath = "/" + child_name
                else:
                    child_treePath = treeNode_data_buildData.treePath + "/" + child_name

                if (
                    isinstance(child_treeNode_data, list)
                    and child_treePath == target_tupleNodePath
                ):
                    # 当前子节点数据就是要寻找的目标元组节点数据,
                    # 获取将其转换为列表的数据, 让后在让其父节点根据索引序号覆盖掉
                    source_data = child_treeNode_data
                    target_tupleData = tuple(child_treeNode_data)
                    target_index = child_index

                child_treeNode_data_buildData = {"treePath": child_treePath}
                loopDeepVisitTreeData_and_convertToTuple(
                    target_tupleNodePath,
                    child_treeNode_data,
                    child_treeNode_data_buildData,
                )
                count += 1

            if target_index != -1:
                if isinstance(treeNode_data, list):
                    treeNode_data[target_index] = target_tupleData
                    return

                elif isinstance(treeNode_data, set):
                    treeNode_data.remove(source_data)
                    treeNode_data.add(target_tupleData)
                    return

        else:
            if len(treeNode_data) == 0:
                return

            source_data = None
            target_tupleData = None
            target_index = -1
            count = 1
            for child_treeNode_data in treeNode_data:
                child_index = count - 1
                child_name = "c{0}".format(child_index)

                # 子树路径 树根为 `/`, 子树每向下一层追加 `/${子节点序号名称}`
                # 例如: /c1/c0/c1/c0/c3/c0/c0/c2
                child_treePath = None
                if treeNode_data_buildData.treePath == "/":
                    child_treePath = "/" + child_name
                else:
                    child_treePath = treeNode_data_buildData.treePath + "/" + child_name

                if (
                    isinstance(child_treeNode_data, list)
                    and child_treePath == target_tupleNodePath
                ):
                    # 当前子节点数据就是要寻找的目标元组节点数据,
                    # 获取将其转换为列表的数据, 让后在让其父节点根据索引序号覆盖掉
                    source_data = child_treeNode_data
                    target_tupleData = tuple(child_treeNode_data)
                    target_index = child_index

                child_treeNode_data_buildData = {"treePath": child_treePath}
                loopDeepVisitTreeData_and_convertToTuple(
                    target_tupleNodePath,
                    child_treeNode_data,
                    child_treeNode_data_buildData,
                )
                count += 1

            if target_index != -1:
                if isinstance(treeNode_data, list):
                    treeNode_data[target_index] = target_tupleData
                    return

                elif isinstance(treeNode_data, set):
                    treeNode_data.remove(source_data)
                    treeNode_data.add(target_tupleData)
                    return
    else:
        return


def getTreeData(treeNode):
    """
    获取树形节点 `TreeNode` 对象对应的数据
        获取规则:
            从 `treeNode` 树根开始向下递归遍历, 每一层节点, 同时构建一个数据与每层次节点对应.
            遍历完成后返回构建的树根数据.
            注意:
                在每层遍历时, 如果当前层节点是块节点, 则根据块类型,
                构建对应的块数据(例如: list块节点就构建一个列表);
                反之, 如果是非块节点(单一类型节点), 则取 当前层 `TreeNode` 对象的 `value` 属性值.
                由于元组只能一次性赋值整个数据, 无法像列表那样先创建空列表, 在一个个元素追加,
                所以在构建过程中, 会将其看成列表进行动态追加构建, 同时记录该列表的在树根节点中的访问路径,
                当构建完整个树根数据后, 按照访问路径的深度, 从最深的访问路径开始遍历, 并将对应的节点数据转换为元组
    """
    if not isinstance(treeNode, TreeNode):
        return None

    tupleTreeNodePaths = []
    blockType = TreeNode.getBlockType()
    treeNode_data = getBlockEmptyData(blockType) if blockType else treeNode.value
    loopDeepVisitTreeNode(tupleTreeNodePaths, treeNode, treeNode_data)
    # 将需要替换为元组的节点路径进行排序(路径最深的放在最前面)
    tupleTreeNodePaths.sort(key=lambda x: len(x.split("/")), reverse=True)

    # 遍历每一个需要替换的元组路径, 并在 `treeNode_data` 的子节点中找到对应的节点并替换为元组
    for tupleTreeNodePath in tupleTreeNodePaths:
        treeNode_data_buildData = {"deep": 0, "treePath": "/"}
        loopDeepVisitTreeData_and_convertToTuple(
            tupleTreeNodePath, treeNode_data, treeNode_data_buildData
        )

    return treeNode_data
