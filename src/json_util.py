# json工具


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
