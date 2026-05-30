"""
魔法方法 05: 迭代器协议
========================

面试高频问题:
1. 迭代器和可迭代对象的区别？
2. yield 和 return 的区别？
3. 生成器表达式和列表推导式的区别？

核心要点:
- 可迭代对象: 实现了 __iter__ 的对象（如 list, dict, str）
- 迭代器: 实现了 __iter__ 和 __next__ 的对象
- 生成器: 用 yield 的函数，自动实现迭代器协议
"""


# ============================================================
# 1. 迭代器 vs 可迭代对象
# ============================================================
# 面试官问: 迭代器和可迭代对象有什么区别？
#
# 标准答:
# | 特性       | 可迭代对象 (Iterable) | 迭代器 (Iterator) |
# |-----------|----------------------|-------------------|
# | 方法      | __iter__             | __iter__ + __next__|
# | 可重复迭代 | 是                   | 否（用完就没了）    |
# | 例子      | list, dict, str      | list_iter, map    |
#
# 关系:
# - 可迭代对象的 __iter__ 返回一个迭代器
# - 迭代器的 __iter__ 返回 self
# - for 循环的本质: 先调用 __iter__ 获取迭代器，再反复调用 __next__
# ============================================================

class Fibonacci:
    """
    斐波那契数列迭代器

    特点:
        1. 无限序列（可以一直生成）
        2. 惰性求值（用到才计算）
        3. 内存占用 O(1)

    运行结果:
        前 10 个: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        小于 100 的: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    """

    def __init__(self, max_count=None, max_value=None):
        """
        参数:
            max_count: 最多生成多少个（None 表示无限）
            max_value: 最大值（超过就停止）
        """
        self.max_count = max_count
        self.max_value = max_value

    def __iter__(self):
        """
        返回迭代器对象

        对于迭代器类，通常返回 self
        """
        self.count = 0
        self.a, self.b = 0, 1
        return self

    def __next__(self):
        """
        返回下一个值

        没有更多值时抛出 StopIteration（for 循环会捕获这个异常）
        """
        # 检查是否达到最大数量
        if self.max_count is not None and self.count >= self.max_count:
            raise StopIteration

        # 检查是否超过最大值
        if self.max_value is not None and self.a > self.max_value:
            raise StopIteration

        # 计算下一个值
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result


# ============================================================
# 2. 生成器函数 - 更简洁的迭代器
# ============================================================
# 面试官问: yield 和 return 有什么区别？
#
# 标准答:
# - return: 返回值并结束函数
# - yield: 返回值并暂停函数，下次调用从暂停处继续
#
# 生成器的特点:
# - 自动实现迭代器协议
# - 惰性求值，节省内存
# - 可以保存状态（局部变量）
#
# 使用场景:
# - 处理大数据集（逐行读取文件）
# - 无限序列（斐波那契、素数）
# - 管道式数据处理
# ============================================================

def fibonacci_generator(max_count=None):
    """
    用生成器实现斐波那契数列

    对比迭代器版本:
        - 代码更简洁（不需要 __iter__ 和 __next__）
        - 自动保存状态（不需要手动维护 self.a, self.b）
        - 更 Pythonic

    运行结果:
        前 10 个: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    a, b = 0, 1
    count = 0
    while max_count is None or count < max_count:
        yield a  # 返回值并暂停
        a, b = b, a + b  # 下次调用从这里继续
        count += 1


def read_large_file(file_path, chunk_size=8192):
    """
    用生成器逐块读取大文件

    优点:
        - 内存占用 O(chunk_size)，不管文件多大
        - 可以处理比内存还大的文件

    用法:
        for chunk in read_large_file("huge.log"):
            process(chunk)
    """
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


# ============================================================
# 3. 生成器表达式 vs 列表推导式
# ============================================================
# 面试官问: 生成器表达式和列表推导式有什么区别？
#
# 标准答:
# | 特性       | 列表推导式        | 生成器表达式       |
# |-----------|------------------|-------------------|
# | 语法      | [x for x in ...] | (x for x in ...) |
# | 返回类型   | list             | generator         |
# | 内存      | O(n) 立即生成     | O(1) 惰性求值     |
# | 速度      | 立即计算          | 按需计算          |
# | 重复使用   | 可以             | 不可以（用完没了） |
#
# 使用建议:
# - 数据量小 → 列表推导式
# - 数据量大 → 生成器表达式
# - 只用一次 → 生成器表达式
# - 需要多次遍历 → 列表推导式
# ============================================================

def demo_memory_comparison():
    """
    对比内存占用

    列表推导式: 创建一个包含 100 万个元素的 list
    生成器表达式: 只创建一个 generator 对象
    """
    import sys

    # 列表推导式：立即生成所有元素
    list_comp = [x ** 2 for x in range(1000000)]

    # 生成器表达式：惰性求值
    gen_exp = (x ** 2 for x in range(1000000))

    print(f"列表推导式内存: {sys.getsizeof(list_comp):,} bytes")
    print(f"生成器表达式内存: {sys.getsizeof(gen_exp):,} bytes")
    print(f"内存比: {sys.getsizeof(list_comp) / sys.getsizeof(gen_exp):.0f}x")


# ============================================================
# 4. yield from - 子生成器
# ============================================================
# 面试官问: yield from 是什么？有什么用？
#
# 标准答:
# yield from 用于将一个可迭代对象委托给子生成器。
#
# 主要用途:
# 1. 简化嵌套生成器
# 2. 实现协程的委托（async/await 的前身）
# 3. 链接多个可迭代对象
#
# 等价关系:
#   yield from iterable
# 等价于:
#   for item in iterable:
#       yield item
# ============================================================

def flatten(nested_list):
    """
    递归展平嵌套列表

    用 yield from 简化递归生成器

    运行结果:
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)  # 委托给子生成器
        else:
            yield item


def chain(*iterables):
    """
    链接多个可迭代对象

    类似 itertools.chain

    运行结果:
        [1, 2, 3, 'a', 'b', 'c', 10, 20]
    """
    for iterable in iterables:
        yield from iterable


# ============================================================
# 5. send() - 生成器的双向通信
# ============================================================
# 面试官问: 生成器的 send() 方法有什么用？
#
# 标准答:
# send() 可以向生成器发送值，这个值会成为 yield 表达式的返回值。
#
# 协程的本质:
# - yield 可以同时产出值和接收值
# - 这是 asyncio 的基础（协程 = 能接收值的生成器）
#
# 注意:
# - 第一次调用必须 send(None) 或 next()
# - send(value) 会恢复生成器，value 成为 yield 的返回值
# ============================================================

def accumulator():
    """
    累加器协程

    演示 send() 的双向通信

    运行结果:
        累加: 10
        累加: 25
        累加: 28
        最终结果: 28
    """
    total = 0
    while True:
        value = yield total  # yield 当前总和，并接收新值
        if value is None:
            break
        total += value
        print(f"累加: {total}")
    return total


# ============================================================
# 主函数
# ============================================================

def demo_iterator():
    """演示迭代器"""
    print("=" * 60)
    print("1. 迭代器 vs 可迭代对象")
    print("=" * 60)

    # 斐波那契迭代器
    fib = Fibonacci(max_count=10)
    print(f"前 10 个: {list(fib)}")

    # 无限序列 + 条件停止
    fib2 = Fibonacci(max_value=100)
    print(f"小于 100 的: {list(fib2)}")
    print()


def demo_generator():
    """演示生成器"""
    print("=" * 60)
    print("2. 生成器函数")
    print("=" * 60)

    # 生成器版本
    fib_gen = fibonacci_generator(max_count=10)
    print(f"生成器前 10 个: {list(fib_gen)}")

    # 内存对比
    print("\n内存对比:")
    demo_memory_comparison()
    print()


def demo_yield_from():
    """演示 yield from"""
    print("=" * 60)
    print("3. yield from")
    print("=" * 60)

    # 展平嵌套列表
    nested = [1, [2, 3], [4, [5, 6]], [7, [8, [9]]]]
    print(f"展平: {list(flatten(nested))}")

    # 链接多个迭代器
    result = list(chain([1, 2, 3], ['a', 'b', 'c'], [10, 20]))
    print(f"链接: {result}")
    print()


def demo_send():
    """演示 send()"""
    print("=" * 60)
    print("4. send() 双向通信")
    print("=" * 60)

    acc = accumulator()
    next(acc)        # 启动生成器（必须先调用一次）
    acc.send(10)     # 发送 10
    acc.send(15)     # 发送 15
    acc.send(3)      # 发送 3
    try:
        acc.send(None)   # 结束
    except StopIteration as e:
        print(f"最终结果: {e.value}")
    print()


if __name__ == "__main__":
    demo_iterator()
    demo_generator()
    demo_yield_from()
    demo_send()
