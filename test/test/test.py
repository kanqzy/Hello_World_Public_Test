import traceback


class AAA:
    def __init__(self, a, b, c=100) -> None:
        self.a = a
        self.b = b
        self.c = c

    def toString(self):
        return "{" + "a:{0}, b:{1}, c:{2}".format(self.a, self.b, self.c) + "}"


def test_string_to_bool():
    """
    测试将字符串转bool
    """
    strings = ["", "/", "0", "1", "True", "False", "true", "tRUe"]
    for string in strings:
        boolValue = None
        try:
            boolValue = bool(string)
        except Exception as e:
            print("string to bool err")
            traceback.print_exc()
            print()
            continue

        print("string: [{0}]".format(string))
        print("boolValue type: ", type(boolValue))
        print("boolValue: ", boolValue)
        print()


def test_set_class_AAA_instance_property_outer():
    """
    测试 在外部设置类 `AAA` 的实例对象属性值
    """
    aaa = AAA("一", 2)
    print("aaa: ", aaa.toString())
    print()

    aaa.c = 200
    print("after outer set property")
    print("aaa: ", aaa.toString())
    print()


# run
# test_string_to_bool()
test_set_class_AAA_instance_property_outer()
