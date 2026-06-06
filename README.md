<div align="center">

# 🐍 Python Interview

### Python 面试题全集

[![专题](https://img.shields.io/badge/专题-5-blue?style=flat-square)]()
[![题目](https://img.shields.io/badge/题目-40+-green?style=flat-square)]()
[![语言](https://img.shields.io/badge/语言-Python 3.12-orange?style=flat-square)]()
[![更新](https://img.shields.io/badge/更新-2025.06-red?style=flat-square)]()

*数据结构 · 并发编程 · OOP · 装饰器 · 元类 · 面试高频题*

</div>

---

# Python 面试题 Demo 集合

面试准备：Python 高级特性的代码实现和演示。

## 📁 目录结构

```
python_interview/
├── run_all.py                    # 一键运行所有
├── CHEATSHEET.md                 # 面试速查表（面试前 30 分钟看）
├── README.md
│
├── magic_methods/                # 魔法方法（5 个文件）
│   ├── 01_lifecycle.py           # __new__, __init__, __del__, 单例模式
│   ├── 02_string_comparison.py   # __str__, __repr__, __eq__, __hash__, 容器协议
│   ├── 03_arithmetic_context.py  # 算术运算符, __call__, 上下文管理器
│   ├── 04_attribute_descriptor.py # __getattr__, 描述符, property
│   └── 05_iterator_generator.py  # 迭代器, 生成器, yield from, send()
│
├── decorators/                   # 装饰器（2 个文件）
│   ├── 01_basic.py               # 基础装饰器, functools.wraps, 带参数装饰器
│   └── 02_advanced.py            # 装饰器叠加, 重试, 限流, 异步装饰器
│
├── async_programming/            # 异步编程（1 个文件）
│   └── 01_coroutine.py           # 协程, gather, create_task, Semaphore
│
├── stdlib/                       # 标准库（2 个文件）
│   ├── 01_collections.py         # Counter, defaultdict, deque, namedtuple
│   └── 02_functools.py           # lru_cache, partial, reduce, total_ordering
│
├── patterns/                     # 设计模式（1 个文件）
│   └── 01_creational.py          # 单例, 工厂, 建造者, 原型
│
├── advanced/                     # 进阶主题（3 个文件）
│   ├── 01_gil.py                 # GIL 原理与绕过
│   ├── 02_metaclass.py           # 元类 (metaclass)
│   └── 03_memory.py              # 内存管理与垃圾回收
│
└── tests/                        # 测试用例
    └── test_all.py               # pytest 测试
```

## 🚀 运行方式

```bash
# 运行所有演示
python run_all.py

# 运行指定模块
python run_all.py magic        # 魔法方法
python run_all.py decorator    # 装饰器
python run_all.py async        # 异步编程
python run_all.py stdlib       # 标准库
python run_all.py pattern      # 设计模式
python run_all.py advanced     # 进阶主题

# 直接运行单个文件
python magic_methods/01_lifecycle.py

# 运行测试
pytest tests/ -v
```

## 📖 内容概览

### 魔法方法 (magic_methods/)
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_lifecycle | __new__ vs __init__, 单例模式, 不可变类型 | 5 |
| 02_string_comparison | __str__ vs __repr__, __eq__/__hash__, 容器协议 | 3 |
| 03_arithmetic_context | 算术运算符, __call__, 上下文管理器 | 3 |
| 04_attribute_descriptor | __getattr__, 描述符, property | 3 |
| 05_iterator_generator | 迭代器, 生成器, yield from, send() | 5 |

### 装饰器 (decorators/)
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_basic | 基础装饰器, functools.wraps, 带参数装饰器, 类装饰器 | 5 |
| 02_advanced | 装饰器叠加, 重试, 限流, 异步装饰器, 注册表 | 5 |

### 异步编程 (async_programming/)
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_coroutine | 协程, gather, create_task, as_completed, Semaphore | 8 |

### 标准库 (stdlib/)
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_collections | Counter, defaultdict, deque, namedtuple, ChainMap | 5 |
| 02_functools | lru_cache, partial, reduce, total_ordering | 4 |

### 设计模式 (patterns/)
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_creational | 单例, 工厂, 建造者, 原型 | 4 |

### 进阶主题 (advanced/) 🆕
| 文件 | 面试考点 | 示例数 |
|------|----------|--------|
| 01_gil | GIL 原理, CPU/IO 密集型, 多进程绕过 | 6 |
| 02_metaclass | type/object, 动态创建类, 元类, __init_subclass__ | 7 |
| 03_memory | 引用计数, 循环引用, __slots__, weakref | 6 |

## 💡 学习建议

1. **先看 CHEATSHEET.md** — 面试前 30 分钟快速复习
2. **再看注释** — 每个文件开头都有"面试高频问题"和"核心要点"
3. **运行代码** — 亲手运行，观察输出
4. **修改代码** — 尝试修改参数，理解行为变化
5. **跑测试** — `pytest tests/ -v` 验证理解

## 📚 配套文档

详细知识点请参考：`project_list/Python面试题精讲-技术文档.md`

## ⚠️ 注意事项

- 异步编程文件需要 Python 3.7+
- 部分示例使用了 `time.sleep()` 模拟耗时操作
- 运行前确保在项目目录下
- 测试需要安装 pytest: `pip install pytest pytest-asyncio`

