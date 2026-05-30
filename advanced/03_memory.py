"""
进阶 03: 内存管理与垃圾回收
==============================

面试高频问题:
1. Python 的内存管理机制是什么？
2. 引用计数和垃圾回收的关系？
3. __slots__ 有什么用？

核心要点:
- 引用计数: 主要的内存管理机制
- 垃圾回收: 处理循环引用（分代收集）
- 内存池: 小对象使用内存池（pymalloc）
- __slots__: 减少内存占用
"""


import sys
import gc
import weakref
import tracemalloc
from pympler import asizeof  # 需要安装: pip install pympler


# ============================================================
# 1. 引用计数
# ============================================================
# 面试官问: Python 怎么知道什么时候释放对象？
#
# 标准答:
# Python 使用引用计数作为主要的内存管理机制：
# - 每个对象都有一个引用计数器
# - 当引用计数变为 0 时，对象立即被释放
# - 优点: 实时性好，不会延迟释放
# - 缺点: 无法处理循环引用
#
# 引用计数增加的情况:
# 1. 对象被创建: a = 1
# 2. 对象被引用: b = a
# 3. 对象作为参数: func(a)
# 4. 对象在容器中: list.append(a)
#
# 引用计数减少的情况:
# 1. 变量被重新赋值: a = 2
# 2. 变量被删除: del a
# 3. 对象离开作用域
# 4. 容器被清空
# ============================================================

def demo_reference_count():
    """演示引用计数"""
    print("=" * 60)
    print("1. 引用计数")
    print("=" * 60)

    # 创建对象
    a = [1, 2, 3]
    print(f"初始引用计数: {sys.getrefcount(a)}")  # 2（a + getrefcount 参数）

    # 增加引用
    b = a
    print(f"b = a 后: {sys.getrefcount(a)}")  # 3

    # 在容器中
    c = [a]
    print(f"在列表中: {sys.getrefcount(a)}")  # 4

    # 减少引用
    del b
    print(f"del b 后: {sys.getrefcount(a)}")  # 3

    c.pop()
    print(f"从列表移除: {sys.getrefcount(a)}")  # 2

    # 查看对象大小
    print(f"\na 的大小: {sys.getsizeof(a)} bytes")
    print(f"a 的实际大小: {asizeof.asizeof(a)} bytes")
    print()


# ============================================================
# 2. 循环引用与垃圾回收
# ============================================================
# 面试官问: 什么是循环引用？怎么处理？
#
# 标准答:
# 循环引用是指对象之间互相引用，导致引用计数永远不为 0：
#
#   a -> b -> a
#
# 即使没有外部引用，a 和 b 的引用计数都是 1，
# 引用计数无法释放它们。
#
# 解决方案: 垃圾回收器（GC）
# - 使用分代收集算法（3 代）
# - 定期检测循环引用
# - 可以手动触发: gc.collect()
#
# GC 的工作方式:
# 1. 新创建的对象在第 0 代
# 2. 每次 GC 后存活的对象会升级到下一代
# 3. 第 0 代 GC 最频繁，第 2 代最少
# ============================================================

def demo_circular_reference():
    """演示循环引用"""
    print("=" * 60)
    print("2. 循环引用与垃圾回收")
    print("=" * 60)

    # 禁用自动 GC，手动控制
    gc.disable()

    # 创建循环引用
    class Node:
        def __init__(self, name):
            self.name = name
            self.parent = None
            self.children = []

        def add_child(self, child):
            child.parent = self  # 循环引用！
            self.children.append(child)

        def __del__(self):
            print(f"  释放 {self.name}")

    # 创建循环引用
    parent = Node("parent")
    child = Node("child")
    parent.add_child(child)

    print(f"GC 统计: {gc.get_stats()}")
    print(f"未收集的垃圾: {gc.collect()}")

    # 删除外部引用
    del parent
    del child

    # 此时对象还在内存中（循环引用）
    print(f"删除后未收集: {gc.collect()}")

    # 手动触发 GC
    gc.enable()
    collected = gc.collect()
    print(f"手动 GC 后收集: {collected} 个对象")
    print()


# ============================================================
# 3. __slots__ — 减少内存占用
# ============================================================
# 面试官问: __slots__ 有什么用？
#
# 标准答:
# __slots__ 可以限制实例的属性，并减少内存占用：
#
# 普通类:
# - 每个实例有一个 __dict__ 字典存储属性
# - 字典有额外的内存开销（哈希表）
#
# 使用 __slots__:
# - 没有 __dict__，属性直接存储在实例中
# - 内存占用减少 30%-50%
# - 属性访问更快
#
# 限制:
# - 不能动态添加未声明的属性
# - 不能使用 __weakref__（除非显式声明）
# - 继承时需要注意
#
# 使用场景:
# - 创建大量实例（如数据点、坐标）
# - 内存敏感的场景
# ============================================================

class RegularPoint:
    """普通类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SlottedPoint:
    """使用 __slots__ 的类"""
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y


def demo_slots():
    """演示 __slots__"""
    print("=" * 60)
    print("3. __slots__ — 减少内存占用")
    print("=" * 60)

    # 创建实例
    regular = RegularPoint(1, 2)
    slotted = SlottedPoint(1, 2)

    # 内存对比
    print(f"普通类大小: {sys.getsizeof(regular)} bytes")
    print(f"__slots__ 大小: {sys.getsizeof(slotted)} bytes")

    # 批量创建对比
    n = 100000
    regular_list = [RegularPoint(i, i) for i in range(n)]
    slotted_list = [SlottedPoint(i, i) for i in range(n)]

    regular_mem = sum(sys.getsizeof(p) for p in regular_list)
    slotted_mem = sum(sys.getsizeof(p) for p in slotted_list)

    print(f"\n创建 {n} 个实例:")
    print(f"普通类内存: {regular_mem / 1024 / 1024:.2f} MB")
    print(f"__slots__ 内存: {slotted_mem / 1024 / 1024:.2f} MB")
    print(f"节省: {(1 - slotted_mem / regular_mem) * 100:.1f}%")

    # 限制
    print(f"\n普通类可以动态添加属性:")
    regular.z = 3  # OK

    print(f"__slots__ 不能动态添加属性:")
    try:
        slotted.z = 3
    except AttributeError as e:
        print(f"  错误: {e}")
    print()


# ============================================================
# 4. weakref — 弱引用
# ============================================================
# 面试官问: 什么是弱引用？有什么用？
#
# 标准答:
# 弱引用不会增加对象的引用计数：
# - 当对象只有弱引用时，可以被垃圾回收
# - 常用于缓存、观察者模式
#
# 使用场景:
# 1. 缓存: 避免缓存阻止对象被回收
# 2. 观察者模式: 避免观察者阻止被观察对象回收
# 3. 大型对象: 避免内存泄漏
#
# 注意:
# - 不是所有对象都支持弱引用（如 int, str, list）
# - 需要导入 weakref 模块
# ============================================================

def demo_weakref():
    """演示弱引用"""
    print("=" * 60)
    print("4. weakref — 弱引用")
    print("=" * 60)

    class HeavyObject:
        def __init__(self, name):
            self.name = name
            print(f"  创建 {name}")

        def __del__(self):
            print(f"  释放 {self.name}")

    # 创建对象
    obj = HeavyObject("heavy_data")

    # 创建弱引用
    ref = weakref.ref(obj)
    print(f"弱引用: {ref}")
    print(f"通过弱引用访问: {ref().name}")

    # 删除强引用
    print("\n删除强引用:")
    del obj

    # 弱引用变为 None
    print(f"弱引用: {ref}")
    print(f"通过弱引用访问: {ref()}")  # None

    # 弱引用用于缓存
    print("\n弱引用缓存示例:")
    cache = weakref.WeakValueDictionary()

    class Data:
        def __init__(self, value):
            self.value = value

    cache['key'] = Data(42)
    print(f"缓存: {cache['key'].value}")

    # 当对象被回收时，自动从缓存中移除
    del cache['key']
    print(f"删除后: {cache.get('key')}")  # None
    print()


# ============================================================
# 5. 内存分析工具
# ============================================================
# 面试官问: 怎么分析 Python 程序的内存使用？
#
# 标准答:
# 1. sys.getsizeof(): 查看单个对象的大小
# 2. tracemalloc: 追踪内存分配
# 3. memory_profiler: 逐行分析内存
# 4. objgraph: 可视化对象引用
# 5. pympler: 详细的内存分析
# ============================================================

def demo_memory_tools():
    """演示内存分析工具"""
    print("=" * 60)
    print("5. 内存分析工具")
    print("=" * 60)

    # tracemalloc
    print("\ntracemalloc 示例:")
    tracemalloc.start()

    # 分配一些内存
    data = [list(range(1000)) for _ in range(100)]

    # 快照
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("  前 3 个内存分配:")
    for stat in top_stats[:3]:
        print(f"    {stat}")

    tracemalloc.stop()

    # 常见对象大小
    print("\n常见对象大小:")
    objects = [
        ("int(0)", 0),
        ("int(2**30)", 2**30),
        ("float(0.0)", 0.0),
        ("str('')", ""),
        ("str('hello')", "hello"),
        ("list([])", []),
        ("list(range(10))", list(range(10))),
        ("dict({})", {}),
        ("tuple(())", ()),
        ("set()", set()),
    ]

    for name, obj in objects:
        print(f"  {name:20} → {sys.getsizeof(obj)} bytes")
    print()


# ============================================================
# 6. 内存优化技巧
# ============================================================
# 面试官问: 怎么优化 Python 程序的内存？
#
# 标准答:
# 1. 使用 __slots__
# 2. 使用生成器而不是列表
# 3. 使用 weakref 做缓存
# 4. 及时释放大对象（del + gc.collect()）
# 5. 使用 __del__ 或上下文管理器管理资源
# 6. 避免循环引用
# 7. 使用 numpy 数组存储数值数据
# ============================================================

def demo_optimization_tips():
    """内存优化技巧"""
    print("=" * 60)
    print("6. 内存优化技巧")
    print("=" * 60)

    print("""
    1. __slots__: 减少实例内存
       class Point:
           __slots__ = ['x', 'y']

    2. 生成器: 惰性求值
       # 不好: 创建完整列表
       data = [x**2 for x in range(1000000)]
       # 好: 使用生成器
       data = (x**2 for x in range(1000000))

    3. weakref: 缓存不阻止回收
       cache = weakref.WeakValueDictionary()

    4. 及时释放: del + gc.collect()
       del big_object
       gc.collect()

    5. 上下文管理器: 确保资源释放
       with open('file') as f:
           data = f.read()

    6. numpy: 高效数值存储
       import numpy as np
       arr = np.zeros(1000000)  # 8MB vs Python list 36MB

    7. 避免嵌套: 扁平数据结构
       # 不好: 嵌套字典
       data = {'a': {'b': {'c': 1}}}
       # 好: 扁平化
       data = {'a.b.c': 1}
    """)
    print()


# ============================================================
# 主函数
# ============================================================

def main():
    demo_reference_count()
    demo_circular_reference()
    demo_slots()
    demo_weakref()
    demo_memory_tools()
    demo_optimization_tips()


if __name__ == "__main__":
    main()
