"""
进阶 02: 元类 (Metaclass)
===========================

面试高频问题:
1. 什么是元类？类和对象的关系是什么？
2. type 和 object 的关系是什么？
3. __new__ 和 __init_subclass__ 的区别？

核心要点:
- 元类是创建类的类（类是元类的实例）
- type 是所有类的元类
- object 是所有类的基类
- 元类可以拦截类的创建过程
"""


# ============================================================
# 1. 类也是对象
# ============================================================
# 面试官问: Python 中类是什么？
#
# 标准答:
# 在 Python 中，类也是对象：
# - 类是 type 的实例
# - 类可以被赋值、传递、作为参数
# - 类可以有属性
# - 类可以被创建（通过 type() 或 metaclass）
#
# 对比:
# - 对象 = 类()     → 创建实例
# - 类 = type()     → 创建类
# - type = type()   → type 是自己的实例
# ============================================================

def demo_class_is_object():
    """演示类也是对象"""
    print("=" * 60)
    print("1. 类也是对象")
    print("=" * 60)

    class Dog:
        species = "Canine"

        def bark(self):
            return "Woof!"

    # 类可以被赋值
    MyClass = Dog

    # 类可以作为参数
    def create_instance(cls):
        return cls()

    obj = create_instance(Dog)
    print(f"obj.bark() = {obj.bark()}")

    # 类可以有属性
    Dog.legs = 4
    print(f"Dog.legs = {Dog.legs}")

    # 类是 type 的实例
    print(f"type(Dog) = {type(Dog)}")
    print(f"isinstance(Dog, type) = {isinstance(Dog, type)}")
    print()


# ============================================================
# 2. type 和 object 的关系
# ============================================================
# 面试官问: type 和 object 有什么关系？
#
# 标准答:
# 这是 Python 中最令人困惑的关系：
#
# 1. object 是所有类的基类
#    - 所有类都继承自 object
#    - type 也继承自 object
#
# 2. type 是所有类的元类
#    - 所有类都是 type 的实例
#    - object 也是 type 的实例
#
# 3. 特殊关系:
#    - type 的类型是 type（自己是自己的实例）
#    - object 的类型是 type
#    - type 继承自 object
#
# 这形成了一个循环:
#   type → object → type → object → ...
# ============================================================

def demo_type_object():
    """演示 type 和 object 的关系"""
    print("=" * 60)
    print("2. type 和 object 的关系")
    print("=" * 60)

    # 类型关系
    print(f"type(object) = {type(object)}")      # <class 'type'>
    print(f"type(type) = {type(type)}")            # <class 'type'>
    print(f"isinstance(object, type) = {isinstance(object, type)}")  # True
    print(f"isinstance(type, object) = {isinstance(type, object)}")  # True

    # 继承关系
    print(f"type.__bases__ = {type.__bases__}")    # (<class 'object'>,)
    print(f"object.__bases__ = {object.__bases__}")  # ()

    # 结论
    print("\n关系图:")
    print("  type 是 object 的子类")
    print("  object 是 type 的实例")
    print("  type 是自己的实例")
    print()


# ============================================================
# 3. 用 type() 动态创建类
# ============================================================
# 面试官问: type() 除了查看类型，还有什么用？
#
# 标准答:
# type() 有两种用法:
# 1. type(obj) — 查看对象的类型
# 2. type(name, bases, dict) — 动态创建类
#
# 第二种用法是元类的基础:
#   MyClass = type('MyClass', (BaseClass,), {'attr': value})
#
# 等价于:
#   class MyClass(BaseClass):
#       attr = value
# ============================================================

def demo_dynamic_class():
    """演示动态创建类"""
    print("=" * 60)
    print("3. 用 type() 动态创建类")
    print("=" * 60)

    # 用 type() 创建类
    Dog = type('Dog', (object,), {
        'species': 'Canine',
        'bark': lambda self: 'Woof!',
    })

    dog = Dog()
    print(f"Dog = {Dog}")
    print(f"dog.bark() = {dog.bark()}")
    print(f"dog.species = {dog.species}")

    # 带 __init__ 的类
    def dog_init(self, name, age):
        self.name = name
        self.age = age

    Dog2 = type('Dog', (object,), {
        '__init__': dog_init,
        '__repr__': lambda self: f"Dog('{self.name}', {self.age})",
    })

    dog2 = Dog2("Buddy", 3)
    print(f"\ndog2 = {dog2}")
    print()


# ============================================================
# 4. 自定义元类
# ============================================================
# 面试官问: 什么时候需要自定义元类？
#
# 标准答:
# 元类可以拦截类的创建过程，用于:
# 1. 验证类的定义（如检查必须实现某些方法）
# 2. 自动修改类（如自动添加方法）
# 3. 注册类（如插件系统）
# 4. 单例模式
# 5. ORM（如 Django Model）
#
# 使用方式:
#   class MyClass(metaclass=MyMeta):
#       pass
#
# 元类方法:
#   __new__: 创建类（返回类对象）
#   __init__: 初始化类
#   __call__: 创建实例（当调用 MyClass() 时）
# ============================================================

class ValidationMeta(type):
    """
    验证元类 — 检查类是否正确定义

    功能:
    1. 检查是否有 __repr__ 方法
    2. 检查类名是否以大写字母开头
    """

    def __new__(mcs, name, bases, namespace):
        # 跳过基类检查
        if bases:  # 只检查子类，不检查基类本身
            # 检查类名
            if not name[0].isupper():
                raise ValueError(f"Class name '{name}' must start with uppercase")

            # 检查是否有 __repr__
            if '__repr__' not in namespace:
                print(f"  Warning: {name} 没有 __repr__ 方法")

        return super().__new__(mcs, name, bases, namespace)


class RegistrationMeta(type):
    """
    注册元类 — 自动注册所有子类

    功能:
    - 自动将子类注册到 _registry 字典
    - 可以通过名称获取类
    """

    _registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # 只注册子类
            mcs._registry[name] = cls
            print(f"  注册类: {name}")
        return cls

    @classmethod
    def get_class(mcs, name):
        return mcs._registry.get(name)

    @classmethod
    def list_classes(mcs):
        return list(mcs._registry.keys())


class SingletonMeta(type):
    """
    单例元类 — 确保只有一个实例

    用法:
        class MyClass(metaclass=SingletonMeta):
            pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ============================================================
# 5. 元类实战示例
# ============================================================

# 使用 ValidationMeta
class User(metaclass=ValidationMeta):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User('{self.name}')"


# 使用 RegistrationMeta
class Shape(metaclass=RegistrationMeta):
    pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height


# 使用 SingletonMeta
class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"
        print("  数据库连接初始化")


def demo_metaclass():
    """演示元类"""
    print("=" * 60)
    print("4. 自定义元类")
    print("=" * 60)

    # ValidationMeta
    print("\nValidationMeta:")
    user = User("Alice")
    print(f"  user = {user}")

    # RegistrationMeta
    print("\nRegistrationMeta:")
    print(f"  已注册的类: {RegistrationMeta.list_classes()}")

    # 动态获取类
    CircleClass = RegistrationMeta.get_class("Circle")
    c = CircleClass(5)
    print(f"  Circle(5).radius = {c.radius}")

    # SingletonMeta
    print("\nSingletonMeta:")
    db1 = Database()
    db2 = Database()
    print(f"  db1 is db2 = {db1 is db2}")
    print()


# ============================================================
# 6. __init_subclass__ — 更简单的方案
# ============================================================
# 面试官问: 除了元类，还有什么方式可以拦截子类创建？
#
# 标准答:
# Python 3.6+ 引入了 __init_subclass__，
# 可以在父类中拦截子类的创建，比元类更简单。
#
# 使用场景:
# - 注册子类
# - 验证子类
# - 自动配置
#
# 对比:
# - 元类: 更强大，但更复杂
# - __init_subclass__: 更简单，但功能有限
# ============================================================

class PluginBase:
    """插件基类 — 用 __init_subclass__ 自动注册"""

    _plugins = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        cls._plugins[name] = cls
        print(f"  注册插件: {name}")

    @classmethod
    def get_plugin(cls, name):
        return cls._plugins.get(name)

    @classmethod
    def list_plugins(cls):
        return list(cls._plugins.keys())


class JSONPlugin(PluginBase, plugin_name="json"):
    pass


class XMLPlugin(PluginBase, plugin_name="xml"):
    pass


class CSVPlugin(PluginBase):  # 用类名作为插件名
    pass


def demo_init_subclass():
    """演示 __init_subclass__"""
    print("=" * 60)
    print("5. __init_subclass__ — 更简单的方案")
    print("=" * 60)

    print(f"\n已注册的插件: {PluginBase.list_plugins()}")

    # 动态获取插件
    JSONClass = PluginBase.get_plugin("json")
    print(f"JSON 插件: {JSONClass}")
    print()


# ============================================================
# 7. 元类 vs __init_subclass__ 对比
# ============================================================

def demo_comparison():
    """对比元类和 __init_subclass__"""
    print("=" * 60)
    print("6. 元类 vs __init_subclass__")
    print("=" * 60)

    print("""
    ┌─────────────────┬─────────────────┬─────────────────┐
    │ 特性             │ 元类            │ __init_subclass__│
    ├─────────────────┼─────────────────┼─────────────────┤
    │ 适用版本         │ 所有版本        │ Python 3.6+     │
    │ 复杂度           │ 高              │ 低              │
    │ 拦截范围         │ 类的整个创建过程│ 子类创建后      │
    │ 修改类           │ 可以            │ 有限            │
    │ 控制实例创建     │ 可以 (__call__) │ 不可以          │
    │ 多个元类冲突     │ 需要解决        │ 不存在          │
    │ 可读性           │ 较差            │ 较好            │
    └─────────────────┴─────────────────┴─────────────────┘

    选择建议:
    1. 如果只需要注册/验证子类 → __init_subclass__
    2. 如果需要控制实例创建 → 元类
    3. 如果需要修改类的定义 → 元类
    4. 如果不确定 → 先用 __init_subclass__，不够再换元类
    """)
    print()


# ============================================================
# 主函数
# ============================================================

def main():
    demo_class_is_object()
    demo_type_object()
    demo_dynamic_class()
    demo_metaclass()
    demo_init_subclass()
    demo_comparison()


if __name__ == "__main__":
    main()
