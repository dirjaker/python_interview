"""
进阶 01: GIL 原理与绕过
=========================

面试高频问题:
1. 什么是 GIL？为什么需要它？
2. GIL 对多线程有什么影响？
3. 怎么绕过 GIL？

核心要点:
- GIL (Global Interpreter Lock): 全局解释器锁，CPython 的特性
- 同一时刻只有一个线程执行 Python 字节码
- IO 密集型: 多线程有效（等待 IO 时释放 GIL）
- CPU 密集型: 多线程无效（需要多进程或 C 扩展）
"""


import time
import threading
import multiprocessing
import concurrent.futures
from functools import reduce
import operator


# ============================================================
# 1. GIL 是什么？
# ============================================================
# 面试官问: 什么是 GIL？
#
# 标准答:
# GIL (Global Interpreter Lock) 是 CPython 解释器中的一个互斥锁：
# - 同一时刻只有一个线程执行 Python 字节码
# - 主要是为了保护 Python 对象的内存管理（引用计数）
# - 避免多线程同时修改引用计数导致的竞态条件
#
# GIL 的影响:
# - CPU 密集型任务: 多线程不能利用多核，甚至比单线程更慢
# - IO 密集型任务: 多线程仍然有效（等待 IO 时会释放 GIL）
# - C 扩展: 可以在执行 C 代码时释放 GIL（如 numpy）
#
# Python 3.13+ 的变化:
# - 引入了实验性的 free-threaded 模式（--disable-gil）
# - 但目前还不稳定，不建议在生产环境使用
# ============================================================


# ============================================================
# 2. GIL 对 CPU 密集型任务的影响
# ============================================================

def cpu_bound(n):
    """CPU 密集型任务：计算累加和"""
    return sum(range(n))


def demo_gil_cpu_bound():
    """
    演示 GIL 对 CPU 密集型任务的影响

    运行结果（典型）:
        单线程: 2.50s
        多线程: 2.55s  ← 没有加速！甚至更慢（线程切换开销）
        多进程: 1.30s  ← 真正利用多核
    """
    print("=" * 60)
    print("1. GIL 对 CPU 密集型任务的影响")
    print("=" * 60)

    n = 10_000_000
    tasks = [n] * 4

    # 单线程
    start = time.perf_counter()
    results = [cpu_bound(t) for t in tasks]
    single_time = time.perf_counter() - start
    print(f"单线程: {single_time:.2f}s")

    # 多线程
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound, tasks))
    multi_thread_time = time.perf_counter() - start
    print(f"多线程: {multi_thread_time:.2f}s")

    # 多进程
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound, tasks))
    multi_process_time = time.perf_counter() - start
    print(f"多进程: {multi_process_time:.2f}s")

    print(f"\n结论: CPU 密集型任务用多进程，不用多线程")
    print()


# ============================================================
# 3. GIL 对 IO 密集型任务的影响
# ============================================================

def io_bound(url, delay):
    """IO 密集型任务：模拟网络请求"""
    import urllib.request
    time.sleep(delay)
    return f"Response from {url}"


def demo_gil_io_bound():
    """
    演示 GIL 对 IO 密集型任务的影响

    运行结果:
        单线程: 4.00s
        多线程: 1.05s  ← 有效加速！
        多进程: 1.10s  ← 也有加速，但进程创建开销更大
    """
    print("=" * 60)
    print("2. GIL 对 IO 密集型任务的影响")
    print("=" * 60)

    tasks = [("url1", 1.0), ("url2", 1.0), ("url3", 1.0), ("url4", 1.0)]

    # 单线程
    start = time.perf_counter()
    results = [io_bound(url, delay) for url, delay in tasks]
    single_time = time.perf_counter() - start
    print(f"单线程: {single_time:.2f}s")

    # 多线程
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(io_bound, url, delay) for url, delay in tasks]
        results = [f.result() for f in futures]
    multi_thread_time = time.perf_counter() - start
    print(f"多线程: {multi_thread_time:.2f}s")

    print(f"\n结论: IO 密集型任务用多线程就够了")
    print()


# ============================================================
# 4. 绕过 GIL 的方法
# ============================================================
# 面试官问: 怎么绕过 GIL？
#
# 标准答:
# 1. 多进程 (multiprocessing): 每个进程有独立的 GIL
# 2. C 扩展: 执行 C 代码时可以释放 GIL（如 numpy, scipy）
# 3. 异步编程 (asyncio): 单线程并发，适合 IO 密集型
# 4. 其他解释器: Jython, IronPython 没有 GIL
# 5. Python 3.13+ free-threaded 模式（实验性）
# ============================================================

def demo_bypass_gil():
    """演示绕过 GIL 的方法"""
    print("=" * 60)
    print("3. 绕过 GIL 的方法")
    print("=" * 60)

    print("""
    方法 1: 多进程 (multiprocessing)
    - 每个进程有独立的 Python 解释器和 GIL
    - 适合 CPU 密集型任务
    - 缺点: 进程间通信开销大

    方法 2: C 扩展
    - numpy, scipy 等库在底层用 C 实现
    - 执行 C 代码时释放 GIL
    - 适合数值计算

    方法 3: 异步编程 (asyncio)
    - 单线程内的并发
    - 适合 IO 密集型任务
    - 不需要多线程/多进程

    方法 4: 其他解释器
    - Jython (JVM): 没有 GIL
    - IronPython (.NET): 没有 GIL
    - PyPy: 有 GIL，但 JIT 编译更快

    方法 5: Python 3.13+ free-threaded
    - 编译时加 --disable-gil
    - 目前是实验性功能
    - 性能可能不如预期
    """)
    print()


# ============================================================
# 5. 多线程 vs 多进程 vs 异步 对比
# ============================================================
# 面试官问: 多线程、多进程、异步编程怎么选？
#
# 标准答:
# | 场景         | 推荐方案      | 原因                     |
# |-------------|--------------|--------------------------|
# | CPU 密集型   | 多进程        | 绕过 GIL，利用多核        |
# | IO 密集型    | 多线程或异步   | GIL 在 IO 时释放          |
# | 高并发 IO    | 异步 (asyncio)| 单线程，开销最小          |
# | 混合型       | 多进程+异步    | 进程处理 CPU，异步处理 IO |
# ============================================================

def demo_comparison():
    """对比总结"""
    print("=" * 60)
    print("4. 多线程 vs 多进程 vs 异步 对比")
    print("=" * 60)

    print("""
    ┌─────────────┬──────────────┬──────────────┬──────────────┐
    │ 特性         │ 多线程        │ 多进程        │ 异步          │
    ├─────────────┼──────────────┼──────────────┼──────────────┤
    │ 并发模型     │ 抢占式        │ 独立进程      │ 协作式        │
    │ GIL 影响     │ 有           │ 无（独立 GIL）│ 无（单线程）   │
    │ 适用场景     │ IO 密集型     │ CPU 密集型    │ IO 密集型     │
    │ 内存开销     │ 小           │ 大           │ 最小          │
    │ 编程复杂度   │ 中（需要锁）  │ 中（需要 IPC）│ 低（async/await）│
    │ 竞态条件     │ 需要注意      │ 不存在        │ 不存在        │
    │ 创建开销     │ 小           │ 大           │ 最小          │
    └─────────────┴──────────────┴──────────────┴──────────────┘

    选择建议:
    1. 如果是 IO 密集型（网络请求、文件读写）→ asyncio 或多线程
    2. 如果是 CPU 密集型（计算、数据处理）→ 多进程
    3. 如果需要高并发连接 → asyncio
    4. 如果是混合型 → 多进程 + asyncio
    """)
    print()


# ============================================================
# 6. 实际应用：用多进程加速计算
# ============================================================

def parallel_sum(data, num_workers=4):
    """
    用多进程并行计算累加和

    思路:
    1. 将数据分成 N 块
    2. 每个进程计算一块的和
    3. 最后汇总结果
    """
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with multiprocessing.Pool(num_workers) as pool:
        partial_sums = pool.map(sum, chunks)

    return sum(partial_sums)


def demo_practical():
    """实际应用示例"""
    print("=" * 60)
    print("5. 实际应用：多进程并行计算")
    print("=" * 60)

    data = list(range(10_000_000))

    # 单进程
    start = time.perf_counter()
    result1 = sum(data)
    t1 = time.perf_counter() - start
    print(f"单进程: {t1:.3f}s, 结果: {result1}")

    # 多进程
    start = time.perf_counter()
    result2 = parallel_sum(data, num_workers=4)
    t2 = time.perf_counter() - start
    print(f"多进程: {t2:.3f}s, 结果: {result2}")

    print(f"加速比: {t1/t2:.2f}x")
    print()


# ============================================================
# 主函数
# ============================================================

def main():
    demo_gil_cpu_bound()
    demo_gil_io_bound()
    demo_bypass_gil()
    demo_comparison()
    demo_practical()


if __name__ == "__main__":
    main()
