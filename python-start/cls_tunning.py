GLOBAL_VAR = ('GLOBAL_VAR')  # 全局常量，大写字母，下划线分割


# 类名，以驼峰式命名，要求以object作为继承类
# 继承自 object 是为了使属性(properties)正常工作
# 使其不受Python 3000的一个特殊的潜在不兼容性影响. 同时也实现了object的默认语义
class BaseClass(object):

    class_var = 'class_var'  # 类变量

    def __init__(self):  # 构造函数
        self.inst_var = 'inst_var'  # 成员变量
        self._mod_or_protected_var = '_mod_or_protected_var'  # 模块变量或者protected变量，以单个下划线开头
        self.__private__var = '__private__var'   # 私有变量，以双下划线开头

    def inst_method(self, param):  # public实例函数，以self开头变量的函数
        print(self.__private__var)
        print(param)

    def _mod_protected_method(self):  # 模块或者protected方法，以单个下划线开头，其他模块import * from时候不会导入
        pass

    def __private_method(self):  # 私有方法，以双下划线开头
        pass

    @classmethod
    def class_method(cls, var):  # 类方法，第一个参数是cls，用classmethod修饰
        print(var)

    @staticmethod
    def static_method(param):  # 静态方法，没有self或者cls作为第一个参数，staticmethod注解修饰
        print(param)


