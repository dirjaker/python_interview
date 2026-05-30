# Python 面试速查表

> 面试前 30 分钟快速复习用

---

## 1. 魔法方法

### 对象生命周期
```python
class MyClass:
    def __new__(cls, *args):      # 1. 创建实例（必须返回实例）
        return super().__new__(cls)
    def __init__(self, *args):    # 2. 初始化实例
        pass
    def __del__(self):            # 3. 销毁实例（不推荐依赖）
        pass
```

### 字符串表示
```python
def __str__(self):    # print() 时调用，面向用户
    return "可读"
def __repr__(self):   # repr() 时调用，面向开发者
    return "ClassName(...)"
```

### 比较运算符
```python
def __eq__(self, other): return self.val == other.val  # ==
def __lt__(self, other): return self.val < other.val   # <
def __hash__(self): return hash(self.val)              # set/dict 需要
# @total_ordering: 只需 __eq__ + __lt__，自动生成其余
```

### 容器协议
```python
def __len__(self):        # len(obj)
def __getitem__(self, k): # obj[k]
def __setitem__(self, k, v): # obj[k] = v
def __contains__(self, item): # item in obj
def __iter__(self):       # for x in obj
```

### 上下文管理器
```python
def __enter__(self):      # with obj:
    return self
def __exit__(self, *exc): # 离开 with 块
    return False  # True=吞异常
```

### 描述符
```python
def __get__(self, obj, objtype):  # 访问属性
def __set__(self, obj, value):    # 设置属性
def __delete__(self, obj):        # 删除属性
# @property 是描述符的语法糖
```

---

## 2. 装饰器

### 基础装饰器
```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # 保留元信息！
    def wrapper(*args, **kwargs):
        # 前置逻辑
        result = func(*args, **kwargs)
        # 后置逻辑
        return result
    return wrapper
```

### 带参数装饰器
```python
def repeat(n=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(n=3)
def say_hello(): print("Hello!")
```

### 类装饰器
```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
```

### 装饰器叠加顺序
```python
@A    # 最后执行
@B    # ↓
@C    # 最先执行（靠近函数）
def func(): pass
# 等价于: A(B(C(func)))
```

---

## 3. 异步编程

### 协程基础
```python
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    return "result"

asyncio.run(my_coroutine())
```

### 并发执行
```python
# gather: 并发执行，按顺序返回
results = await asyncio.gather(coro1(), coro2(), coro3())

# create_task: 动态创建任务
task = asyncio.create_task(coro())
result = await task

# as_completed: 按完成顺序返回
for coro in asyncio.as_completed(tasks):
    result = await coro
```

### 超时控制
```python
try:
    result = await asyncio.wait_for(coro(), timeout=5.0)
except asyncio.TimeoutError:
    print("超时！")
```

### Semaphore 限流
```python
sem = asyncio.Semaphore(10)
async with sem:
    # 最多同时执行 10 个
    await do_work()
```

---

## 4. GIL

### 是什么
- Global Interpreter Lock，CPython 特性
- 同一时刻只有一个线程执行 Python 字节码

### 影响
| 任务类型 | 多线程效果 | 推荐方案 |
|---------|-----------|---------|
| CPU 密集型 | ❌ 无效 | 多进程 |
| IO 密集型 | ✅ 有效 | 多线程/异步 |

### 绕过方法
```python
# 1. 多进程
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(func, data)

# 2. C 扩展（numpy 自动释放 GIL）
import numpy as np
result = np.sum(big_array)

# 3. 异步（单线程并发）
async def main():
    await asyncio.gather(coro1(), coro2())
```

---

## 5. 元类

### type 和 object
```python
type(object)  # <class 'type'>
type(type)    # <class 'type'>
isinstance(object, type)  # True
isinstance(type, object)  # True
```

### 动态创建类
```python
Dog = type('Dog', (object,), {
    'bark': lambda self: 'Woof!'
})
```

### 自定义元类
```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(metaclass=SingletonMeta):
    pass
```

### __init_subclass__（更简单）
```python
class PluginBase:
    _plugins = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._plugins[cls.__name__] = cls
```

---

## 6. 内存管理

### 引用计数
```python
import sys
a = [1, 2, 3]
sys.getrefcount(a)  # 2（a + 参数）
b = a
sys.getrefcount(a)  # 3
```

### __slots__
```python
class Point:
    __slots__ = ['x', 'y']  # 减少内存 30%-50%
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### 弱引用
```python
import weakref
ref = weakref.ref(obj)
ref()  # 访问对象（可能返回 None）
```

### 垃圾回收
```python
import gc
gc.collect()        # 手动触发
gc.disable()        # 禁用自动 GC
gc.get_stats()      # 查看统计
```

---

## 7. 标准库速查

### collections
```python
from collections import Counter, defaultdict, deque, namedtuple

Counter(['a', 'b', 'a'])  # {'a': 2, 'b': 1}
defaultdict(list)          # 访问不存在的 key 自动创建 []
deque(maxlen=5)            # 双端队列，自动丢弃旧元素
Point = namedtuple('Point', ['x', 'y'])
```

### functools
```python
from functools import lru_cache, partial, reduce

@lru_cache(maxsize=128)    # 缓存装饰器
def fib(n): ...

square = partial(pow, exp=2)  # 偏函数
reduce(lambda x, y: x+y, [1,2,3])  # 累积计算
```

### itertools
```python
from itertools import chain, combinations, permutations

chain([1,2], [3,4])       # [1,2,3,4]
combinations('abc', 2)    # ('a','b'), ('a','c'), ('b','c')
permutations('abc', 2)    # 所有排列
```

---

## 8. 设计模式速查

### 单例模式
```python
# 方式 1: __new__
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 方式 2: 装饰器
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
```

### 工厂模式
```python
class ShapeFactory:
    _registry = {'circle': Circle, 'rect': Rectangle}
    @classmethod
    def create(cls, shape_type, **kwargs):
        return cls._registry[shape_type](**kwargs)
```

### 观察者模式
```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}
    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
    def emit(self, event, *args):
        for cb in self._listeners.get(event, []):
            cb(*args)
```

---

## 9. 常见面试问答

### Q: Python 是解释型还是编译型？
A: 两者都有。Python 代码先编译成字节码（.pyc），再由解释器执行。

### Q: Python 的 GIL 是什么？
A: 全局解释器锁，确保同一时刻只有一个线程执行字节码。CPU 密集型用多进程，IO 密集型用多线程/异步。

### Q: 深拷贝和浅拷贝的区别？
A: 浅拷贝只复制外层，深拷贝递归复制所有层。

### Q: *args 和 **kwargs 的区别？
A: *args 接收位置参数（元组），**kwargs 接收关键字参数（字典）。

### Q: 列表推导式和生成器表达式的区别？
A: 列表推导式 [] 立即生成所有元素，生成器表达式 () 惰性求值。

### Q: 什么是猴子补丁（Monkey Patching）？
A: 运行时动态修改类或模块的行为。

---

*最后更新: 2026-05-30*
