"""装饰器完整演示"""

import time
import functools
from typing import Any, Callable


# ============================================================
# 1. 基础装饰器
# ============================================================

def timer(func):
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱ {func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper


def logger(func):
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📝 调用 {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"📝 {func.__name__} 返回: {result}")
        return result
    return wrapper


# ============================================================
# 2. 带参数的装饰器
# ============================================================

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"⚠ 重试 {attempt + 1}/{max_attempts}: {e}")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def rate_limit(calls_per_second=10):
    """限流装饰器"""
    min_interval = 1.0 / calls_per_second
    last_call_time = 0

    def decorator(func):
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


def validate_types(**expected_types):
    """类型验证装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 检查位置参数
            annotations = func.__annotations__
            for i, (arg_name, expected_type) in enumerate(expected_types.items()):
                if i < len(args):
                    if not isinstance(args[i], expected_type):
                        raise TypeError(
                            f"参数 {arg_name} 期望 {expected_type.__name__}, "
                            f"得到 {type(args[i]).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache(maxsize=128):
    """简单缓存装饰器"""
    def decorator(func):
        cache_dict = {}
        access_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in cache_dict:
                # 移到最前面
                access_order.remove(args)
                access_order.insert(0, args)
                return cache_dict[args]

            result = func(*args)

            # 缓存满时淘汰最久未使用的
            if len(cache_dict) >= maxsize:
                oldest = access_order.pop()
                del cache_dict[oldest]

            cache_dict[args] = result
            access_order.insert(0, args)
            return result

        wrapper.cache_clear = lambda: (cache_dict.clear(), access_order.clear())
        wrapper.cache_info = lambda: {"hits": 0, "misses": 0, "size": len(cache_dict)}
        return wrapper
    return decorator


# ============================================================
# 3. 类装饰器
# ============================================================

class SingletonDecorator:
    """单例装饰器"""

    def __init__(self, cls):
        self.cls = cls
        self.instance = None
        functools.update_wrapper(self, cls)

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


class CountCalls:
    """调用计数装饰器"""

    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"📊 {self.func.__name__} 已调用 {self.count} 次")
        return self.func(*args, **kwargs)


class Memoize:
    """记忆化装饰器（支持异步）"""

    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]


# ============================================================
# 4. 装饰器叠加
# ============================================================

@timer
@logger
def add(a, b):
    """加法函数"""
    time.sleep(0.1)
    return a + b


@retry(max_attempts=3, delay=0.5)
def unstable_api_call():
    """模拟不稳定的 API 调用"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("网络错误")
    return "成功"


@validate_types(x=int, y=int)
def multiply(x, y):
    return x * y


@cache(maxsize=100)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================
# 5. functools.lru_cache 对比
# ============================================================

@functools.lru_cache(maxsize=128)
def fib_builtin(n):
    """使用内置 lru_cache"""
    if n < 2:
        return n
    return fib_builtin(n - 1) + fib_builtin(n - 2)


# ============================================================
# 6. 属性装饰器
# ============================================================

class Circle:
    """使用 property 装饰器"""

    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """getter"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """setter"""
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value

    @radius.deleter
    def radius(self):
        """deleter"""
        del self._radius

    @property
    def area(self):
        """只读属性"""
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        import math
        return 2 * math.pi * self._radius


# ============================================================
# 7. 注册装饰器
# ============================================================

class Registry:
    """函数注册表"""

    def __init__(self):
        self._registry = {}

    def register(self, name=None):
        def decorator(func):
            key = name or func.__name__
            self._registry[key] = func
            return func
        return decorator

    def get(self, name):
        return self._registry.get(name)

    def list_all(self):
        return list(self._registry.keys())


# 创建全局注册表
command_registry = Registry()


@command_registry.register()
def hello():
    return "Hello!"


@command_registry.register(name="greet")
def greet_user(name):
    return f"Hello, {name}!"


# ============================================================
# 8. 异步装饰器
# ============================================================

def async_timer(func):
    """异步计时装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱ {func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper


def async_retry(max_attempts=3, delay=1.0):
    """异步重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("装饰器演示")
    print("=" * 60)

    # 1. 基础装饰器
    print("\n1. 基础装饰器:")
    result = add(3, 4)
    print(f"结果: {result}")
    print(f"函数名: {add.__name__}")  # 保留了原函数名

    # 2. 带参数的装饰器
    print("\n2. 类型验证:")
    try:
        multiply(3, 4)
        print("multiply(3, 4) = 12")
        multiply("3", 4)
    except TypeError as e:
        print(f"类型错误: {e}")

    # 3. 缓存装饰器
    print("\n3. 缓存装饰器:")
    start = time.perf_counter()
    result = fib_builtin(100)
    elapsed = time.perf_counter() - start
    print(f"fib(100) = {result}, 耗时: {elapsed:.6f}s")

    start = time.perf_counter()
    result = fib_builtin(100)
    elapsed = time.perf_counter() - start
    print(f"fib(100) 缓存命中: {elapsed:.6f}s")

    # 4. 属性装饰器
    print("\n4. 属性装饰器:")
    c = Circle(5)
    print(f"半径: {c.radius}")
    print(f"面积: {c.area:.2f}")
    print(f"周长: {c.circumference:.2f}")

    # 5. 注册装饰器
    print("\n5. 注册装饰器:")
    print(f"已注册命令: {command_registry.list_all()}")
    func = command_registry.get("greet")
    print(f"调用 greet: {func('Alice')}")

    # 6. 类装饰器
    print("\n6. 调用计数装饰器:")

    @CountCalls
    def say_hello():
        return "Hello!"

    say_hello()
    say_hello()
    say_hello()
    print(f"总调用次数: {say_hello.count}")
