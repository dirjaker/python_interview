# Python 面试题 Demo 集合

面试准备：Python 高级特性的代码实现和演示。

## 📁 目录结构

```
python_interview/
├── run_all.py                    # 一键运行所有
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
└── patterns/                     # 设计模式（1 个文件）
    └── 01_creational.py          # 单例, 工厂, 建造者, 原型
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

# 直接运行单个文件
python magic_methods/01_lifecycle.py
python decorators/01_basic.py
```

## 📖 内容概览

### 魔法方法 (magic_methods/)
| 文件 | 内试考点 | 示例数 |
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

## 💡 学习建议

1. **先看注释** — 每个文件开头都有"面试高频问题"和"核心要点"
2. **运行代码** — 亲手运行，观察输出
3. **修改代码** — 尝试修改参数，理解行为变化
4. **面试问答** — 每个知识点都有"面试官问 → 标准答"格式

## 📚 配套文档

详细知识点请参考：`project_list/Python面试题精讲-技术文档.md`

## ⚠️ 注意事项

- 异步编程文件需要 Python 3.7+
- 部分示例使用了 `time.sleep()` 模拟耗时操作
- 运行前确保在项目目录下
