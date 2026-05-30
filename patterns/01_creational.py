"""
设计模式 01: 创建型模式
=========================

面试高频问题:
1. 单例模式有哪些实现方式？
2. 工厂模式和抽象工厂的区别？
3. Python 中哪些地方用到了设计模式？

核心要点:
- 单例模式: 确保只有一个实例
- 工厂模式: 根据参数创建不同类型的对象
- 建造者模式: 分步构建复杂对象
"""


# ============================================================
# 1. 单例模式 - 多种实现
# ============================================================
# 面试官问: Python 怎么实现单例模式？
#
# 标准答:
# 1. __new__ 方法（最常见）
# 2. 装饰器
# 3. 模块级变量（Python 模块天然单例）
# 4. metaclass
#
# 推荐: 装饰器或模块级变量（最 Pythonic）
# ============================================================

# 方式 1: __new__ 方法
class SingletonNew:
    """用 __new__ 实现单例"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


# 方式 2: 装饰器
def singleton(cls):
    """用装饰器实现单例"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class SingletonDecorator:
    def __init__(self, value=None):
        self.value = value


# 方式 3: 模块级变量（推荐）
# 在模块中直接创建实例
# config.py:
#   class _Config:
#       ...
#   config = _Config()
#
# 其他文件:
#   from config import config


# ============================================================
# 2. 工厂模式
# ============================================================
# 面试官问: 工厂模式有什么用？
#
# 标准答:
# 工厂模式将对象的创建和使用分离：
# - 调用者不需要知道具体类名
# - 只需要告诉工厂要什么，工厂返回对应的对象
# - 新增类型时只需要修改工厂，不需要修改调用者
#
# 使用场景:
# - 根据配置创建不同的数据库连接
# - 根据文件类型创建不同的解析器
# - 根据用户输入创建不同的图形
# ============================================================

class Shape:
    """图形基类"""
    def draw(self):
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        return f"Drawing Circle(radius={self.radius})"

    def __repr__(self):
        return f"Circle({self.radius})"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self):
        return f"Drawing Rectangle({self.width}x{self.height})"

    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"


class ShapeFactory:
    """
    图形工厂

    用法:
        factory = ShapeFactory()
        circle = factory.create("circle", radius=5)
        rect = factory.create("rectangle", width=3, height=4)
    """

    # 注册表：类型名 → 类
    _registry = {
        "circle": Circle,
        "rectangle": Rectangle,
    }

    @classmethod
    def create(cls, shape_type, **kwargs):
        """根据类型创建图形"""
        shape_class = cls._registry.get(shape_type)
        if shape_class is None:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return shape_class(**kwargs)

    @classmethod
    def register(cls, name, shape_class):
        """注册新的图形类型"""
        cls._registry[name] = shape_class


# ============================================================
# 3. 建造者模式
# ============================================================
# 面试官问: 建造者模式什么时候用？
#
# 标准答:
# 当对象有很多可选参数时，用建造者模式：
# - 链式调用，代码可读性好
# - 可以分步构建
# - 可以创建不同配置的对象
#
# Python 中的替代方案:
# - dataclass with defaults
# - **kwargs
# ============================================================

class QueryBuilder:
    """
    SQL 查询构建器

    用法:
        query = (QueryBuilder()
            .select("name", "age")
            .from_table("users")
            .where("age > 18")
            .order_by("name")
            .limit(10)
            .build())
    """

    def __init__(self):
        self._select = "*"
        self._from = ""
        self._where = []
        self._order_by = ""
        self._limit = None

    def select(self, *columns):
        self._select = ", ".join(columns)
        return self  # 返回 self 支持链式调用

    def from_table(self, table):
        self._from = table
        return self

    def where(self, condition):
        self._where.append(condition)
        return self

    def order_by(self, column):
        self._order_by = column
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        """构建 SQL 查询"""
        parts = [f"SELECT {self._select}"]
        parts.append(f"FROM {self._from}")
        if self._where:
            parts.append(f"WHERE {' AND '.join(self._where)}")
        if self._order_by:
            parts.append(f"ORDER BY {self._order_by}")
        if self._limit:
            parts.append(f"LIMIT {self._limit}")
        return " ".join(parts)


# ============================================================
# 4. 原型模式
# ============================================================
# 面试官问: 什么是原型模式？
#
# 标准答:
# 通过复制现有对象来创建新对象，而不是 new 一个。
#
# Python 实现:
# - copy.copy(): 浅拷贝
# - copy.deepcopy(): 深拷贝
# - 实现 __copy__ 和 __deepcopy__ 方法
# ============================================================

import copy


class Prototype:
    """原型模式基类"""

    def clone(self):
        """浅拷贝"""
        return copy.copy(self)

    def deep_clone(self):
        """深拷贝"""
        return copy.deepcopy(self)


class Config(Prototype):
    """配置对象（演示原型模式）"""

    def __init__(self, host, port, options=None):
        self.host = host
        self.port = port
        self.options = options or {}

    def __repr__(self):
        return f"Config(host='{self.host}', port={self.port}, options={self.options})"


# ============================================================
# 主函数
# ============================================================

def demo_singleton():
    """演示单例模式"""
    print("=" * 60)
    print("1. 单例模式")
    print("=" * 60)

    # __new__ 方式
    s1 = SingletonNew("first")
    s2 = SingletonNew("second")
    print(f"SingletonNew: s1 is s2 = {s1 is s2}")
    print(f"s1.value = {s1.value}")  # first

    # 装饰器方式
    s3 = SingletonDecorator("hello")
    s4 = SingletonDecorator("world")
    print(f"\nSingletonDecorator: s3 is s4 = {s3 is s4}")
    print(f"s3.value = {s3.value}")  # hello
    print()


def demo_factory():
    """演示工厂模式"""
    print("=" * 60)
    print("2. 工厂模式")
    print("=" * 60)

    factory = ShapeFactory()

    circle = factory.create("circle", radius=5)
    rect = factory.create("rectangle", width=3, height=4)

    print(circle.draw())
    print(rect.draw())
    print()


def demo_builder():
    """演示建造者模式"""
    print("=" * 60)
    print("3. 建造者模式")
    print("=" * 60)

    query = (QueryBuilder()
        .select("name", "age")
        .from_table("users")
        .where("age > 18")
        .where("status = 'active'")
        .order_by("name")
        .limit(10)
        .build())

    print(f"查询: {query}")
    print()


def demo_prototype():
    """演示原型模式"""
    print("=" * 60)
    print("4. 原型模式")
    print("=" * 60)

    # 原始配置
    original = Config("localhost", 8080, {"debug": True})

    # 浅拷贝
    shallow = original.clone()
    shallow.host = "192.168.1.1"

    # 深拷贝
    deep = original.deep_clone()
    deep.options["debug"] = False

    print(f"原始: {original}")
    print(f"浅拷贝: {shallow}")
    print(f"深拷贝: {deep}")
    print(f"\n原始.options['debug'] = {original.options['debug']}")  # False（浅拷贝共享引用）
    print()


if __name__ == "__main__":
    demo_singleton()
    demo_factory()
    demo_builder()
    demo_prototype()
