# 开发指南

> 本文档面向项目开发者，包含环境搭建、代码规范、测试方法和贡献流程。

---

## 目录

- [环境要求](#环境要求)
- [快速搭建](#快速搭建)
- [项目结构](#项目结构)
- [运行指南](#运行指南)
- [测试指南](#测试指南)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [发布流程](#发布流程)

---

## 环境要求

| 依赖 | 版本要求 |
|------|---------|
| Python | 3.12+ |
| conda | 最新版（推荐）或 venv |
| Git | 2.0+ |

## 快速搭建

```bash
# 1. 克隆仓库
git clone https://github.com/dirjaker/python_interview.git
cd python_interview

# 2. 创建并激活 conda 环境
conda create -n python_interview python=3.12 -y
conda activate python_interview

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证安装
python run_all.py --help
```

### 使用 venv（备选方案）

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## 项目结构

```
python_interview/
├── run_all.py                    # 主入口
├── requirements.txt              # Python 依赖
├── README.md                     # 项目说明
├── CHEATSHEET.md                 # 面试速查表
├── assets/                       # 静态资源
├── magic_methods/                # 魔法方法模块
├── decorators/                   # 装饰器模块
├── async_programming/            # 异步编程模块
├── patterns/                     # 设计模式模块
├── advanced/                     # 进阶主题模块
├── stdlib/                       # 标准库模块
├── third_party_api/              # 第三方 API 模块
├── tests/                        # 测试目录
└── docs/                         # 文档目录
```

### 模块配置

`run_all.py` 中的 `MODULES` 字典定义了所有模块的映射关系：

```python
MODULES = {
    "magic":     {"name": "魔法方法",   "files": [...]},
    "decorator": {"name": "装饰器",     "files": [...]},
    "async":     {"name": "异步编程",   "files": [...]},
    "stdlib":    {"name": "标准库",     "files": [...]},
    "pattern":   {"name": "设计模式",   "files": [...]},
    "advanced":  {"name": "进阶主题",   "files": [...]},
}
```

## 运行指南

### 运行所有演示

```bash
python run_all.py
```

### 运行指定模块

```bash
python run_all.py magic        # 魔法方法
python run_all.py decorator    # 装饰器
python run_all.py async        # 异步编程
python run_all.py stdlib       # 标准库
python run_all.py pattern      # 设计模式
python run_all.py advanced     # 进阶主题
```

### 直接运行单个文件

```bash
python magic_methods/01_lifecycle.py
python decorators/01_basic.py
python async_programming/01_coroutine.py
```

### 查看帮助

```bash
python run_all.py --help
```

## 测试指南

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试类

```bash
pytest tests/test_all.py::TestLifecycle -v
pytest tests/test_all.py::TestDecorators -v
pytest tests/test_all.py::TestAsync -v
```

### 运行异步测试

异步测试需要 `pytest-asyncio` 插件（已在 `requirements.txt` 中声明）：

```bash
pytest tests/test_all.py::TestAsync -v
```

### 查看测试覆盖率

```bash
pip install pytest-cov
pytest tests/ -v --cov=. --cov-report=term-missing
```

## 代码规范

### 文件命名

- 模块目录：`snake_case`（如 `magic_methods`）
- 源文件：`数字_描述.py`（如 `01_lifecycle.py`）
- 测试文件：`test_xxx.py`
- `__init__.py`：每个模块目录都需要

### 代码风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 使用 4 空格缩进，不用 Tab
- 行宽不超过 100 字符
- 使用双引号字符串

### 文档注释

每个文件必须包含：

```python
"""
模块名称 — 简短描述
=========================

面试高频问题:
1. 问题 1？
2. 问题 2？
3. 问题 3？

核心要点:
- 要点 1
- 要点 2
- 要点 3
"""
```

每个函数/类必须包含：

```python
def function_name(args):
    """
    函数描述

    Args:
        arg1: 参数说明

    Returns:
        返回值说明

    运行结果:
        预期输出示例
    """
```

### 面试考点注释

使用以下格式标注面试考点：

```python
# 面试官问: xxx？
#
# 标准答:
# 回答内容...
```

## 提交规范

### 分支策略

- `main`：稳定版本
- `dev`：开发分支
- `feature/xxx`：功能分支
- `fix/xxx`：修复分支

### Commit 消息格式

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

**示例**：

```
feat(magic_methods): 新增描述符协议专题

- 添加 04_attribute_descriptor.py
- 实现 Property 描述符示例
- 包含数据描述符和非数据描述符对比

Closes #12
```

## 发布流程

1. 确保所有测试通过：`pytest tests/ -v`
2. 更新 `docs/CHANGELOG.md`
3. 合并到 `main` 分支
4. 打 Git Tag：`git tag v1.x.x`
5. 推送到远程：`git push origin main --tags`

---

## 依赖说明

| 包名 | 用途 |
|------|------|
| `aiohttp` | 异步 HTTP 客户端 |
| `Pympler` | 内存分析工具 |
| `typing_extensions` | 类型注解扩展 |
| `pytest` | 测试框架 |
| `pytest-asyncio` | 异步测试支持 |

---

## 常见问题

### Q: 运行时报 `ModuleNotFoundError`
A: 确保在项目根目录运行，并且已激活正确的 conda/venv 环境。

### Q: 异步测试报错
A: 确保安装了 `pytest-asyncio`，并在测试中使用 `@pytest.mark.asyncio` 装饰器。

### Q: 内存分析模块报错
A: 确保安装了 `pympler`：`pip install pympler`

---

*最后更新: 2026-06-22*
