# Python 面试题精讲 — 完整技术文档

> 本文档是项目的完整技术参考手册，涵盖所有模块的详细说明、核心原理和面试考点。

---

## 目录

- [一、魔法方法](#一魔法方法)
- [二、装饰器](#二装饰器)
- [三、异步编程](#三异步编程)
- [四、设计模式](#四设计模式)
- [五、GIL 机制](#五gil-机制)
- [六、元类编程](#六元类编程)
- [七、内存管理](#七内存管理)
- [八、标准库](#八标准库)
- [九、第三方 API 最佳实践](#九第三方-api-最佳实践)

---

## 一、魔法方法

> 对应目录：`magic_methods/`

魔法方法（Magic Methods / Dunder Methods）是 Python 中以双下划线开头和结尾的特殊方法，让类能够支持运算符重载、容器协议、上下文管理器等高级特性。

### 1.1 对象生命周期（01_lifecycle.py）

#### 面试高频问题

1. `__new__` 和 `__init__` 的区别是什么？
2. 什么时候需要重写 `__new__`？
3. Python 的单例模式怎么实现？

#### 核心知识点

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        """创建实例（在 __init__ 之前调用），必须返回实例"""
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        """初始化实例，不返回任何值"""
        self.value = value

    def __del__(self):
        """析构函数（引用计数为 0 时调用）"""
        pass
```

**调用顺序**：`__new__` → `__init__` → 使用对象 → `__del__`

| 方法 | 类型 | 返回值 | 用途 |
|------|------|--------|------|
| `__new__` | 静态方法 | 必须返回实例 | 控制实例创建（单例、不可变类型） |
| `__init__` | 实例方法 | 返回 None | 初始化实例属性 |
| `__del__` | 实例方法 | 忽略 | 资源清理（不推荐依赖） |

#### 本模块实现的示例

| 类 | 功能 |
|------|------|
| `LifecycleDemo` | 演示对象从创建到销毁的完整生命周期 |
| `Singleton` | 通过 `__new__` 实现单例模式 |
| `DatabaseConnection` | 通过装饰器实现单例模式 |
| `ImmutablePoint` | 在 `__new__` 中设置值实现不可变类型 |
| `Shape` | 通过类方法实现工厂模式 |

---

### 1.2 字符串表示与比较（02_string_comparison.py）

#### 面试高频问题

1. `__str__` 和 `__repr__` 的区别？
2. 实现 `__eq__` 后 `__hash__` 会怎样？
3. `functools.total_ordering` 怎么用？

#### 核心知识点

```python
def __str__(self):    # print() / str() 调用，面向用户
    return "可读"
def __repr__(self):   # repr() / 交互式环境，面向开发者
    return "ClassName(...)"
```

**关键规则**：
- 只实现一个时，优先实现 `__repr__`
- `__str__` 默认回退到 `__repr__`
- 实现 `__eq__` 后 `__hash__` 被设为 `None`（除非显式实现）
- `@functools.total_ordering`：只需 `__eq__` + 一个比较方法，自动生成其余

#### 容器协议

```python
def __len__(self):           # len(obj)
def __getitem__(self, k):    # obj[k]
def __setitem__(self, k, v): # obj[k] = v
def __contains__(self, item):# item in obj
def __iter__(self):          # for x in obj
```

---

### 1.3 算术运算与上下文管理器（03_arithmetic_context.py）

#### 核心知识点

**算术运算符重载**：

| 方法 | 运算符 | 说明 |
|------|--------|------|
| `__add__` | `+` | 加法 |
| `__radd__` | `+` | 右加法（左操作数不支持时） |
| `__iadd__` | `+=` | 原地加法 |
| `__mul__` | `*` | 乘法 |
| `__truediv__` | `/` | 真除法 |
| `__floordiv__` | `//` | 整除 |
| `__mod__` | `%` | 取模 |
| `__pow__` | `**` | 幂 |
| `__neg__` | `-x` | 取负 |
| `__abs__` | `abs()` | 绝对值 |

**上下文管理器**：

```python
def __enter__(self):      # with obj: 进入时调用
    return self
def __exit__(self, *exc): # 离开 with 块时调用
    return False  # True=吞异常，False=传播异常
```

---

### 1.4 属性访问与描述符（04_attribute_descriptor.py）

#### 属性查找顺序

`__getattribute__` → 数据描述符 → 实例字典 → 类字典 → `__getattr__`

| 方法 | 触发时机 |
|------|----------|
| `__getattr__` | 属性不存在时才调用 |
| `__getattribute__` | 每次访问都调用（容易死循环） |
| `__setattr__` | 设置属性时调用 |
| `__delattr__` | 删除属性时调用 |

#### 描述符协议

```python
class Descriptor:
    def __get__(self, obj, objtype):  # 访问属性
    def __set__(self, obj, value):    # 设置属性
    def __delete__(self, obj):        # 删除属性
```

`@property` 是描述符的语法糖。

---

### 1.5 迭代器与生成器（05_iterator_generator.py）

#### 迭代器协议

```python
class MyIterator:
    def __iter__(self):    # 返回迭代器对象（通常是 self）
        return self
    def __next__(self):    # 返回下一个值，无值时 raise StopIteration
        ...
```

#### 生成器

```python
def fibonacci(n):
    """惰性求值，逐个产生值"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

**面试考点**：
- 生成器表达式 `()` vs 列表推导式 `[]`：惰性 vs 立即生成
- `yield from` 委托给子生成器
- 生成器只能遍历一次

---

## 二、装饰器

> 对应目录：`decorators/`

### 2.1 基础装饰器（01_basic.py）

#### 面试高频问题

1. 什么是装饰器？本质是什么？
2. `functools.wraps` 有什么用？
3. 装饰器的执行时机？

#### 核心知识点

```python
def my_decorator(func):
    @functools.wraps(func)  # 保留原函数的元信息！
    def wrapper(*args, **kwargs):
        # 前置逻辑
        result = func(*args, **kwargs)
        # 后置逻辑
        return result
    return wrapper
```

**本质**：接受函数作为参数，返回新函数的高阶函数

**执行时机**：装饰器在**定义函数时**执行（不是调用时）

#### 带参数的装饰器（三层嵌套）

```python
def repeat(n=2):          # 最外层：接受装饰器参数
    def decorator(func):  # 中间层：接受被装饰的函数
        def wrapper(*args, **kwargs):  # 最内层：实际执行
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```

#### 类装饰器

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

#### 本模块实现的装饰器

| 装饰器 | 类型 | 功能 |
|--------|------|------|
| `timer` | 函数装饰器 | 测量函数执行时间 |
| `logger` | 函数装饰器 | 记录函数调用日志 |
| `repeat(n)` | 带参装饰器 | 重复执行 n 次 |
| `validate_types` | 带参装饰器 | 参数类型验证 |
| `CountCalls` | 类装饰器 | 记录调用次数 |
| `Memoize` | 类装饰器 | 自动缓存结果 |

---

## 三、异步编程

> 对应目录：`async_programming/`

### 3.1 协程基础与并发模式（01_coroutine.py）

#### 面试高频问题

1. 协程和线程的区别？
2. asyncio 的核心组件是什么？
3. 为什么异步代码有时比同步还慢？

#### 协程 vs 线程

| 特性 | 协程 | 线程 |
|------|------|------|
| 调度 | 协作式（主动让出） | 抢占式（OS 调度） |
| 切换 | 用户态，纳秒级 | 内核态，微秒级 |
| 并发 | 单线程内并发 | 多线程并发 |
| 竞态 | 不存在（单线程） | 需要锁 |
| 适用场景 | IO 密集型 | IO + CPU 混合 |

#### 核心 API

| API | 功能 |
|-----|------|
| `asyncio.run()` | 运行入口协程 |
| `asyncio.gather()` | 并发执行，按顺序返回 |
| `asyncio.create_task()` | 创建任务，立即开始执行 |
| `asyncio.as_completed()` | 按完成顺序返回 |
| `asyncio.wait_for()` | 超时控制 |
| `asyncio.Semaphore()` | 限制并发数 |

#### 异步上下文管理器

```python
class AsyncDB:
    async def __aenter__(self):
        """异步进入"""
        await asyncio.sleep(0.1)
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出"""
        await asyncio.sleep(0.1)
```

#### 异步迭代器和生成器

```python
# 异步迭代器：实现 __aiter__ 和 __anext__
# 异步生成器：使用 async def + yield
async def async_generator(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i
```

---

## 四、设计模式

> 对应目录：`patterns/`

### 4.1 创建型模式（01_creational.py）

#### 面试高频问题

1. 单例模式有哪些实现方式？
2. 工厂模式和抽象工厂的区别？
3. Python 中哪些地方用到了设计模式？

#### 单例模式（4 种实现）

| 方式 | 实现 | 优缺点 |
|------|------|--------|
| `__new__` | 重写 `__new__`，缓存实例 | 简单，但子类需要额外处理 |
| 装饰器 | 闭包缓存实例 | 可复用，Pythonic |
| 模块级变量 | 模块天然单例 | 最简单，推荐 |
| 元类 | `__call__` 控制 | 最强大，可拦截所有创建 |

#### 工厂模式

```python
class ShapeFactory:
    _registry = {'circle': Circle, 'rect': Rectangle}
    @classmethod
    def create(cls, shape_type, **kwargs):
        return cls._registry[shape_type](**kwargs)
```

#### 建造者模式

链式调用构建复杂对象：

```python
query = (QueryBuilder()
    .select("name", "age")
    .from_table("users")
    .where("age > 18")
    .order_by("name")
    .limit(10)
    .build())
```

#### 原型模式

```python
import copy
shallow = copy.copy(obj)       # 浅拷贝
deep = copy.deepcopy(obj)      # 深拷贝
```

---

## 五、GIL 机制

> 对应目录：`advanced/01_gil.py`

### 面试高频问题

1. 什么是 GIL？为什么需要它？
2. GIL 对多线程有什么影响？
3. 怎么绕过 GIL？

### 核心知识点

**GIL（Global Interpreter Lock）**：CPython 解释器中的互斥锁，同一时刻只有一个线程执行 Python 字节码。

#### GIL 的影响

| 任务类型 | 多线程效果 | 推荐方案 |
|---------|-----------|---------|
| CPU 密集型 | ❌ 无效甚至更慢 | 多进程 |
| IO 密集型 | ✅ 有效 | 多线程/异步 |

#### 绕过 GIL 的方法

| 方法 | 适用场景 | 说明 |
|------|---------|------|
| 多进程 | CPU 密集型 | 每个进程独立 GIL |
| C 扩展 | 数值计算 | numpy 等自动释放 GIL |
| asyncio | IO 密集型 | 单线程并发，无竞态 |
| 其他解释器 | 特殊场景 | Jython/IronPython 无 GIL |
| Python 3.13+ free-threaded | 实验性 | `--disable-gil` |

#### 多线程 vs 多进程 vs 异步对比

| 特性 | 多线程 | 多进程 | 异步 |
|------|--------|--------|------|
| 并发模型 | 抢占式 | 独立进程 | 协作式 |
| GIL 影响 | 有 | 无 | 无 |
| 适用场景 | IO 密集型 | CPU 密集型 | IO 密集型 |
| 内存开销 | 小 | 大 | 最小 |
| 竞态条件 | 需要注意 | 不存在 | 不存在 |

---

## 六、元类编程

> 对应目录：`advanced/02_metaclass.py`

### 面试高频问题

1. 什么是元类？类和对象的关系是什么？
2. `type` 和 `object` 的关系是什么？
3. `__new__` 和 `__init_subclass__` 的区别？

### 核心知识点

#### type 和 object 的关系

```
type(object)  → <class 'type'>
type(type)    → <class 'type'>
type 继承自 object
object 是 type 的实例
type 是自己的实例（循环关系）
```

#### 动态创建类

```python
Dog = type('Dog', (object,), {
    'species': 'Canine',
    'bark': lambda self: 'Woof!',
})
```

#### 自定义元类

| 元类 | 功能 |
|------|------|
| `ValidationMeta` | 验证类定义（检查方法、命名） |
| `RegistrationMeta` | 自动注册子类 |
| `SingletonMeta` | 通过 `__call__` 实现单例 |

#### 元类 vs `__init_subclass__`

| 特性 | 元类 | `__init_subclass__` |
|------|------|---------------------|
| 适用版本 | 所有版本 | Python 3.6+ |
| 复杂度 | 高 | 低 |
| 拦截范围 | 整个类创建过程 | 子类创建后 |
| 控制实例创建 | 可以（`__call__`） | 不可以 |

---

## 七、内存管理

> 对应目录：`advanced/03_memory.py`

### 面试高频问题

1. Python 的内存管理机制是什么？
2. 引用计数和垃圾回收的关系？
3. `__slots__` 有什么用？

### 核心知识点

#### 引用计数（主要机制）

- 每个对象都有引用计数器
- 引用计数为 0 时立即释放
- 优点：实时性好
- 缺点：无法处理循环引用

#### 垃圾回收（分代收集）

- 3 代收集算法
- 处理循环引用
- 手动触发：`gc.collect()`

#### `__slots__`

```python
class Point:
    __slots__ = ['x', 'y']  # 减少内存 30%-50%
```

**限制**：不能动态添加未声明的属性

#### 弱引用

```python
import weakref
ref = weakref.ref(obj)
ref()  # 访问对象（可能返回 None）
```

**适用场景**：缓存、观察者模式、避免内存泄漏

#### 内存分析工具

| 工具 | 用途 |
|------|------|
| `sys.getsizeof()` | 查看单个对象大小 |
| `tracemalloc` | 追踪内存分配 |
| `pympler` | 详细内存分析 |
| `memory_profiler` | 逐行分析内存 |
| `objgraph` | 可视化对象引用 |

---

## 八、标准库

> 对应目录：`stdlib/`

### 8.1 collections 模块（01_collections.py）

| 数据结构 | 用途 | 时间复杂度 |
|---------|------|-----------|
| `Counter` | 统计元素出现次数 | O(n) |
| `defaultdict` | 带默认值的字典 | O(1) |
| `deque` | 双端队列 | 两端 O(1) |
| `namedtuple` | 命名元组 | — |
| `OrderedDict` | 有序字典 | — |
| `ChainMap` | 链式映射 | — |

### 8.2 functools 模块（02_functools.py）

| 工具 | 用途 |
|------|------|
| `lru_cache` | LRU 缓存装饰器 |
| `partial` | 偏函数，固定部分参数 |
| `reduce` | 累积计算 |
| `total_ordering` | 自动生成比较方法 |
| `wraps` | 保留被装饰函数的元信息 |

---

## 九、第三方 API 最佳实践

> 对应目录：`third_party_api/`

### 面试高频问题

1. 调用第三方 API 时如何处理超时和重试？
2. 什么是熔断器模式？
3. 如何安全地管理 API Key？
4. 如何处理限流（Rate Limiting）？
5. 如何保证 API 调用的幂等性？

### 核心组件

#### 超时与重试

- **指数退避 + 抖动**：避免惊群效应
- **可重试错误**：网络错误、5xx、429
- **不可重试错误**：4xx（除 429）

```python
@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    exponential_base: float = 2.0
    jitter: bool = True
```

#### 熔断器模式（Circuit Breaker）

| 状态 | 说明 |
|------|------|
| CLOSED（关闭） | 请求正常通过 |
| OPEN（打开） | 直接快速失败 |
| HALF_OPEN（半开） | 允许少量请求试探 |

#### 限流器

- **令牌桶**：允许突发流量
- **漏桶**：平滑流量
- **自适应限流**：根据服务端响应动态调整（类似 TCP AIMD）

#### API Key 安全管理

- 环境变量 > 配置文件 > 硬编码
- 支持 Key 轮转（新旧并行期）
- HMAC-SHA256 请求签名

---

## 附录：常见面试问答

### Q: Python 是解释型还是编译型？
A: 两者都有。Python 代码先编译成字节码（.pyc），再由解释器执行。

### Q: Python 的 GIL 是什么？
A: 全局解释器锁，确保同一时刻只有一个线程执行字节码。CPU 密集型用多进程，IO 密集型用多线程/异步。

### Q: 深拷贝和浅拷贝的区别？
A: 浅拷贝只复制外层，深拷贝递归复制所有层。

### Q: *args 和 **kwargs 的区别？
A: `*args` 接收位置参数（元组），`**kwargs` 接收关键字参数（字典）。

### Q: 列表推导式和生成器表达式的区别？
A: 列表推导式 `[]` 立即生成所有元素，生成器表达式 `()` 惰性求值。

### Q: 什么是猴子补丁（Monkey Patching）？
A: 运行时动态修改类或模块的行为。

---

*最后更新: 2026-06-22*
