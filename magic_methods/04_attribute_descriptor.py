"""
魔法方法 04: 属性访问控制与描述符
====================================

面试高频问题:
1. __getattr__ 和 __getattribute__ 的区别？
2. 什么是描述符？有哪些类型？
3. property 的本质是什么？

核心要点:
- __getattr__: 属性不存在时调用（兜底）
- __getattribute__: 每次访问属性时都调用（拦截所有访问）
- 描述符: 实现了 __get__/__set__/__delete__ 的对象
- property 是描述符的语法糖
"""


# ============================================================
# 1. __getattr__ vs __getattribute__
# ============================================================
# 面试官问: __getattr__ 和 __getattribute__ 有什么区别？
#
# 标准答:
# - __getattr__: 只在属性不存在时调用（最后的兜底）
# - __getattribute__: 每次访问属性时都会调用（拦截所有访问）
#
# 属性查找顺序:
# 1. 类的 __getattribute__（默认实现会按下面顺序查找）
# 2. 数据描述符（实现了 __get__ 和 __set__）
# 3. 实例的 __dict__
# 4. 非数据描述符（只实现了 __get__）
# 5. 类的 __dict__
# 6. 类的 __getattr__
#
# 使用场景:
# - __getattr__: 动态属性、代理模式、兼容旧 API
# - __getattribute__: 日志记录、访问控制、缓存
# ============================================================

class Config:
    """
    动态配置类 - 演示 __getattr__

    特点:
        1. 支持默认值（通过 default 参数）
        2. 支持嵌套访问（config.a.b.c）
        3. 属性不存在时不报错，返回 None

    运行结果:
        config.debug: True
        config.host: localhost
        config.not_exist: None
        config.nested.x.y: NestedValue
    """

    def __init__(self, defaults=None, **kwargs):
        # 用 object.__setattr__ 避免触发 __setattr__
        object.__setattr__(self, '_data', kwargs)
        object.__setattr__(self, '_defaults', defaults or {})

    def __getattr__(self, name):
        """
        属性不存在时调用

        调用时机:
            当正常查找（实例 __dict__ → 类 __dict__）找不到属性时

        注意:
            这里不能用 self.xxx，会无限递归！
            要用 object.__getattribute__ 或 self.__dict__
        """
        # 先在 _data 中查找
        if name in self._data:
            return self._data[name]
        # 再在 _defaults 中查找
        if name in self._defaults:
            return self._defaults[name]
        # 返回一个嵌套 Config（支持 config.a.b.c）
        return Config()

    def __setattr__(self, name, value):
        """
        设置属性时调用

        注意:
            如果在 __init__ 中用 self.xxx = value，会触发这里
            所以 __init__ 中要用 object.__setattr__
        """
        self._data[name] = value

    def __delattr__(self, name):
        """删除属性时调用"""
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(name)

    def __contains__(self, key):
        """支持 key in config"""
        return key in self._data or key in self._defaults

    def __repr__(self):
        return f"Config({self._data})"


class LoggedAttribute:
    """
    用 __getattribute__ 记录属性访问

    运行结果:
        访问属性: name
        访问属性: age
        访问日志: ['name', 'age']
    """

    def __init__(self):
        self.name = "Alice"
        self.age = 30
        self._access_log = []

    def __getattribute__(self, name):
        """
        每次访问属性时调用

        警告:
            容易造成无限递归！
            不能在这里访问 self.xxx（除非用 object.__getattribute__）
        """
        # 记录访问（用 object.__getattribute__ 避免递归）
        log = object.__getattribute__(self, '_access_log')
        log.append(name)

        # 正常返回属性值
        return object.__getattribute__(self, name)


# ============================================================
# 2. 描述符协议
# ============================================================
# 面试官问: 什么是描述符？有哪些类型？
#
# 标准答:
# 描述符是实现了 __get__、__set__、__delete__ 中至少一个方法的对象。
#
# 两种类型:
# - 数据描述符: 同时实现了 __get__ 和 __set__（优先级高于实例 __dict__）
# - 非数据描述符: 只实现了 __get__（优先级低于实例 __dict__）
#
# 描述符的应用:
# - property、classmethod、staticmethod 都是描述符
# - Django 的 Model 字段
# - 类型检查、验证、延迟计算
# ============================================================

class Validated:
    """
    验证描述符 - 自动验证属性值

    用法:
        class Person:
            age = Validated(min_val=0, max_val=150)
            name = Validated(min_len=1)

        p = Person()
        p.age = 25    # OK
        p.age = -5    # 抛出 ValueError

    运行结果:
        Person(name='Alice', age=30)
        验证失败: age: 值必须在 0-150 之间 (got -5)
    """

    def __init__(self, validator=None, error_msg="Invalid value",
                 min_val=None, max_val=None, min_len=None):
        self.validator = validator
        self.error_msg = error_msg
        self.min_val = min_val
        self.max_val = max_val
        self.min_len = min_len

    def __set_name__(self, owner, name):
        """
        描述符被赋给类属性时自动调用

        参数:
            owner: 拥有这个描述符的类
            name: 描述符的属性名

        作用:
            让描述符知道自己叫什么名字（用于错误提示）
        """
        self.name = name

    def __get__(self, obj, objtype=None):
        """
        访问属性时调用

        参数:
            obj: 实例（如果是类访问，为 None）
            objtype: 类

        返回:
            属性值
        """
        if obj is None:
            # 类访问（如 Person.age），返回描述符本身
            return self
        # 从实例的 __dict__ 中获取值
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        """
        设置属性时调用

        这里可以做验证：
        - 类型检查
        - 范围检查
        - 自定义验证逻辑
        """
        # 验证
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name}: 值必须 >= {self.min_val} (got {value})")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name}: 值必须在 {self.min_val}-{self.max_val} 之间 (got {value})")
        if self.min_len is not None and len(str(value)) < self.min_len:
            raise ValueError(f"{self.name}: 长度必须 >= {self.min_len}")

        # 存储到实例的 __dict__
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        """删除属性时调用"""
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]
        else:
            raise AttributeError(f"{self.name} not set")


class Person:
    """使用描述符验证的 Person 类"""

    name = Validated(min_len=1, error_msg="名字不能为空")
    age = Validated(min_val=0, max_val=150, error_msg="年龄必须在 0-150 之间")

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


# ============================================================
# 3. property 的本质（描述符）
# ============================================================
# 面试官问: property 和描述符有什么关系？
#
# 标准答:
# property 本质上就是一个数据描述符的语法糖。
#
# @property 等价于:
#   class property:
#       def __get__(self, obj, objtype): ...
#       def __set__(self, obj, value): ...
#       def __delete__(self, obj): ...
#
# 所以 @property 的优先级高于实例 __dict__
# ============================================================

class Circle:
    """
    用 property 实现属性验证

    运行结果:
        Circle(radius=5)
        面积: 78.54
        修改半径: Circle(radius=10)
        验证失败: Radius must be positive
    """

    def __init__(self, radius):
        self._radius = radius  # 存储在私有属性中

    @property
    def radius(self):
        """
        getter: 访问 circle.radius 时调用

        等价于:
            radius = property(fget=get_radius)
        """
        return self._radius

    @radius.setter
    def radius(self, value):
        """
        setter: 设置 circle.radius = value 时调用

        等价于:
            radius = property(fget=get_radius, fset=set_radius)
        """
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @radius.deleter
    def radius(self):
        """
        deleter: 删除 circle.radius 时调用
        """
        raise AttributeError("Cannot delete radius")

    @property
    def area(self):
        """
        只读属性（没有 setter）

        计算属性：每次访问时实时计算
        """
        import math
        return math.pi * self._radius ** 2

    def __repr__(self):
        return f"Circle(radius={self._radius})"


# ============================================================
# 主函数
# ============================================================

def demo_attribute_access():
    """演示属性访问控制"""
    print("=" * 60)
    print("1. __getattr__ vs __getattribute__")
    print("=" * 60)

    # Config
    config = Config(debug=True, host="localhost")
    print(f"config.debug: {config.debug}")
    print(f"config.host: {config.host}")
    print(f"config.not_exist: {config.not_exist}")  # None

    # 嵌套访问
    config.nested = Config(x=Config(y="NestedValue"))
    print(f"config.nested.x.y: {config.nested.x.y}")

    # LoggedAttribute
    print("\nLoggedAttribute:")
    obj = LoggedAttribute()
    print(f"name: {obj.name}")
    print(f"age: {obj.age}")
    print(f"访问日志: {obj._access_log}")
    print()


def demo_descriptor():
    """演示描述符"""
    print("=" * 60)
    print("2. 描述符")
    print("=" * 60)

    p = Person("Alice", 30)
    print(p)

    try:
        p.age = -5
    except ValueError as e:
        print(f"验证失败: {e}")
    print()


def demo_property():
    """演示 property"""
    print("=" * 60)
    print("3. property")
    print("=" * 60)

    c = Circle(5)
    print(c)
    print(f"面积: {c.area:.2f}")

    c.radius = 10
    print(f"修改半径: {c}")

    try:
        c.radius = -1
    except ValueError as e:
        print(f"验证失败: {e}")
    print()


if __name__ == "__main__":
    demo_attribute_access()
    demo_descriptor()
    demo_property()
