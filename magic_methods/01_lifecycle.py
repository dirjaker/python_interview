"""
魔法方法 01: 对象生命周期
============================

面试高频问题:
1. __new__ 和 __init__ 的区别是什么？
2. 什么时候需要重写 __new__？
3. Python 的单例模式怎么实现？

核心要点:
- __new__: 创建实例（构造器），是静态方法，第一个参数是 cls
- __init__: 初始化实例，是实例方法，第一个参数是 self
- __del__: 销毁实例时调用（不推荐依赖它做清理）

调用顺序: __new__ → __init__ → ... 使用对象 ... → __del__
"""

import gc


# ============================================================
# 1. __new__ vs __init__ 的区别
# ============================================================
# 面试官问: __new__ 和 __init__ 有什么区别？
#
# 标准答:
# - __new__ 负责创建实例，返回一个新的对象（必须返回实例）
# - __init__ 负责初始化实例，不返回任何值（返回 None）
# - __new__ 是类方法（虽然没加 @classmethod），__init__ 是实例方法
# - __new__ 先于 __init__ 被调用
# - 通常不需要重写 __new__，除非你要控制实例创建过程（如单例、不可变类型）
# ============================================================

class LifecycleDemo:
    """
    演示对象从创建到销毁的完整生命周期

    运行结果:
        __new__ 创建实例: LifecycleDemo    # 先创建
        __init__ 初始化实例: 42            # 再初始化
        __del__ 销毁实例: 42               # 最后销毁
    """

    def __new__(cls, *args, **kwargs):
        """
        创建实例 - 在 __init__ 之前调用

        参数:
            cls: 类本身（不是实例）
            *args, **kwargs: 传递给构造函数的参数

        返回:
            必须返回 super().__new__(cls) 创建的实例

        使用场景:
            1. 单例模式（控制只创建一个实例）
            2. 不可变类型（如 tuple, str 的子类，需要在 __new__ 中设置值）
            3. 返回不同的类实例（工厂模式）
        """
        print(f"__new__ 创建实例: {cls.__name__}")
        # 调用父类的 __new__ 来创建实例
        instance = super().__new__(cls)
        return instance  # 必须返回实例！

    def __init__(self, value):
        """
        初始化实例 - 在 __new__ 之后调用

        参数:
            self: __new__ 创建好的实例
            value: 用户传入的初始化值

        注意:
            这里不能返回任何值，只能设置属性
        """
        print(f"__init__ 初始化实例: {value}")
        self.value = value

    def __del__(self):
        """
        销毁实例 - 引用计数为 0 时调用

        注意:
            1. 不推荐依赖 __del__ 做资源清理（调用时机不确定）
            2. 推荐用上下文管理器（with 语句）来管理资源
            3. 循环引用时 __del__ 可能不被调用
        """
        print(f"__del__ 销毁实例: {self.value}")


# ============================================================
# 2. 单例模式 - __new__ 最常见的应用
# ============================================================
# 面试官问: Python 怎么实现单例模式？
#
# 标准答:
# 1. 重写 __new__，用类变量缓存实例
# 2. 用装饰器实现
# 3. 用模块级变量（Python 模块天然单例）
# 4. 用 metaclass
# ============================================================

class Singleton:
    """
    单例模式实现

    核心思想:
        重写 __new__，第一次调用时创建实例并缓存，
        之后每次调用都返回同一个实例

    运行结果:
        创建新实例
        返回已有实例
        s1 is s2: True    # 两个变量指向同一个对象
        s1.value: first   # 第二次创建不会覆盖 __init__ 的值
    """

    # 类变量：缓存实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        控制实例创建：只创建一次

        第一次调用: cls._instance is None → 创建新实例并缓存
        之后调用: cls._instance 不是 None → 直接返回缓存的实例
        """
        if cls._instance is None:
            print("创建新实例")
            cls._instance = super().__new__(cls)
        else:
            print("返回已有实例")
        return cls._instance

    def __init__(self, value=None):
        """
        注意: 虽然 __new__ 返回的是同一个实例，
        但 __init__ 每次都会被调用！

        所以需要用 _initialized 标志来防止重复初始化
        """
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


# ============================================================
# 3. 更好的单例实现 - 用装饰器
# ============================================================

def singleton(cls):
    """
    装饰器版本的单例模式

    优点:
        1. 不需要修改类的代码
        2. 可以复用到任何类
        3. 更 Pythonic

    用法:
        @singleton
        class MyClass:
            pass
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DatabaseConnection:
    """用装饰器实现单例的数据库连接"""

    def __init__(self, host="localhost", port=3306):
        self.host = host
        self.port = port
        print(f"连接到数据库 {host}:{port}")


# ============================================================
# 4. 不可变类型 - 必须在 __new__ 中设置值
# ============================================================
# 面试官问: 为什么 str、tuple 这些不可变类型要重写 __new__？
#
# 标准答:
# 因为不可变类型的值在 __init__ 之前就已经确定了。
# 如果在 __init__ 中修改值，会违反不可变的语义。
# 所以必须在 __new__ 中（创建实例时）就设置好值。
# ============================================================

class ImmutablePoint:
    """
    不可变的点类

    为什么要在 __new__ 中设置值？
    因为我们要让 x, y 不可变（类似 tuple），
    如果在 __init__ 中设置，用户可以继承并覆盖 __init__ 来修改值
    """

    def __new__(cls, x, y):
        # 在创建实例时就设置值，确保不可变
        instance = super().__new__(cls)
        instance._x = x  # 用私有属性存储
        instance._y = y
        return instance

    def __init__(self, x, y):
        # __init__ 不设置值，因为 __new__ 已经设置了
        # 这样即使子类覆盖 __init__，值也不会被修改
        pass

    @property
    def x(self):
        """只读属性"""
        return self._x

    @property
    def y(self):
        """只读属性"""
        return self._y

    def __repr__(self):
        return f"ImmutablePoint(x={self.x}, y={self.y})"


# ============================================================
# 5. 工厂模式 - 用类方法实现
# ============================================================

class Shape:
    """
    图形基类 - 工厂模式

    用法:
        circle = Shape.create("circle", radius=5)
        rect = Shape.create("rectangle", width=3, height=4)
    """

    _registry = {}

    @classmethod
    def register(cls, shape_type, shape_class):
        """注册新的图形类型"""
        cls._registry[shape_type] = shape_class

    @classmethod
    def create(cls, shape_type, *args, **kwargs):
        """
        工厂方法：根据参数返回不同类型的实例

        这种模式在标准库中也有使用，
        比如 logging.getLogger() 就是工厂模式
        """
        shape_class = cls._registry.get(shape_type)
        if shape_class is None:
            raise ValueError(f"Unknown shape: {shape_type}")
        return shape_class(*args, **kwargs)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def __repr__(self):
        return f"Circle(radius={self.radius})"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


# 注册图形类型
Shape.register("circle", Circle)
Shape.register("rectangle", Rectangle)


# ============================================================
# 主函数：运行所有演示
# ============================================================

def demo_lifecycle():
    """演示对象生命周期"""
    print("=" * 60)
    print("1. 对象生命周期: __new__ → __init__ → __del__")
    print("=" * 60)

    # 创建对象
    obj = LifecycleDemo(42)
    # 删除引用，触发 __del__
    del obj

    # 强制垃圾回收（确保 __del__ 被调用）
    gc.collect()
    print()


def demo_singleton():
    """演示单例模式"""
    print("=" * 60)
    print("2. 单例模式")
    print("=" * 60)

    # 第一次创建
    s1 = Singleton("first")
    # 第二次创建（返回同一个实例）
    s2 = Singleton("second")

    print(f"s1 is s2: {s1 is s2}")       # True
    print(f"s1.value: {s1.value}")        # first（不会被覆盖）

    # 装饰器版本
    print("\n装饰器版本:")
    db1 = DatabaseConnection("192.168.1.1", 5432)
    db2 = DatabaseConnection("192.168.1.2", 3306)  # 不会创建新连接
    print(f"db1 is db2: {db1 is db2}")
    print()


def demo_immutable():
    """演示不可变类型"""
    print("=" * 60)
    print("3. 不可变类型")
    print("=" * 60)

    p = ImmutablePoint(3, 4)
    print(f"p = {p}")
    print(f"p.x = {p.x}, p.y = {p.y}")

    try:
        p.x = 10  # AttributeError: can't set attribute
    except AttributeError as e:
        print(f"修改失败: {e}")
    print()


def demo_factory():
    """演示工厂模式"""
    print("=" * 60)
    print("4. 工厂模式")
    print("=" * 60)

    # 通过 Shape 工厂创建不同类型的图形
    c = Shape.create("circle", 5)
    r = Shape.create("rectangle", 3, 4)

    print(f"c = {c}")
    print(f"r = {r}")
    print(f"type(c) = {type(c).__name__}")
    print(f"type(r) = {type(r).__name__}")
    print()


if __name__ == "__main__":
    demo_lifecycle()
    demo_singleton()
    demo_immutable()
    demo_factory()
