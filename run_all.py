"""
Python 面试题 Demo 集合 - 主入口
==================================

一键运行所有演示，或单独运行某个模块。

用法:
    python run_all.py              # 运行所有
    python run_all.py magic        # 只运行魔法方法
    python run_all.py decorator    # 只运行装饰器
    python run_all.py async        # 只运行异步编程
    python run_all.py stdlib       # 只运行标准库
    python run_all.py pattern      # 只运行设计模式
    python run_all.py advanced     # 只运行进阶主题
"""

import sys
import os
import importlib
import subprocess


# 模块配置
MODULES = {
    "magic": {
        "name": "魔法方法",
        "files": [
            "magic_methods.01_lifecycle",
            "magic_methods.02_string_comparison",
            "magic_methods.03_arithmetic_context",
            "magic_methods.04_attribute_descriptor",
            "magic_methods.05_iterator_generator",
        ]
    },
    "decorator": {
        "name": "装饰器",
        "files": [
            "decorators.01_basic",
            "decorators.02_advanced",
        ]
    },
    "async": {
        "name": "异步编程",
        "files": [
            "async_programming.01_coroutine",
        ]
    },
    "stdlib": {
        "name": "标准库",
        "files": [
            "stdlib.01_collections",
            "stdlib.02_functools",
        ]
    },
    "pattern": {
        "name": "设计模式",
        "files": [
            "patterns.01_creational",
        ]
    },
    "advanced": {
        "name": "进阶主题",
        "files": [
            "advanced.01_gil",
            "advanced.02_metaclass",
            "advanced.03_memory",
        ]
    },
}


def run_file(file_path):
    """运行单个 Python 文件"""
    # 将模块路径转换为文件路径
    path = file_path.replace('.', '/') + '.py'
    if os.path.exists(path):
        subprocess.run([sys.executable, path], check=True)
    else:
        print(f"  ⚠️ 文件不存在: {path}")


def run_module(module_name, files):
    """运行一个模块的所有文件"""
    print("\n" + "=" * 70)
    print(f"  {module_name}")
    print("=" * 70)

    for file_path in files:
        try:
            print(f"\n--- {file_path} ---")
            run_file(file_path)
        except Exception as e:
            print(f"  ❌ Error running {file_path}: {e}")


def list_modules():
    """列出所有可用模块"""
    print("\n可用模块:")
    for key, info in MODULES.items():
        print(f"  {key:12} - {info['name']}")
    print()


def main():
    # 添加当前目录到 Python 路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        # 运行所有
        print("🚀 运行所有 Python 面试题 Demo\n")
        for key, info in MODULES.items():
            run_module(info["name"], info["files"])
    elif sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        list_modules()
    elif sys.argv[1] in MODULES:
        # 运行指定模块
        info = MODULES[sys.argv[1]]
        run_module(info["name"], info["files"])
    else:
        print(f"❌ 未知模块: {sys.argv[1]}")
        list_modules()
        sys.exit(1)


if __name__ == "__main__":
    main()
