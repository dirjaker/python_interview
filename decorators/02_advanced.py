"""
装饰器 02: 高级装饰器
=======================

面试高频问题:
1. 装饰器叠加的执行顺序？
2. 异步装饰器怎么写？
3. 装饰器有哪些实际应用场景？

核心要点:
- 装饰器叠加：从下往上装饰，从上往下执行
- 异步装饰器：需要区分同步/异步函数
- 实际应用：缓存、重试、限流、权限检查
"""


import functools
import asyncio
import time
from functools import lru_cache


# ============================================================
# 1. 装饰器叠加
# ============================================================
# 面试官问: 多个装饰器叠加时，执行顺序是什么？
#
# 标准答:
# 装饰顺序：从下往上（靠近函数的先装饰）
# 执行顺序：从上往下（靠近函数的后执行）
#
# @A
# @B
# @C
# def func(): pass
#
# 等价于: func = A(B(C(func)))
#
# 执行顺序: A → B → C → func
# ============================================================

def bold(func):
    """加粗装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italic(func):
    """斜体装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


def underline(func):
    """下划线装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper


@bold
@italic
@underline
def greet(name):
    """
    装饰顺序: underline → italic → bold
    执行顺序: bold → italic → underline → greet

    运行结果: <b><i><u>Hello, Alice!</u></i></b>
    """
    return f"Hello, {name}!"


# ============================================================
# 2. 重试装饰器
# ============================================================

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """
    重试装饰器 - 自动重试失败的函数

    用法:
        @retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
        def fetch_data():
            ...

    运行结果:
        尝试 1/3 失败: Connection refused
        等待 0.5s...
        尝试 2/3 成功！
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"尝试 {attempt}/{max_attempts} 成功！")
                    return result
                except exceptions as e:
                    last_exception = e
                    print(f"尝试 {attempt}/{max_attempts} 失败: {e}")
                    if attempt < max_attempts:
                        print(f"等待 {delay}s...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# ============================================================
# 3. 限流装饰器
# ============================================================

def rate_limit(calls_per_second=10):
    """
    限流装饰器 - 控制函数调用频率

    用法:
        @rate_limit(calls_per_second=2)
        def api_call():
            ...
    """
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_call_time = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            elapsed = time.time() - last_call_time
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call_time = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# 4. 异步装饰器
# ============================================================
# 面试官问: 异步函数怎么用装饰器？
#
# 标准答:
# 需要用 asyncio.iscoroutinefunction 检测是否是异步函数，
# 然后分别处理：
# - 异步函数：wrapper 也用 async def
# - 同步函数：wrapper 用普通 def
#
# 或者用 functools.wraps + async def wrapper（简单情况）
# ============================================================

def async_timer(func):
    """
    异步计时装饰器

    用法:
        @async_timer
        async def my_coroutine():
            await asyncio.sleep(1)
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[async_timer] {func.__name__} 耗时: {elapsed:.3f}s")
        return result
    return wrapper


def async_retry(max_attempts=3, delay=1.0):
    """
    异步重试装饰器

    用法:
        @async_retry(max_attempts=3)
        async def fetch():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"尝试 {attempt} 失败: {e}, 重试中...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator


# ============================================================
# 5. 注册表装饰器（插件系统）
# ============================================================

class Registry:
    """
    注册表 - 用装饰器注册函数

    常见于:
        - Web 框架的路由注册 (@app.route)
        - 命令行工具的命令注册
        - 插件系统

    运行结果:
        注册命令: hello
        注册命令: goodbye
        已注册命令: ['hello', 'goodbye']
        执行 hello: Hello, World!
    """

    def __init__(self):
        self._registry = {}

    def register(self, name=None):
        """
        注册装饰器

        用法:
            @registry.register("my_func")
            def func(): pass

            @registry.register()  # 用函数名作为注册名
            def func(): pass
        """
        def decorator(func):
            func_name = name or func.__name__
            self._registry[func_name] = func
            print(f"注册命令: {func_name}")
            return func
        return decorator

    def get(self, name):
        """获取已注册的函数"""
        return self._registry.get(name)

    def list_all(self):
        """列出所有已注册的函数"""
        return list(self._registry.keys())

    def execute(self, name, *args, **kwargs):
        """执行已注册的函数"""
        func = self._registry.get(name)
        if func is None:
            raise KeyError(f"Unknown command: {name}")
        return func(*args, **kwargs)


# 创建全局注册表
command_registry = Registry()


@command_registry.register()
def hello():
    return "Hello, World!"


@command_registry.register()
def goodbye():
    return "Goodbye, World!"


# ============================================================
# 主函数
# ============================================================

def demo_stacking():
    """演示装饰器叠加"""
    print("=" * 60)
    print("1. 装饰器叠加")
    print("=" * 60)

    result = greet("Alice")
    print(f"结果: {result}")
    print()


def demo_retry():
    """演示重试装饰器"""
    print("=" * 60)
    print("2. 重试装饰器")
    print("=" * 60)

    call_count = 0

    @retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
    def unstable_api():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Connection refused")
        return "Success!"

    result = unstable_api()
    print(f"结果: {result}")
    print()


def demo_registry():
    """演示注册表装饰器"""
    print("=" * 60)
    print("3. 注册表装饰器")
    print("=" * 60)

    print(f"已注册命令: {command_registry.list_all()}")
    result = command_registry.execute("hello")
    print(f"执行 hello: {result}")
    print()


async def demo_async():
    """演示异步装饰器"""
    print("=" * 60)
    print("4. 异步装饰器")
    print("=" * 60)

    @async_timer
    async def slow_coroutine():
        await asyncio.sleep(0.3)
        return "Done!"

    result = await slow_coroutine()
    print(f"结果: {result}")
    print()


if __name__ == "__main__":
    demo_stacking()
    demo_retry()
    demo_registry()
    asyncio.run(demo_async())
