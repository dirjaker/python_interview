"""
魔法方法 03: 算术运算符与上下文管理器
========================================

面试高频问题:
1. __add__ 和 __radd__ 的区别？
2. 上下文管理器的原理是什么？
3. 怎么实现一个连接池？

核心要点:
- 算术运算符: __add__, __sub__, __mul__, __truediv__ 等
- 反向运算符: __radd__, __rsub__ 等（左操作数不支持时调用右操作数的方法）
- 上下文管理器: __enter__ 和 __exit__，配合 with 语句使用
"""


import time
import threading
from contextlib import contextmanager


# ============================================================
# 1. 算术运算符重载
# ============================================================
# 面试官问: __add__ 和 __radd__ 有什么区别？
#
# 标准答:
# - __add__: obj + other 时调用 obj.__add__(other)
# - __radd__: other + obj 时，如果 other 不支持加法，调用 obj.__radd__(other)
# - 典型场景: Money(100) + 50  →  Money.__add__(50)
#             50 + Money(100)  →  int 不支持 + Money → Money.__radd__(50)
# ============================================================

class Money:
    """
    货币类 - 演示算术运算符

    运行结果:
        ¥100.00 + ¥50.00 = ¥150.00
        ¥100.00 * 3 = ¥300.00
        3 * ¥100.00 = ¥300.00    # 触发 __rmul__
        -¥100.00 = ¥-100.00      # 取负
        bool(¥0.00) = False      # 转布尔
        bool(¥100.00) = True
    """

    def __init__(self, amount, currency="CNY"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        """
        支持 Money + Money 或 Money + number

        注意:
            返回新对象（不可变语义）
            不修改 self
        """
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Currency mismatch")
            return Money(self.amount + other.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented  # 告诉 Python 尝试 other.__radd__

    def __radd__(self, other):
        """
        反向加法: 支持 number + Money

        调用时机:
            当 other + self 时，如果 other.__add__(self) 返回 NotImplemented，
            Python 就会尝试 self.__radd__(other)
        """
        # 注意: 这里直接调用 __add__，因为加法满足交换律
        return self.__add__(other)

    def __sub__(self, other):
        """支持 Money - Money 或 Money - number"""
        if isinstance(other, Money):
            return Money(self.amount - other.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount - other, self.currency)
        return NotImplemented

    def __mul__(self, scalar):
        """支持 Money * number"""
        if isinstance(scalar, (int, float)):
            return Money(self.amount * scalar, self.currency)
        return NotImplemented

    def __rmul__(self, scalar):
        """反向乘法: 支持 number * Money"""
        return self.__mul__(scalar)

    def __neg__(self):
        """支持 -Money"""
        return Money(-self.amount, self.currency)

    def __abs__(self):
        """支持 abs(Money)"""
        return Money(abs(self.amount), self.currency)

    def __bool__(self):
        """
        支持 bool(Money)

        规则:
            金额为 0 时返回 False，否则返回 True
            这样 if Money(0): 就不会执行
        """
        return self.amount != 0

    def __repr__(self):
        return f"¥{self.amount:.2f}"

    def __str__(self):
        return f"¥{self.amount:.2f}"


# ============================================================
# 2. 可调用对象 - __call__
# ============================================================
# 面试官问: 什么是可调用对象？
#
# 标准答:
# 可以用 () 调用的对象：
# - 函数
# - 类（调用时创建实例）
# - 实现了 __call__ 的实例
#
# 使用场景:
# - 装饰器（类实现的装饰器需要 __call__）
# - 策略模式（把策略封装成可调用对象）
# - 缓存（functools.lru_cache 内部就是用 __call__）
# ============================================================

class Polynomial:
    """
    多项式类 - 演示 __call__

    用法:
        p = Polynomial(1, 2, 3)  # 1 + 2x + 3x²
        print(p(2))              # 1 + 4 + 12 = 17

    运行结果:
        多项式: 1 + 2x + 3x²
        p(0) = 1
        p(1) = 6
        p(2) = 17
    """

    def __init__(self, *coefficients):
        """
        参数: 从低次到高次的系数
        Polynomial(1, 2, 3) 表示 1 + 2x + 3x²
        """
        self.coefficients = coefficients

    def __call__(self, x):
        """
        让实例可以像函数一样调用

        实现:
            p(x) = c0 + c1*x + c2*x² + ...
        """
        return sum(c * x**i for i, c in enumerate(self.coefficients))

    def __repr__(self):
        """生成可读的多项式表示"""
        terms = []
        for i, c in enumerate(self.coefficients):
            if c == 0:
                continue
            if i == 0:
                terms.append(str(c))
            elif i == 1:
                terms.append(f"{c}x")
            else:
                terms.append(f"{c}x{i}")
        return " + ".join(terms) if terms else "0"


# ============================================================
# 3. 上下文管理器 - __enter__ 和 __exit__
# ============================================================
# 面试官问: with 语句的原理是什么？
#
# 标准答:
# 1. with 语句调用 __enter__()，返回值赋给 as 后面的变量
# 2. 执行 with 代码块
# 3. 无论是否发生异常，都会调用 __exit__()
# 4. 如果发生异常，__exit__ 收到三个参数: exc_type, exc_val, exc_tb
# 5. __exit__ 返回 True 会吞掉异常，返回 False 会继续抛出
#
# 最佳实践:
# - 资源管理（文件、连接、锁）
# - 临时修改状态（修改全局变量、环境变量）
# - 计时、日志
# ============================================================

class Timer:
    """
    计时器上下文管理器

    用法:
        with Timer("my code"):
            time.sleep(1)

    运行结果:
        [my code] 耗时: 1.001s
    """

    def __init__(self, label=""):
        self.label = label

    def __enter__(self):
        """
        进入 with 代码块时调用

        返回值:
            会赋值给 as 后面的变量
            这里返回 self，这样可以用 Timer 的方法
        """
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出 with 代码块时调用（无论是否发生异常）

        参数:
            exc_type: 异常类型（没有异常时为 None）
            exc_val: 异常值
            exc_tb: 异常的 traceback

        返回值:
            True: 吞掉异常（不推荐，除非你有充分理由）
            False: 继续抛出异常（默认行为）
        """
        self.elapsed = time.perf_counter() - self.start
        print(f"[{self.label}] 耗时: {self.elapsed:.3f}s")
        return False  # 不吞掉异常


class ConnectionPool:
    """
    连接池上下文管理器

    演示:
        1. 资源的获取和释放
        2. 异常安全的资源管理
        3. __enter__ 返回有用的对象

    运行结果:
        连接池初始化，大小: 3
        获取连接: conn_0
        执行查询...
        释放连接: conn_0
    """

    def __init__(self, size=3):
        self.size = size
        self.pool = [f"conn_{i}" for i in range(size)]
        self.in_use = set()
        self.lock = threading.Lock()
        print(f"连接池初始化，大小: {size}")

    def __enter__(self):
        """
        获取连接

        返回值: 连接对象（会赋给 as 变量）
        """
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        释放连接

        注意:
            这里我们没有直接释放，因为 __exit__ 不知道释放哪个连接
            实际使用时，通常会在 __enter__ 返回一个包装对象，
            包装对象的 __exit__ 来释放连接
        """
        # 简化版：直接清空（实际应该释放特定连接）
        return False

    def acquire(self):
        """从池中获取一个连接"""
        with self.lock:
            if not self.pool:
                raise RuntimeError("No connections available")
            conn = self.pool.pop()
            self.in_use.add(conn)
            print(f"获取连接: {conn}")
            return conn

    def release(self, conn):
        """释放连接回池中"""
        with self.lock:
            self.in_use.discard(conn)
            self.pool.append(conn)
            print(f"释放连接: {conn}")


# ============================================================
# 4. 用 contextmanager 装饰器实现上下文管理器（更简洁）
# ============================================================
# 面试官问: 除了实现 __enter__/__exit__，还有其他方式创建上下文管理器吗？
#
# 标准答:
# 可以用 contextlib.contextmanager 装饰器，
# 把一个生成器函数变成上下文管理器。
# yield 之前的代码是 __enter__，yield 之后的是 __exit__。
# ============================================================

@contextmanager
def managed_resource(name):
    """
    用装饰器实现的上下文管理器

    优点: 代码更简洁，不需要写类

    用法:
        with managed_resource("database") as res:
            print(f"Using {res}")
    """
    print(f"获取资源: {name}")
    try:
        yield name  # yield 的值会赋给 as 变量
    except Exception as e:
        print(f"发生异常: {e}")
        raise  # 重新抛出
    finally:
        print(f"释放资源: {name}")


# ============================================================
# 主函数
# ============================================================

def demo_arithmetic():
    """演示算术运算符"""
    print("=" * 60)
    print("1. 算术运算符")
    print("=" * 60)

    m1 = Money(100)
    m2 = Money(50)

    print(f"{m1} + {m2} = {m1 + m2}")
    print(f"{m1} * 3 = {m1 * 3}")
    print(f"3 * {m1} = {3 * m1}")  # 触发 __rmul__
    print(f"-{m1} = {-m1}")
    print(f"bool({Money(0)}) = {bool(Money(0))}")
    print(f"bool({m1}) = {bool(m1)}")
    print()


def demo_callable():
    """演示可调用对象"""
    print("=" * 60)
    print("2. 可调用对象 __call__")
    print("=" * 60)

    p = Polynomial(1, 2, 3)  # 1 + 2x + 3x²
    print(f"多项式: {p}")
    print(f"p(0) = {p(0)}")
    print(f"p(1) = {p(1)}")
    print(f"p(2) = {p(2)}")
    print()


def demo_context_manager():
    """演示上下文管理器"""
    print("=" * 60)
    print("3. 上下文管理器")
    print("=" * 60)

    # Timer
    with Timer("sleep"):
        time.sleep(0.1)

    # ConnectionPool
    pool = ConnectionPool(size=3)
    conn = pool.acquire()
    print("执行查询...")
    pool.release(conn)

    # contextmanager 装饰器
    print("\n用装饰器实现:")
    with managed_resource("database") as res:
        print(f"使用 {res}")
    print()


if __name__ == "__main__":
    demo_arithmetic()
    demo_callable()
    demo_context_manager()
