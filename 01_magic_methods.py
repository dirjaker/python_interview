"""魔法方法完整演示"""

import time
from functools import total_ordering


# ============================================================
# 1. 对象生命周期
# ============================================================

class LifecycleDemo:
    """演示 __new__ 和 __init__ 的区别"""

    def __new__(cls, *args, **kwargs):
        print(f"__new__ 创建实例: {cls.__name__}")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        print(f"__init__ 初始化实例: {value}")
        self.value = value

    def __del__(self):
        print(f"__del__ 销毁实例: {self.value}")


# 单例模式
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("创建新实例")
            cls._instance = super().__new__(cls)
        else:
            print("返回已有实例")
        return cls._instance

    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


# ============================================================
# 2. 字符串表示
# ============================================================

class Vector:
    """自定义向量类，演示 __str__ 和 __repr__"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """面向用户：print() 和 str() 时调用"""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """面向开发者：repr() 和交互式环境"""
        return f"Vector(x={self.x}, y={self.y})"


# ============================================================
# 3. 比较运算符
# ============================================================

@total_ordering
class Temperature:
    """使用 @total_ordering 简化比较方法"""

    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        return self.celsius == other.celsius

    def __lt__(self, other):
        return self.celsius < other.celsius

    def __repr__(self):
        return f"Temperature({self.celsius}°C)"

    def __hash__(self):
        return hash(self.celsius)


# ============================================================
# 4. 算术运算符
# ============================================================

class Money:
    """货币类，演示算术运算符重载"""

    def __init__(self, amount, currency="CNY"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("不同货币不能相加")
            return Money(self.amount + other.amount, self.currency)
        return Money(self.amount + other, self.currency)

    def __radd__(self, other):
        """支持 int + Money"""
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            return Money(self.amount - other.amount, self.currency)
        return Money(self.amount - other, self.currency)

    def __mul__(self, scalar):
        return Money(self.amount * scalar, self.currency)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __neg__(self):
        return Money(-self.amount, self.currency)

    def __abs__(self):
        return Money(abs(self.amount), self.currency)

    def __bool__(self):
        return self.amount != 0

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        return f"¥{self.amount:.2f}"


# ============================================================
# 5. 容器协议
# ============================================================

class SortedList:
    """自定义有序列表，演示容器协议"""

    def __init__(self, data=None):
        self._data = sorted(data) if data else []

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value
        self._data.sort()  # 保持有序

    def __delitem__(self, index):
        del self._data[index]

    def __contains__(self, item):
        # 二分查找优化
        import bisect
        i = bisect.bisect_left(self._data, item)
        return i < len(self._data) and self._data[i] == item

    def __iter__(self):
        return iter(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def __add__(self, other):
        return SortedList(self._data + other._data)

    def __iadd__(self, other):
        self._data.extend(other._data)
        self._data.sort()
        return self

    def __repr__(self):
        return f"SortedList({self._data})"


# ============================================================
# 6. 可调用对象
# ============================================================

class Polynomial:
    """多项式类，支持调用"""

    def __init__(self, *coefficients):
        self.coefficients = coefficients

    def __call__(self, x):
        """计算多项式的值"""
        result = 0
        for i, coef in enumerate(self.coefficients):
            result += coef * (x ** i)
        return result

    def __repr__(self):
        terms = []
        for i, coef in enumerate(self.coefficients):
            if coef == 0:
                continue
            if i == 0:
                terms.append(str(coef))
            elif i == 1:
                terms.append(f"{coef}x")
            else:
                terms.append(f"{coef}x^{i}")
        return " + ".join(terms) or "0"


# ============================================================
# 7. 上下文管理器
# ============================================================

class Timer:
    """计时上下文管理器"""

    def __init__(self, label=""):
        self.label = label
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        if self.label:
            print(f"{self.label}: {self.elapsed:.4f}s")
        return False  # 不抑制异常


class ConnectionPool:
    """连接池上下文管理器"""

    def __init__(self, size=5):
        self.size = size
        self.connections = []
        self.in_use = set()

    def __enter__(self):
        print("初始化连接池")
        for i in range(self.size):
            self.connections.append(f"conn_{i}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关闭连接池")
        self.connections.clear()
        self.in_use.clear()
        return False

    def acquire(self):
        for conn in self.connections:
            if conn not in self.in_use:
                self.in_use.add(conn)
                return conn
        raise RuntimeError("没有可用连接")

    def release(self, conn):
        self.in_use.discard(conn)


# ============================================================
# 8. 属性访问控制
# ============================================================

class Config:
    """配置类，支持动态属性访问"""

    def __init__(self, **kwargs):
        object.__setattr__(self, '_data', kwargs)

    def __getattr__(self, name):
        """访问不存在的属性时调用"""
        return self._data.get(name)

    def __setattr__(self, name, value):
        """设置属性时调用"""
        self._data[name] = value

    def __delattr__(self, name):
        """删除属性时调用"""
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(name)

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return f"Config({self._data})"


# ============================================================
# 9. 描述符
# ============================================================

class Validated:
    """带验证的描述符"""

    def __init__(self, validator=None, error_msg="Invalid value"):
        self.validator = validator
        self.error_msg = error_msg

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"{self.name}: {self.error_msg} (got {value})")
        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        delattr(obj, self.private_name)


class Person:
    name = Validated(lambda x: isinstance(x, str) and len(x) > 0, "名字不能为空")
    age = Validated(lambda x: isinstance(x, int) and 0 < x < 150, "年龄必须在 1-149 之间")

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


# ============================================================
# 10. 迭代器协议
# ============================================================

class Fibonacci:
    """斐波那契迭代器"""

    def __init__(self, max_count=None, max_value=None):
        self.max_count = max_count
        self.max_value = max_value

    def __iter__(self):
        self.a, self.b = 0, 1
        self.count = 0
        return self

    def __next__(self):
        if self.max_count and self.count >= self.max_count:
            raise StopIteration
        if self.max_value and self.a > self.max_value:
            raise StopIteration

        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("魔法方法演示")
    print("=" * 60)

    # 1. 生命周期
    print("\n1. 对象生命周期:")
    obj = LifecycleDemo(42)
    del obj

    print("\n单例模式:")
    s1 = Singleton("first")
    s2 = Singleton("second")
    print(f"s1 is s2: {s1 is s2}")

    # 2. 字符串表示
    print("\n2. 字符串表示:")
    v = Vector(3, 4)
    print(f"str: {v}")
    print(f"repr: {repr(v)}")

    # 3. 比较运算符
    print("\n3. 比较运算符:")
    t1 = Temperature(20)
    t2 = Temperature(30)
    print(f"{t1} < {t2}: {t1 < t2}")
    print(f"{t1} > {t2}: {t1 > t2}")
    print(f"{t1} == {t2}: {t1 == t2}")

    # 4. 算术运算符
    print("\n4. 算术运算符:")
    m1 = Money(100)
    m2 = Money(50)
    print(f"{m1} + {m2} = {m1 + m2}")
    print(f"{m1} * 3 = {m1 * 3}")
    print(f"3 * {m1} = {3 * m1}")
    print(f"bool(Money(0)): {bool(Money(0))}")

    # 5. 容器协议
    print("\n5. 容器协议:")
    sl = SortedList([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"SortedList: {sl}")
    print(f"len: {len(sl)}")
    print(f"3 in list: {3 in sl}")
    print(f"reversed: {list(reversed(sl))}")

    # 6. 可调用对象
    print("\n6. 可调用对象:")
    p = Polynomial(1, 2, 3)  # 1 + 2x + 3x^2
    print(f"多项式: {p}")
    print(f"p(2) = {p(2)}")

    # 7. 上下文管理器
    print("\n7. 上下文管理器:")
    with Timer("排序测试"):
        sorted(range(100000))

    # 8. 属性访问
    print("\n8. 属性访问控制:")
    config = Config(debug=True, port=8000)
    print(f"config: {config}")
    print(f"config.debug: {config.debug}")
    config.host = "localhost"
    print(f"config.host: {config.host}")

    # 9. 描述符
    print("\n9. 描述符:")
    p = Person("Alice", 30)
    print(p)
    try:
        p.age = -5
    except ValueError as e:
        print(f"验证失败: {e}")

    # 10. 迭代器
    print("\n10. 迭代器:")
    fib = Fibonacci(max_count=10)
    print(f"斐波那契前10项: {list(fib)}")

    fib = Fibonacci(max_value=100)
    print(f"斐波那契(<100): {list(fib)}")
