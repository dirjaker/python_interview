"""
装饰器 01: 基础装饰器
=======================

面试高频问题:
1. 什么是装饰器？本质是什么？
2. functools.wraps 有什么用？
3. 装饰器的执行时机？

核心要点:
- 装饰器本质：接受函数作为参数，返回新函数的高阶函数
- @语法糖：@decorator 等价于 func = decorator(func)
- functools.wraps：保留原函数的元信息（name, docstring 等）
"""


import functools
import time
import logging


# ============================================================
# 1. 最简单的装饰器
# ============================================================
# 面试官问: 什么是装饰器？
#
# 标准答:
# 装饰器是一个接受函数作为参数、返回新函数的高阶函数。
# 它可以在不修改原函数代码的情况下，增加额外功能。
#
# 本质:
#   @decorator
#   def func(): pass
#
# 等价于:
#   def func(): pass
#   func = decorator(func)
#
# 执行时机:
#   装饰器在定义函数时就执行（不是调用函数时）
#   所以装饰器中的闭包逻辑在 import 时就会执行
# ============================================================

def timer(func):
    """
    计时装饰器 - 测量函数执行时间

    这是最经典的装饰器示例

    运行结果:
        [timer] slow_function 耗时: 0.501s
        Result: 42
    """
    @functools.wraps(func)  # 保留原函数的元信息！
    def wrapper(*args, **kwargs):
        """
        wrapper 是实际被调用的函数

        *args, **kwargs: 接受任意参数，保证通用性
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)  # 调用原函数
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} 耗时: {elapsed:.3f}s")
        return result

    return wrapper  # 返回包装后的函数


def logger(func):
    """
    日志装饰器 - 记录函数调用

    运行结果:
        [logger] 调用 add(1, 2)
        [logger] add 返回 3
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 调用前记录
        print(f"[logger] 调用 {func.__name__}({args}, {kwargs})")

        # 调用原函数
        result = func(*args, **kwargs)

        # 调用后记录
        print(f"[logger] {func.__name__} 返回 {result}")
        return result

    return wrapper


# ============================================================
# 2. functools.wraps 的作用
# ============================================================
# 面试官问: functools.wraps 有什么用？
#
# 标准答:
# 不用 wraps 时，wrapper 会丢失原函数的元信息：
# - __name__ 变成 'wrapper'
# - __doc__ 变成 wrapper 的 docstring
# - help() 显示 wrapper 的信息
#
# 用 wraps 后，这些信息会从原函数复制过来。
#
# 最佳实践: 总是使用 @functools.wraps(func)
# ============================================================

def bad_decorator(func):
    """没有使用 wraps 的装饰器"""
    def wrapper(*args, **kwargs):
        """wrapper 的文档"""
        return func(*args, **kwargs)
    return wrapper


def good_decorator(func):
    """使用了 wraps 的装饰器"""
    @functools.wraps(func)  # 关键！
    def wrapper(*args, **kwargs):
        """wrapper 的文档"""
        return func(*args, **kwargs)
    return wrapper


@bad_decorator
def func_a():
    """func_a 的文档"""
    pass


@good_decorator
def func_b():
    """func_b 的文档"""
    pass


# ============================================================
# 3. 带参数的装饰器（三层嵌套）
# ============================================================
# 面试官问: 怎么给装饰器传递参数？
#
# 标准答:
# 需要三层嵌套：
# 1. 最外层：接受装饰器参数
# 2. 中间层：接受被装饰的函数
# 3. 最内层：实际执行的包装函数
#
# 语法:
#   @decorator(arg)    # 等价于 func = decorator(arg)(func)
#   def func(): pass
# ============================================================

def repeat(n=2):
    """
    重复执行装饰器

    运行结果:
        Hello!
        Hello!
        Hello!
        Hello!
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def validate_types(**expected_types):
    """
    类型验证装饰器

    用法:
        @validate_types(x=int, y=int)
        def add(x, y):
            return x + y

    运行结果:
        add(1, 2) = 3
        TypeError: x must be int, got str
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数的参数名
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # 验证类型
            for param_name, expected_type in expected_types.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{param_name} must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )

            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# 4. 类实现的装饰器
# ============================================================
# 面试官问: 装饰器可以用类实现吗？
#
# 标准答:
# 可以！类实现的装饰器需要实现 __call__ 方法。
#
# 优点:
# - 可以维护状态（实例变量）
# - 更容易理解（类比函数闭包）
# - 可以实现更复杂的逻辑
#
# 用法:
#   @MyDecorator
#   def func(): pass
#
# 等价于:
#   def func(): pass
#   func = MyDecorator(func)  # 创建实例
#   func()  # 调用实例的 __call__
# ============================================================

class CountCalls:
    """
    计数装饰器 - 记录函数被调用的次数

    运行结果:
        hello() 被调用了 3 次
    """

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        """每次调用函数时执行"""
        self.count += 1
        print(f"[CountCalls] {self.func.__name__} 被调用了 {self.count} 次")
        return self.func(*args, **kwargs)

    def reset(self):
        """重置计数"""
        self.count = 0


class Memoize:
    """
    缓存装饰器 - 自动缓存函数结果

    运行结果:
        计算 fibonacci(10)...
        fib(10) = 55
        fib(10) = 55  # 直接返回缓存
        缓存: {(10,): 55}
    """

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            print(f"计算 {self.func.__name__}{args}...")
            self.cache[args] = self.func(*args)
        return self.cache[args]


# ============================================================
# 5. 实际应用示例
# ============================================================

@timer
def slow_function():
    """一个慢函数（用于演示 timer）"""
    time.sleep(0.5)
    return 42


@logger
def add(x, y):
    """加法函数（用于演示 logger）"""
    return x + y


@repeat(n=3)
def say_hello():
    """重复打印（用于演示 repeat）"""
    print("Hello!")


@validate_types(x=int, y=int)
def multiply(x, y):
    """乘法（用于演示 validate_types）"""
    return x * y


@CountCalls
def greet(name):
    """问候函数（用于演示 CountCalls）"""
    print(f"Hello, {name}!")


@Memoize
def fibonacci(n):
    """斐波那契（用于演示 Memoize）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================
# 主函数
# ============================================================

def demo_basic():
    """演示基础装饰器"""
    print("=" * 60)
    print("1. 基础装饰器")
    print("=" * 60)

    # timer
    result = slow_function()
    print(f"Result: {result}")

    # logger
    add(1, 2)
    print()


def demo_wraps():
    """演示 functools.wraps"""
    print("=" * 60)
    print("2. functools.wraps")
    print("=" * 60)

    print(f"bad_decorator: __name__={func_a.__name__}, __doc__={func_a.__doc__}")
    print(f"good_decorator: __name__={func_b.__name__}, __doc__={func_b.__doc__}")
    print()


def demo_parameterized():
    """演示带参数的装饰器"""
    print("=" * 60)
    print("3. 带参数的装饰器")
    print("=" * 60)

    # repeat
    say_hello()

    # validate_types
    print(f"\nmultiply(3, 4) = {multiply(3, 4)}")
    try:
        multiply("3", 4)
    except TypeError as e:
        print(f"类型错误: {e}")
    print()


def demo_class_decorator():
    """演示类装饰器"""
    print("=" * 60)
    print("4. 类装饰器")
    print("=" * 60)

    # CountCalls
    greet("Alice")
    greet("Bob")
    greet("Charlie")

    # Memoize
    print(f"\nfib(10) = {fibonacci(10)}")
    print(f"fib(10) = {fibonacci(10)}")  # 从缓存获取
    print()


if __name__ == "__main__":
    demo_basic()
    demo_wraps()
    demo_parameterized()
    demo_class_decorator()
