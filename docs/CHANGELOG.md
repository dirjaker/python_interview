# 更新日志

> 本文档记录项目的所有重要变更。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [未发布]

### 计划中
- 行为型设计模式（观察者、策略、状态）
- 结构型设计模式（适配器、装饰器、代理）
- 在线代码运行功能
- 模拟面试功能
- 视频讲解

---

## [1.5.0] - 2026-06-22

### 新增
- 📄 创建 `docs/` 目录，生成完整技术文档
- 📄 新增 `docs/DEVELOPMENT.md` 开发指南
- 📄 新增 `docs/CHANGELOG.md` 更新日志
- 📄 新增 `docs/index.md` 完整技术参考手册

### 变更
- 📝 更新 `README.md`：新增项目简介、项目结构、贡献指南等内容
- 📝 保持原有 banner 图片和徽章风格不变

---

## [1.4.0] - 2026-06-xx

### 新增
- 🌐 新增第三方 API 调用最佳实践专题（`third_party_api/01_best_practices.py`）
  - 超时与重试策略（指数退避 + 抖动）
  - 熔断器模式（Circuit Breaker）
  - API Key 安全管理（密钥轮转、请求签名）
  - 限流处理（令牌桶、自适应限流）

---

## [1.3.0] - 2026-06-xx

### 新增
- 📝 统一 README 科技风格 + SVG Banner
- 📄 添加 MIT License
- 📄 添加 `CHEATSHEET.md` 面试速查表

### 变更
- 📝 统一 README 居中头部 + badges 风格
- 📝 优化 banner 布局，副标题改为中文项目名
- 📝 修复 banner 文字溢出，自适应字号

---

## [1.2.0] - 2026-06-xx

### 新增
- 🧪 添加 pytest 测试用例（`tests/test_all.py`）
  - 魔法方法测试（生命周期、字符串表示、容器协议、迭代器）
  - 装饰器测试（基础、带参数、类装饰器）
  - 标准库测试（Counter、defaultdict、deque、lru_cache）
  - 设计模式测试（单例、工厂、观察者）
  - 异步编程测试（协程、gather、Semaphore）

### 变更
- 🔧 删除 venv，添加 `requirements.txt`，统一使用 conda 环境

---

## [1.1.0] - 2026-06-xx

### 新增
- ⚡ 新增进阶主题模块
  - `advanced/01_gil.py`：GIL 原理与绕过
  - `advanced/02_metaclass.py`：元类编程
  - `advanced/03_memory.py`：内存管理与垃圾回收
- 📚 新增标准库模块
  - `stdlib/01_collections.py`：collections 高频用法
  - `stdlib/02_functools.py`：functools 高频用法

### 变更
- 🏗️ 重构为模块化目录结构
- 📝 添加详细中文注释

---

## [1.0.0] - 2026-06-xx

### 新增
- 🔮 魔法方法专题（5 个文件）
  - `01_lifecycle.py`：对象生命周期（`__new__` / `__init__` / `__del__`）
  - `02_string_comparison.py`：字符串表示与比较
  - `03_arithmetic_context.py`：算术运算与上下文管理器
  - `04_attribute_descriptor.py`：属性访问与描述符
  - `05_iterator_generator.py`：迭代器与生成器
- 🎭 装饰器专题（2 个文件）
  - `01_basic.py`：基础装饰器、wraps、带参装饰器、类装饰器
  - `02_advanced.py`：高级装饰器应用
- ⚡ 异步编程专题
  - `01_coroutine.py`：协程基础、gather、create_task、Semaphore、异步上下文管理器
- 🏗️ 设计模式专题
  - `01_creational.py`：单例、工厂、建造者、原型模式
- 🚀 `run_all.py` 主入口脚本

---

## 版本说明

- **新增（Added）**：新功能
- **变更（Changed）**：现有功能的变更
- **废弃（Deprecated）**：即将移除的功能
- **移除（Removed）**：已移除的功能
- **修复（Fixed）**：Bug 修复
- **安全（Security）**：安全相关的变更

---

*最后更新: 2026-06-22*
