# 脚本公共模块
#   一些日常使用的公共脚本方法, 类等

import re
import time
import traceback

import pyautogui
import pyperclip
import uiautomation as auto
import win32gui

import util

# str


def getSpaceContent(count=1, bracketed=False):
    """
    根据空格数获取空格内容

    参数:
        bracketed   返回的内容是否用中括号 `[]`括起来
                    由于空格肉眼无法看见, 没有中括号括起来无法看到边界，确定整体样子
    """
    if not isinstance(count, int):
        count = 1
    spaceContent = ""
    for i in range(count):
        spaceContent += " "
    if bracketed:
        return "[{0}]".format(spaceContent)
    return spaceContent


def getMultiStrContent(string, count=1):
    """
    获取给定字符的倍数个构成的新字符串内容
    """
    if not isinstance(count, int) or count < 1:
        count = 1
    multiStrContent = ""
    for i in range(count):
        multiStrContent += string

    return multiStrContent


def getContentSpaceCount(content):
    """
    根据文本内容空格数
    """
    if not isinstance(content, str):
        return -1
    return content.count(" ")


def replaceUndrerlineWithSpace(string, space=" "):
    """
    将下划线替换为空格

    参数:
        string      要替换的字符串
        space       替换的空格 必须是一到多个 `\t`或 `\s` 默认一个空格

    返回:
        返回替换后的内容
    """
    if not isinstance(string, str):
        return None
    if not isinstance(space, str) or not re.match(r"^\s+|\t+$", space):
        space = " "
    return re.sub(r"_+", space, string)


def replaceSpaceWithUndrerline(string, undrerline="_"):
    """
    将空格替换为下划线
        只替换字符串中的 `\t`或 `\s`空格

    参数:
        string      要替换的字符串
        undrerline  替换的下划线 必须是一到多个 `_` 默认一个下划线

    返回:
        返回替换后的内容
    """
    if not isinstance(string, str):
        return None
    if not isinstance(undrerline, str) or not re.match(r"^_+$", undrerline):
        undrerline = "_"
    return re.sub(r"\s+|\t+", undrerline, string)


def splitWord(wordString, separator=" ", firstLowerCase=True):
    """
    分割单词字符串
        分割规则: 检测要分割的单词字符串, 遇到大写字母, 就拆分

    参数：
        wordString      要分割的单词字符串
        separator       分隔符 默认一个空格
        firstLowerCase  分割后首字母是否小写 默认 `True`

    示例:
    ```
    `YoudaoDictFormAnalysis` => `youdao dict form analysis`
    `baiduImageRecognize` => `baidu image recognize`
    ```

    返回:
        返回分割后的文本内容
    """
    if not isinstance(wordString, str):
        return None
    elif re.match(r"^(\s|\t)*$", wordString) or len(wordString) == 1:
        return wordString

    if not isinstance(separator, str):
        separator = " "
    # 分割前, 将第一个字符转为小写
    wordString = wordString[0].lower() + wordString[1:]
    wordStrs = re.split(r"([A-Z])", wordString)
    print("wordStrs: ", wordStrs)
    if len(wordStrs) <= 1:
        return wordString
    wordStringNew = ""
    for wordStr in wordStrs:
        # if not wordStr:
        #     continue
        if re.match(r"^[A-Z]$", wordStr):
            letter = wordStr
            if firstLowerCase:
                letter = letter.lower()
            wordStringNew += separator + letter

        else:
            wordStringNew += wordStr

    return wordStringNew


def combineWord(
    wordStringContent, mode="firstWordLower", firstLowerCase=True, leftUpperCase=True
):
    """
    分割合并字符串
        合并规则: 检测要合并的单词字符串内容, 去除分隔符(空格,下划线,连接符)后
                合并成一个单词

    参数:
        wordStringContent   要合并的单词字符串内容
        mode                如下合并模式:
                                1. firstWordLower       第一个单词全部小写, 剩余单词全部首字母大写,其余字母小写
                                                        这是多个单词合并成一个词的常用写法 例如: `extractWindowInspect`
                                2. allWordsFirstUpper   所有单词全部首字母大写,其余字母小写 例如: `ExtractWindowInspect`

    示例:
    ```
    `extract window inspect` => `extractWindowInspect`
    `Extract window Inspect` => `extractWindowInspect`
    `Extract__window__Inspect` => `extractWindowInspect`
    ```
    返回:
        返回合并后的一个单词串
    """
    if not isinstance(wordStringContent, str):
        return None
    if not isinstance(wordStringContent, str) or wordStringContent not in [
        "firstWordLower",
        "allWordsFirstUpper",
    ]:
        mode = "firstWordLower"

    wordStrs = re.split(r"\s+|\t+|_+|\-+", wordStringContent)
    wordStrsLen = len(wordStrs)
    if wordStrsLen <= 1:
        if mode == "firstWordLower":
            return wordStringContent.lower()
        elif mode == "allWordsFirstUpper":
            return wordStringContent.capitalize()
        return wordStringContent

    if mode == "firstWordLower":
        wordStringContentNew = wordStrs[0].lower()
        index = 1
        while index < wordStrsLen:
            wordStringContentNew += wordStrs[index].capitalize()
            index += 1
        return wordStringContentNew

    elif mode == "allWordsFirstUpper":
        wordStringContentNew = ""
        for wordStr in wordStrs:
            wordStringContentNew += wordStr.capitalize()
        return wordStringContentNew

    else:
        return wordStringContent


# list


def findDictElement(listObj, targetDict):
    """
    从类别对象中查找字典元素
        查找过程: 从前往后扫描列表对象, 发现子元素为字典类型
            且 `targetDict` 下键值均与 该子元素相等, 则返回该子元素

    参数:
        targetDict      目标字典对象

    返回:
        返回扫描到的子元素, 扫描不到返回 `None`
    """
    if (
        not isinstance(listObj, list)
        or listObj == []
        or not isinstance(targetDict, dict)
    ):
        return None

    for element in listObj:
        if targetDict == element:
            return element
        elif isinstance(element, dict):
            isMatch = True
            for key, value in targetDict.items:
                if element.get(key) != value:
                    isMatch = False
                    break
            if isMatch:
                return element

    return None


# dict


def isDictMatch(dictData, dictTemplate):
    """
    判断字典数据是否与字典模板匹配
        匹配规则: 字典数据必须和字典模板具有相同的键, 且每一个键所对应的值
        都必须等于或属于字典模板中的值或值所属类型

    参数:
        dictData        字典数据 dict
        dictTemplate    字典模板 {key:str, value: {value:object|values:list, valueType:Type|(Type)}}
    """
    if not isinstance(dictData, dict) or not isinstance(dictTemplate):
        return False

    dictData_keys_len = len(dictData.keys())
    dictTemplate_keys_len = len(dictTemplate.keys())
    if dictData_keys_len != dictTemplate_keys_len:
        return False

    if dictData_keys_len == 0:
        return True

    for key, value in dictData.items():
        if value is None:
            continue

        # 模板中没有该键, 直接返回 `False`
        dictTemplate_value = dictTemplate.get(key)
        if dictTemplate_value is None:
            return False

        # 读取模板中该键对应的值 {value:object|values:list, valueType:Type|Type}
        # 若该值为一个空字典 `{}`, 则表示对 `value`不做像现在
        # 若该值有键 `value`，则判断该键所对应的值是否与 `value` 相等;
        # 若该值有键 `values`, 则判断 `value` 是否在 该键所对应的值的列表中
        # 若该值有键 `valueType`, 则判断 `value` 是否是该键所对应的值的类型或类型元组
        if dictTemplate_value == {}:
            continue

        tempalte_value = dictTemplate_value.get("value")
        tempalte_values = dictTemplate_value.get("values")
        tempalte_valueType = dictTemplate_value.get("valueType")

        if tempalte_value:
            if tempalte_value != value:
                return False

        elif tempalte_values:
            if value not in tempalte_values:
                return False

        elif tempalte_valueType:
            if not isinstance(value, tempalte_valueType):
                return False

    return True


# 鼠标和键盘


def write_chatGPT_ask_content_to_py_top_refer():
    """
    将对chatGPT的提问内容写到 python脚本文件的头部参考下

    操作过程:
    ```
    1. 手动将对chatGPT提问的问题复制到剪贴板，然后将输入法切位搜狗中文
        注意: 复制的每行内容都要包括该行缩进
    2. 在控制台启动当前脚本方法, 并休眠3秒, 在这3秒钟, 将cmd控制台最小化,
        然后在pythonIDE编辑工具(VSCode, PyCharm等)中, 打开正在编辑的.py文件窗口
        将鼠标移到编写chatGPT引用参考处, 点击以下;
        接着, 程序会自动从光标处开始写入剪贴板中的内容:
            1. 首先, 模拟键盘输入 `# cank:`, 然后回车. 其中输入 `cank`后按一个空格, 代表输入中文 `参考`,
                `:`会显示为中文`：`
            2. 接着, 按 `shift`， 输入法切位英文, 然后输入 `#   ask chatGPT:`，然后回车
            3. 接着, 记录当前鼠标光标位置, 并将剪贴板整个内容复制粘贴上去
            4. 最后, 鼠标光标重新回到刚刚记录的位置, 并向下一行行为每行内容加上注释缩进, 并确保对齐: `#`和空格(\s|\t)
    ```

    示例:
    对chatGPT提问的问题内容:
    ```
        请用python 写两个方法:
        1. 第一个方法用于获取当前windows电脑上的音量
        2. 第二个方法用于设置音量, 第一个参数为是否静音,第二个参数为音量值, 取值[0-100]
    要求:
        方法要能实现人工手动在windows电脑上点击屏幕底部栏目音量图标的设置效果
    ```

    运行当前脚本在.py文件中写入的内容:
    ```
    # 参考:
    #   ask chatGPT:
    #       请用python 写两个方法:
    #           1. 第一个方法用于获取当前windows电脑上的音量
    #           2. 第二个方法用于设置音量, 第一个参数为是否静音,第二个参数为音量值, 取值[0-100]
    #       要求:
    #           方法要能实现人工手动在windows电脑上点击屏幕底部栏目音量图标的设置效果
    ```
    """
    # time.sleep(3)
    time.sleep(5)
    chatGPT_ask_content = None
    try:
        chatGPT_ask_content = pyperclip.waitForPaste(1)
    except Exception as e:
        print("waitForPaste err")
        traceback.print_exc()
        # 重新激活聚焦控制台窗口
        auto.GetConsoleWindow().SetActive()
        return

    xPos, yPos = pyautogui.position()
    # pyautogui.write("# cank :",0.5)
    # pyautogui.write("# cank :",0.25)
    pyautogui.write("# cank :", 0.1)
    pyautogui.hotkey("enter")

    pyautogui.hotkey("shift")
    time.sleep(0.5)
    pyautogui.write("#   ask chatGPT:")
    pyautogui.hotkey("enter")

    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # 当前方法从开始执行到现在, 全是模拟鼠标操作，不涉及到鼠标移动,
    # 因此, 点击后鼠标光标就是当前方法执行前的光标位置(并没有变化)
    pyautogui.click()
    xPos_2, yPos_2 = pyautogui.position()
    if xPos_2 != xPos or yPos_2 != yPos:
        pyautogui.moveTo(xPos, yPos)
        pyautogui.click()
    time.sleep(0.5)
    # 鼠标光标回到行首, 并向2行
    pyautogui.hotkey("home")
    pyautogui.hotkey("down")
    pyautogui.hotkey("down")

    # 计算对chatGPT提问的问题内容行(最后分割的是空字符串要减1)
    chatGPT_ask_content_lineCount = len(chatGPT_ask_content.split("\n")) - 1
    lineCount = 1
    while lineCount <= chatGPT_ask_content_lineCount:
        pyautogui.write("#\t")
        pyautogui.hotkey("home")
        pyautogui.hotkey("down")
        time.sleep(0.5)
        lineCount += 1


# 测试


def test_replaceUndrerlineWithSpace():
    """
    测试方法 `replaceUndrerlineWithSpace`
    """
    content = input("content: ")
    result = replaceUndrerlineWithSpace(content, " ")
    print("replace result: ", result)


def test_replaceSpaceWithUndrerline():
    """
    测试方法 `replaceSpaceWithUndrerline`
    """
    content = input("content: ")
    result = replaceSpaceWithUndrerline(content, " ")
    print("replace result: ", result)


def test_splitWord():
    """
    测试方法 `splitWord`
    """
    content = input("content: ")
    result = splitWord(content)
    print("splitWord result: [{0}]".format(result))


def test_combineWord():
    """
    测试方法 `combineWord`
    """
    content = input("content: ")
    result = combineWord(content)
    print("combineWord result: [{0}]".format(result))
