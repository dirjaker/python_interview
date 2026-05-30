"""
标准库 02: functools 模块
===========================

面试高频问题:
1. lru_cache 的原理是什么？
2. partial 有什么用？
3. reduce 和 sum 的区别？

核心要点:
- lru_cache: 带 LRU 策略的缓存装饰器
- partial: 偏函数，固定部分参数
- reduce: 累积计算
- total_ordering: 自动生成比较方法
"""


import functools
import time
import operator


# ============================================================
# 1. lru_cache - 缓存装饰器
# ============================================================
# 面试官问: lru_cache 的原理是什么？
#
# 标准答:
# lru_cache 是一个装饰器，会缓存函数的输入输出：
# - 相同输入直接返回缓存结果，不重新计算
# - LRU = Least Recently Used，缓存满时淘汰最久没用的
# - 用 dict 存储 {参数: 结果}，用双向链表维护访问顺序
#
# 适用场景:
# - 递归函数（如斐波那契、阶乘）
# - 计算密集型函数（相同输入总是相同输出）
# - IO 密集型函数（避免重复请求）
#
# 注意:
# - 参数必须是可哈希的（不能是 list, dict）
# - 缓存会占用内存
# - 如果函数有副作用，不适合用缓存
# ============================================================

def demo_lru_cache():
    """lru_cache 演示"""
    print("=" * 60)
    print("1. lru_cache - 缓存装饰器")
    print("=" * 60)

    @functools.lru_cache(maxsize=128)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # 第一次计算（需要递归）
    start = time.perf_counter()
    result = fibonacci(100)
    elapsed = time.perf_counter() - start
    print(f"fib(100) = {result}, 耗时: {elapsed:.6f}s")

    # 第二次计算（直接从缓存获取）
    start = time.perf_counter()
    result = fibonacci(100)
    elapsed = time.perf_counter() - start
    print(f"fib(100) = {result}, 耗时: {elapsed:.6f}s")

    # 查看缓存信息
    print(f"缓存信息: {fibonacci.cache_info()}")
    print(f"  hits: 命中次数")
    print(f"  misses: 未命中次数")
    print(f"  maxsize: 最大缓存数")
    print(f"  currsize: 当前缓存数")
    print()


# ============================================================
# 2. partial - 偏函数
# ============================================================
# 面试官问: partial 有什么用？
#
# 标准答:
# partial 固定函数的部分参数，创建一个新函数。
#
# 使用场景:
# - 简化函数调用（固定常用参数）
# - 回调函数（需要特定签名）
# - 函数式编程（组合函数）
# ============================================================

def demo_partial():
    """partial 演示"""
    print("=" * 60)
    print("2. partial - 偏函数")
    print("=" * 60)

    def power(base, exponent):
        return base ** exponent

    # 创建偏函数（固定 exponent）
    square = functools.partial(power, exponent=2)
    cube = functools.partial(power, exponent=3)

    print(f"square(5) = {square(5)}")  # 25
    print(f"cube(3) = {cube(3)}")      # 27

    # 实际应用：简化排序
    students = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35},
    ]

    # 用 partial 创建排序函数
    sort_by_age = functools.partial(sorted, key=lambda x: x["age"])
    print(f"\n按年龄排序: {sort_by_age(students)}")
    print()


# ============================================================
# 3. reduce - 累积计算
# ============================================================
# 面试官问: reduce 和 sum 有什么区别？
#
# 标准答:
# - sum: 只能求和，速度快（C 实现）
# - reduce: 通用累积操作，更灵活
#
# 使用场景:
# - 求和 → sum
# - 求积 → reduce(operator.mul, ...)
# - 合并字典 → reduce(or, ...)
# - 链式操作 → reduce
# ============================================================

def demo_reduce():
    """reduce 演示"""
    print("=" * 60)
    print("3. reduce - 累积计算")
    print("=" * 60)

    # 求和
    data = [1, 2, 3, 4, 5]
    result = functools.reduce(lambda x, y: x + y, data)
    print(f"求和: {result}")  # 15

    # 求积
    result = functools.reduce(operator.mul, data)
    print(f"求积: {result}")  # 120

    # 找最大值
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    result = functools.reduce(max, data)
    print(f"最大值: {result}")

    # 合并字典
    dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
    merged = functools.reduce(lambda x, y: {**x, **y}, dicts)
    print(f"合并字典: {merged}")
    print()


# ============================================================
# 4. total_ordering - 自动生成比较方法
# ============================================================
# 面试官问: total_ordering 是什么？
#
# 标准答:
# @total_ordering 装饰器会根据 __eq__ 和 __lt__（或 __gt__）
# 自动生成其他比较方法：__le__, __gt__, __ge__
#
# 注意:
# - 只需要实现 __eq__ 和 __lt__
# - Python 3.2+ 可用
# - 有性能开销（生成的方法比手写的慢）
# ============================================================

def demo_total_ordering():
    """total_ordering 演示"""
    print("=" * 60)
    print("4. total_ordering")
    print("=" * 60)

    @functools.total_ordering
    class Student:
        def __init__(self, name, grade):
            self.name = name
            self.grade = grade

        def __eq__(self, other):
            return self.grade == other.grade

        def __lt__(self, other):
            return self.grade < other.grade

        def __repr__(self):
            return f"Student('{self.name}', {self.grade})"

    students = [
        Student("Alice", 90),
        Student("Bob", 85),
        Student("Charlie", 90),
    ]

    print(f"排序: {sorted(students)}")
    print(f"Alice >= Bob: {students[0] >= students[1]}")  # 自动生成
    print(f"Alice <= Charlie: {students[0] <= students[2]}")
    print()


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    demo_lru_cache()
    demo_partial()
    demo_reduce()
    demo_total_ordering()
