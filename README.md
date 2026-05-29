# Python 面试题 Demo 集合

面试准备：Python 高级特性的代码实现和演示

## 📁 文件结构

```
python_interview/
├── 01_magic_methods.py      # 魔法方法完整演示
├── 02_decorators.py         # 装饰器完整演示
├── 03_async_programming.py  # 异步编程完整演示
├── 04_stdlib_and_patterns.py # 标准库和设计模式
└── README.md
```

## 🎯 内容概览

### 01_magic_methods.py — 魔法方法
- 对象生命周期 (`__new__`, `__init__`, `__del__`)
- 字符串表示 (`__str__`, `__repr__`)
- 比较运算符 (`__eq__`, `__lt__`, `__gt__`)
- 算术运算符 (`__add__`, `__mul__`, `__neg__`)
- 容器协议 (`__len__`, `__getitem__`, `__contains__`)
- 可调用对象 (`__call__`)
- 上下文管理器 (`__enter__`, `__exit__`)
- 属性访问控制 (`__getattr__`, `__setattr__`)
- 描述符协议 (`__get__`, `__set__`)
- 迭代器协议 (`__iter__`, `__next__`)

### 02_decorators.py — 装饰器
- 基础装饰器 (`@timer`, `@logger`)
- 带参数装饰器 (`@retry`, `@rate_limit`)
- 类装饰器 (`@Singleton`, `@CountCalls`)
- `functools.wraps` 的作用
- 属性装饰器 (`@property`)
- 注册装饰器
- 异步装饰器

### 03_async_programming.py — 异步编程
- 协程基础 (`async/await`)
- 并发执行 (`asyncio.gather`)
- Task 和 `create_task`
- 异步上下文管理器
- 异步迭代器和生成器
- 异步队列
- 超时控制
- Semaphore 限流
- 异步锁
- 异步异常处理

### 04_stdlib_and_patterns.py — 标准库和设计模式
- `collections` (Counter, defaultdict, deque, namedtuple)
- `itertools` (chain, product, permutations, combinations)
- `functools` (lru_cache, partial, reduce, total_ordering)
- `dataclasses`
- `enum`
- `pathlib`
- `re` (正则表达式)
- `json`
- `logging`
- `hashlib`
- 常见数据结构 (LRU Cache, 堆, 二分查找)
- 设计模式 (单例, 观察者, 策略)

## 🚀 运行方式

```bash
# 运行单个文件
python 01_magic_methods.py
python 02_decorators.py
python 03_async_programming.py
python 04_stdlib_and_patterns.py
```

## 📖 配套文档

详细知识点请参考：`project_list/Python面试题精讲-技术文档.md`

## 💡 面试要点

1. **魔法方法**: 理解 `__new__` vs `__init__`, 描述符协议, 上下文管理器
2. **装饰器**: 能手写装饰器, 理解 `functools.wraps` 的作用
3. **异步编程**: 理解协程, Task, asyncio 的核心概念
4. **GIL**: 知道 GIL 是什么, 如何绕过
5. **内存管理**: 引用计数, 垃圾回收, `__slots__`
6. **设计模式**: 单例, 工厂, 观察者, 策略模式
