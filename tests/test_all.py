"""
pytest 测试用例

运行方式:
    cd ~/myprojects/python_interview
    pytest tests/ -v
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# 魔法方法测试
# ============================================================

class TestLifecycle:
    """测试对象生命周期"""

    def test_new_init_order(self):
        """测试 __new__ 和 __init__ 的调用顺序"""
        # 验证实例化逻辑
        class Lifecycle:
            def __new__(cls, *args):
                instance = super().__new__(cls)
                instance._new_called = True
                return instance
            def __init__(self, value):
                self._init_called = True
                self.value = value

        obj = Lifecycle(42)
        assert obj._new_called == True
        assert obj._init_called == True
        assert obj.value == 42

    def test_singleton(self):
        """测试单例模式"""
        class Singleton:
            _instance = None
            def __new__(cls):
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                return cls._instance

        s1 = Singleton()
        s2 = Singleton()
        assert s1 is s2


class TestStringComparison:
    """测试字符串表示和比较"""

    def test_str_repr(self):
        """测试 __str__ 和 __repr__"""
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def __str__(self):
                return f"({self.x}, {self.y})"
            def __repr__(self):
                return f"Point(x={self.x}, y={self.y})"

        p = Point(3, 4)
        assert str(p) == "(3, 4)"
        assert repr(p) == "Point(x=3, y=4)"

    def test_eq_hash(self):
        """测试 __eq__ 和 __hash__"""
        class Temp:
            def __init__(self, val):
                self.val = val
            def __eq__(self, other):
                return self.val == other.val
            def __hash__(self):
                return hash(self.val)

        t1 = Temp(100)
        t2 = Temp(100)
        t3 = Temp(200)

        assert t1 == t2
        assert t1 != t3
        assert hash(t1) == hash(t2)

        # 可以放入 set
        s = {t1, t2, t3}
        assert len(s) == 2

    def test_container_protocol(self):
        """测试容器协议"""
        class MyList:
            def __init__(self, data):
                self._data = list(data)
            def __len__(self):
                return len(self._data)
            def __getitem__(self, index):
                return self._data[index]
            def __contains__(self, item):
                return item in self._data

        ml = MyList([1, 2, 3, 4, 5])
        assert len(ml) == 5
        assert ml[0] == 1
        assert 3 in ml
        assert 6 not in ml


class TestArithmeticContext:
    """测试算术运算符和上下文管理器"""

    def test_arithmetic(self):
        """测试算术运算符"""
        class Money:
            def __init__(self, amount):
                self.amount = amount
            def __add__(self, other):
                return Money(self.amount + other.amount)
            def __mul__(self, scalar):
                return Money(self.amount * scalar)
            def __bool__(self):
                return self.amount != 0

        m1 = Money(100)
        m2 = Money(50)

        assert (m1 + m2).amount == 150
        assert (m1 * 3).amount == 300
        assert bool(Money(0)) == False
        assert bool(Money(100)) == True

    def test_callable(self):
        """测试 __call__"""
        class Adder:
            def __init__(self, n):
                self.n = n
            def __call__(self, x):
                return self.n + x

        add5 = Adder(5)
        assert add5(3) == 8
        assert add5(10) == 15

    def test_context_manager(self):
        """测试上下文管理器"""
        class Timer:
            def __init__(self):
                self.elapsed = 0
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False

        with Timer() as t:
            assert isinstance(t, Timer)


class TestDescriptor:
    """测试描述符"""

    def test_property(self):
        """测试 property"""
        class Circle:
            def __init__(self, radius):
                self._radius = radius
            @property
            def radius(self):
                return self._radius
            @radius.setter
            def radius(self, value):
                if value <= 0:
                    raise ValueError("Radius must be positive")
                self._radius = value
            @property
            def area(self):
                import math
                return math.pi * self._radius ** 2

        c = Circle(5)
        assert c.radius == 5
        assert c.area > 78
        assert c.area < 79

        c.radius = 10
        assert c.radius == 10

        with pytest.raises(ValueError):
            c.radius = -1


class TestIterator:
    """测试迭代器和生成器"""

    def test_iterator(self):
        """测试迭代器协议"""
        class Countdown:
            def __init__(self, start):
                self.current = start
            def __iter__(self):
                return self
            def __next__(self):
                if self.current <= 0:
                    raise StopIteration
                self.current -= 1
                return self.current + 1

        result = list(Countdown(5))
        assert result == [5, 4, 3, 2, 1]

    def test_generator(self):
        """测试生成器"""
        def fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        result = list(fibonacci(10))
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_generator_expression(self):
        """测试生成器表达式"""
        gen = (x ** 2 for x in range(5))
        result = list(gen)
        assert result == [0, 1, 4, 9, 16]


# ============================================================
# 装饰器测试
# ============================================================

class TestDecorators:
    """测试装饰器"""

    def test_basic_decorator(self):
        """测试基础装饰器"""
        import functools

        def my_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) * 2
            return wrapper

        @my_decorator
        def add(a, b):
            return a + b

        assert add(1, 2) == 6
        assert add.__name__ == 'add'

    def test_parameterized_decorator(self):
        """测试带参数装饰器"""
        import functools

        def repeat(n):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    results = []
                    for _ in range(n):
                        results.append(func(*args, **kwargs))
                    return results
                return wrapper
            return decorator

        @repeat(3)
        def greet():
            return "Hello"

        result = greet()
        assert len(result) == 3
        assert all(r == "Hello" for r in result)

    def test_class_decorator(self):
        """测试类装饰器"""
        import functools

        class CountCalls:
            def __init__(self, func):
                functools.update_wrapper(self, func)
                self.func = func
                self.count = 0
            def __call__(self, *args, **kwargs):
                self.count += 1
                return self.func(*args, **kwargs)

        @CountCalls
        def hello():
            return "Hi"

        hello()
        hello()
        hello()
        assert hello.count == 3


# ============================================================
# 标准库测试
# ============================================================

class TestStdlib:
    """测试标准库"""

    def test_counter(self):
        """测试 Counter"""
        from collections import Counter

        c = Counter(['a', 'b', 'a', 'c', 'a'])
        assert c['a'] == 3
        assert c['b'] == 1
        assert c.most_common(1) == [('a', 3)]

    def test_defaultdict(self):
        """测试 defaultdict"""
        from collections import defaultdict

        dd = defaultdict(list)
        dd['a'].append(1)
        dd['a'].append(2)
        dd['b'].append(3)

        assert dd['a'] == [1, 2]
        assert dd['b'] == [3]
        assert dd['c'] == []

    def test_deque(self):
        """测试 deque"""
        from collections import deque

        dq = deque([1, 2, 3], maxlen=5)
        dq.append(4)
        dq.appendleft(0)

        assert list(dq) == [0, 1, 2, 3, 4]

        dq.append(5)
        assert list(dq) == [1, 2, 3, 4, 5]

    def test_lru_cache(self):
        """测试 lru_cache"""
        from functools import lru_cache

        @lru_cache(maxsize=128)
        def fib(n):
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)

        assert fib(10) == 55
        assert fib(20) == 6765
        assert fib.cache_info().hits > 0

    def test_partial(self):
        """测试 partial"""
        from functools import partial

        def power(base, exp):
            return base ** exp

        square = partial(power, exp=2)
        cube = partial(power, exp=3)

        assert square(5) == 25
        assert cube(3) == 27


# ============================================================
# 设计模式测试
# ============================================================

class TestPatterns:
    """测试设计模式"""

    def test_singleton(self):
        """测试单例模式"""
        class Singleton:
            _instance = None
            def __new__(cls):
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                return cls._instance

        s1 = Singleton()
        s2 = Singleton()
        assert s1 is s2

    def test_factory(self):
        """测试工厂模式"""
        class Circle:
            def __init__(self, r):
                self.r = r
            def area(self):
                import math
                return math.pi * self.r ** 2

        class Rectangle:
            def __init__(self, w, h):
                self.w = w
                self.h = h
            def area(self):
                return self.w * self.h

        class ShapeFactory:
            _registry = {'circle': Circle, 'rect': Rectangle}
            @classmethod
            def create(cls, shape_type, **kwargs):
                return cls._registry[shape_type](**kwargs)

        c = ShapeFactory.create('circle', r=5)
        r = ShapeFactory.create('rect', w=3, h=4)

        assert c.area() > 78
        assert c.area() < 79
        assert r.area() == 12

    def test_observer(self):
        """测试观察者模式"""
        class EventEmitter:
            def __init__(self):
                self._listeners = {}
            def on(self, event, callback):
                self._listeners.setdefault(event, []).append(callback)
            def emit(self, event, *args):
                for cb in self._listeners.get(event, []):
                    cb(*args)

        emitter = EventEmitter()
        results = []

        emitter.on('data', lambda x: results.append(x))
        emitter.emit('data', 1)
        emitter.emit('data', 2)

        assert results == [1, 2]


# ============================================================
# 异步测试
# ============================================================

class TestAsync:
    """测试异步编程"""

    @pytest.mark.asyncio
    async def test_coroutine(self):
        """测试协程"""
        import asyncio

        async def fetch():
            await asyncio.sleep(0.01)
            return "data"

        result = await fetch()
        assert result == "data"

    @pytest.mark.asyncio
    async def test_gather(self):
        """测试 asyncio.gather"""
        import asyncio

        async def task(n):
            await asyncio.sleep(0.01)
            return n * 2

        results = await asyncio.gather(
            task(1), task(2), task(3)
        )
        assert results == [2, 4, 6]

    @pytest.mark.asyncio
    async def test_semaphore(self):
        """测试 Semaphore"""
        import asyncio

        sem = asyncio.Semaphore(2)
        counter = 0

        async def limited_task():
            nonlocal counter
            async with sem:
                counter += 1
                await asyncio.sleep(0.01)
                return counter

        tasks = [limited_task() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        assert len(results) == 5
