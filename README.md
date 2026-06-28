<div align="center">

<img src="assets/banner.svg" width="100%" alt="Python 面试题精讲">

<br>

### 🐍 Python 面试题精讲

[![Stars](https://img.shields.io/github/stars/dirjaker/python_interview?style=flat-square&label=Stars&color=FFD700)](https://github.com/dirjaker/python_interview/stargazers)
[![Forks](https://img.shields.io/github/forks/dirjaker/python_interview?style=flat-square&label=Forks&color=4A90D9)](https://github.com/dirjaker/python_interview/network/members)
[![Contributors](https://img.shields.io/github/contributors/dirjaker/python_interview?style=flat-square&label=Contributors&color=8B4513)](https://github.com/dirjaker/python_interview/graphs/contributors)
[![License](https://img.shields.io/github/license/dirjaker/python_interview?style=flat-square&label=License&color=20B2AA)](https://github.com/dirjaker/python_interview/blob/dev/LICENSE)

</div>

---

## 📖 项目简介

一套系统化的 **Python 高级面试题库**，涵盖魔法方法、装饰器、异步编程、设计模式、GIL、元类、内存管理、标准库以及第三方 API 最佳实践等核心主题。每个模块都包含 **详细的中文注释**、**面试高频问答** 和 **可运行的代码示例**，适合面试前快速复习和深度学习。

## 🗺️ 学习指南

> 按优先级排序，面试前可以根据剩余时间选择性学习

### 🔥 必看（面试基本都会问）— 约 3.5 小时

| 文件 | 核心问题 | 时间 |
|------|---------|:--:|
| `magic_methods/01_lifecycle.py` | `__new__` vs `__init__`、单例模式 | 30min |
| `magic_methods/02_string_comparison.py` | `__str__` vs `__repr__`、`__eq__` vs `__hash__` | 30min |
| `magic_methods/04_attribute_descriptor.py` | `__getattr__` vs `__getattribute__`、property | 30min |
| `decorators/01_basic.py` | 装饰器本质、`functools.wraps` | 30min |
| `advanced/01_gil.py` | GIL 原理、怎么绕过 | 25min |
| `advanced/03_memory.py` | 引用计数、垃圾回收、`__slots__` | 35min |

### ⭐ 推荐看（区分度高的加分项）— 约 3 小时

| 文件 | 核心问题 | 时间 |
|------|---------|:--:|
| `magic_methods/03_arithmetic_context.py` | 运算符重载、上下文管理器 | 35min |
| `magic_methods/05_iterator_generator.py` | 迭代器 vs 生成器、`yield` | 30min |
| `decorators/02_advanced.py` | 装饰器叠加、异步装饰器 | 30min |
| `async_programming/01_coroutine.py` | 协程 vs 线程、asyncio | 40min |
| `advanced/02_metaclass.py` | 元类、`type` vs `object` | 40min |

### ✅ 有时间看（锦上添花）— 约 1.5 小时

| 文件 | 核心问题 | 时间 |
|------|---------|:--:|
| `stdlib/01_collections.py` | `defaultdict`、`Counter`、`deque` | 25min |
| `stdlib/02_functools.py` | `lru_cache`、`partial`、`reduce` | 20min |
| `patterns/01_creational.py` | 单例/工厂模式 | 30min |

### 📦 最后看（工程经验）— 约 1.5 小时

| 文件 | 核心问题 | 时间 |
|------|---------|:--:|
| `third_party_api/01_best_practices.py` | 超时重试、熔断、API Key 管理 | 1.5h |

> 💡 **快速路线**：🔥 必看 6 篇 ≈ 3 小时，加上 `CHEATSHEET.md`（15min），一共不到 4 小时覆盖面试核心。

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 🔮 **魔法方法** | `__init__`、`__new__`、`__call__`、`__del__`、描述符协议等深度解析 |
| 🎭 **装饰器** | 函数装饰器、类装饰器、装饰器工厂、`functools.wraps` |
| ⚡ **异步编程** | asyncio、协程、事件循环、Semaphore 限流、异步上下文管理器 |
| 🏗️ **设计模式** | 单例、工厂、建造者、原型、观察者等 Python 实现 |
| 🔒 **GIL 机制** | 全局解释器锁原理、多线程 vs 多进程 vs 异步对比 |
| 🧬 **元类编程** | `type`、`metaclass`、`__init_subclass__`、插件系统 |
| 💾 **内存管理** | 引用计数、垃圾回收、`__slots__`、弱引用、内存分析工具 |
| 📚 **标准库** | `collections`、`functools` 高频用法和面试考点 |
| 🌐 **第三方 API** | 超时/重试/熔断/限流/缓存/幂等/签名最佳实践 |

## 📁 项目结构

```
python_interview/
├── run_all.py                    # 主入口，一键运行所有演示
├── requirements.txt              # Python 依赖
├── README.md                     # 项目说明
├── CHEATSHEET.md                 # 面试速查表
├── assets/
│   └── banner.svg                # 项目 Banner
├── magic_methods/                # 魔法方法专题
│   ├── 01_lifecycle.py           # __new__ / __init__ / __del__ 生命周期
│   ├── 02_string_comparison.py   # __str__ / __repr__ / __eq__ / __hash__
│   ├── 03_arithmetic_context.py  # 算术运算符 / 上下文管理器
│   ├── 04_attribute_descriptor.py# 属性访问 / 描述符协议
│   └── 05_iterator_generator.py  # 迭代器 / 生成器
├── decorators/                   # 装饰器专题
│   ├── 01_basic.py               # 基础装饰器 / wraps / 带参装饰器 / 类装饰器
│   └── 02_advanced.py            # 高级装饰器应用
├── async_programming/            # 异步编程专题
│   └── 01_coroutine.py           # 协程 / gather / create_task / Semaphore
├── patterns/                     # 设计模式专题
│   └── 01_creational.py          # 单例 / 工厂 / 建造者 / 原型模式
├── advanced/                     # 进阶主题
│   ├── 01_gil.py                 # GIL 原理 / 多线程 vs 多进程
│   ├── 02_metaclass.py           # 元类 / type / __init_subclass__
│   └── 03_memory.py              # 引用计数 / __slots__ / weakref / tracemalloc
├── stdlib/                       # 标准库专题
│   ├── 01_collections.py         # Counter / defaultdict / deque / namedtuple
│   └── 02_functools.py           # lru_cache / partial / reduce / total_ordering
├── third_party_api/              # 第三方 API 专题
│   └── 01_best_practices.py      # 超时/重试/熔断/限流/缓存/签名
├── tests/                        # pytest 测试用例
│   └── test_all.py               # 全模块测试
└── docs/                         # 项目文档
    ├── DEVELOPMENT.md            # 开发指南
    └── CHANGELOG.md              # 更新日志
```

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/dirjaker/python_interview.git
cd python_interview

# 创建虚拟环境
conda create -n python_interview python=3.12 -y
conda activate python_interview

# 安装依赖
pip install -r requirements.txt

# 运行所有演示
python run_all.py

# 运行指定模块
python run_all.py magic        # 魔法方法
python run_all.py decorator    # 装饰器
python run_all.py async        # 异步编程
python run_all.py stdlib       # 标准库
python run_all.py pattern      # 设计模式
python run_all.py advanced     # 进阶主题

# 运行测试
pytest tests/ -v
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **运行环境** | Python 3.12+ |
| **异步框架** | asyncio、aiohttp |
| **测试框架** | pytest、pytest-asyncio |
| **内存分析** | pympler、tracemalloc |
| **文档引擎** | VitePress |
| **部署** | GitHub Pages |

## 📝 开发日志

- [x] 魔法方法专题（5 个文件）
- [x] 装饰器详解（2 个文件）
- [x] 异步编程指南
- [x] 设计模式实现（创建型）
- [x] GIL 深度分析
- [x] 元类编程专题
- [x] 内存管理与垃圾回收
- [x] 标准库高频用法
- [x] 第三方 API 最佳实践
- [x] pytest 测试用例
- [ ] 行为型 / 结构型设计模式
- [ ] 在线代码运行
- [ ] 模拟面试功能
- [ ] 视频讲解

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/xxx`
3. 提交修改：`git commit -m 'feat: add xxx'`
4. 推送分支：`git push origin feature/xxx`
5. 提交 Pull Request

## 📄 许可证

[MIT License](LICENSE)

---

<div align="center">

🔗 **GitHub**: [dirjaker/python_interview](https://github.com/dirjaker/python_interview)

⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！

</div>
