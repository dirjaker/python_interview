"""
异步编程 01: 协程基础与并发模式
=================================

面试高频问题:
1. 协程和线程的区别？
2. asyncio 的核心组件是什么？
3. 为什么异步代码有时比同步还慢？

核心要点:
- 协程 (Coroutine): 用 async/await 定义的函数，可以在执行中暂停
- 事件循环 (Event Loop): 调度协程执行的核心
- Task: 对协程的包装，可以并发执行
- await: 暂停当前协程，等待另一个协程完成
"""


import asyncio
import time
import aiohttp


# ============================================================
# 1. 协程 vs 线程
# ============================================================
# 面试官问: 协程和线程有什么区别？
#
# 标准答:
# | 特性     | 协程 (Coroutine)    | 线程 (Thread)        |
# |---------|--------------------|--------------------|
# | 调度     | 协作式（主动让出）   | 抢占式（OS 调度）    |
# | 切换     | 用户态，开销小       | 内核态，开销大       |
# | 并发     | 单线程内并发         | 多线程并发           |
# | 竞态     | 不存在（单线程）     | 需要锁               |
# | 适用场景 | IO 密集型           | IO + CPU 混合       |
# | 编程模型 | async/await         | threading 模块       |
#
# 协程的优势:
# - 无竞态，不需要锁
# - 切换开销小（纳秒级 vs 微秒级）
# - 可以轻松创建数万个协程
#
# 协程的劣势:
# - 不能利用多核 CPU
# - CPU 密集型任务会阻塞事件循环
# ============================================================


# ============================================================
# 2. 协程基础
# ============================================================

async def simple_coroutine():
    """
    最简单的协程

    async def: 定义协程函数
    await: 暂停协程，等待另一个协程完成

    注意:
        - 协程函数调用后不会立即执行，返回一个协程对象
        - 必须用 await 或 asyncio.run() 来执行
    """
    print("协程开始")
    await asyncio.sleep(1)  # 暂停 1 秒，让出控制权
    print("协程结束")
    return 42


async def coroutine_with_return():
    """
    有返回值的协程

    await 的表达式会返回协程的结果
    """
    await asyncio.sleep(0.1)
    return "Hello from coroutine!"


# ============================================================
# 3. 并发执行 - asyncio.gather
# ============================================================
# 面试官问: 怎么并发执行多个协程？
#
# 标准答:
# 1. asyncio.gather(*coros): 并发执行，按顺序返回结果
# 2. asyncio.create_task(coro): 创建任务，立即开始执行
# 3. asyncio.wait(tasks): 等待任务完成（更灵活）
# 4. asyncio.as_completed(tasks): 按完成顺序返回结果
#
# 注意:
# - gather 会等待所有任务完成
# - 如果某个任务失败，其他任务会继续执行
# - return_exceptions=True 可以让异常作为结果返回
# ============================================================

async def fetch_data(url, delay):
    """模拟网络请求"""
    print(f"开始请求 {url}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成请求 {url}")
    return f"Data from {url}"


async def demo_gather():
    """
    用 gather 并发执行

    运行结果（并发，总耗时约 1 秒）:
        开始请求 https://api1.com
        开始请求 https://api2.com
        开始请求 https://api3.com
        完成请求 https://api1.com
        完成请求 https://api2.com
        完成请求 https://api3.com
        结果: ['Data from https://api1.com', ...]
    """
    print("=== asyncio.gather ===")
    start = time.perf_counter()

    # 并发执行 3 个请求
    results = await asyncio.gather(
        fetch_data("https://api1.com", 1.0),
        fetch_data("https://api2.com", 0.5),
        fetch_data("https://api3.com", 0.8),
    )

    elapsed = time.perf_counter() - start
    print(f"结果: {results}")
    print(f"总耗时: {elapsed:.2f}s（并发执行）")
    print()


# ============================================================
# 4. create_task - 更灵活的并发
# ============================================================

async def demo_create_task():
    """
    用 create_task 创建任务

    与 gather 的区别:
    - gather: 一次性提交所有任务
    - create_task: 可以在执行过程中动态创建任务

    运行结果:
        创建任务 1
        创建任务 2
        创建任务 3
        任务 1 完成: Result 1
        任务 2 完成: Result 2
        任务 3 完成: Result 3
    """
    print("=== asyncio.create_task ===")

    async def task(name, delay):
        await asyncio.sleep(delay)
        return f"Result {name}"

    # 创建任务（立即开始执行）
    t1 = asyncio.create_task(task(1, 0.3))
    t2 = asyncio.create_task(task(2, 0.2))
    t3 = asyncio.create_task(task(3, 0.1))

    print("创建了 3 个任务")

    # 等待所有任务完成
    results = await asyncio.gather(t1, t2, t3)
    print(f"结果: {results}")
    print()


# ============================================================
# 5. as_completed - 按完成顺序处理
# ============================================================

async def demo_as_completed():
    """
    用 as_completed 按完成顺序处理结果

    适用场景:
        - 哪个先完成就先处理哪个
        - 实时显示进度
    """
    print("=== asyncio.as_completed ===")

    async def slow_task(n):
        await asyncio.sleep(0.1 * n)
        return n

    tasks = [slow_task(i) for i in range(5, 0, -1)]

    # 按完成顺序获取结果
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"完成: {result}")
    print()


# ============================================================
# 6. 超时控制
# ============================================================
# 面试官问: 异步代码怎么做超时控制？
#
# 标准答:
# 1. asyncio.wait_for(coro, timeout): 设置超时时间
# 2. asyncio.timeout(seconds): Python 3.11+ 的上下文管理器
# 3. asyncio.shield(coro): 保护协程不被取消
# ============================================================

async def demo_timeout():
    """
    超时控制

    运行结果:
        Task 1 完成: fast
        Task 2 超时！
    """
    print("=== 超时控制 ===")

    async def slow_task():
        await asyncio.sleep(5)
        return "slow"

    async def fast_task():
        await asyncio.sleep(0.1)
        return "fast"

    # Task 1: 正常完成
    result = await asyncio.wait_for(fast_task(), timeout=1.0)
    print(f"Task 1 完成: {result}")

    # Task 2: 超时
    try:
        result = await asyncio.wait_for(slow_task(), timeout=0.5)
    except asyncio.TimeoutError:
        print("Task 2 超时！")
    print()


# ============================================================
# 7. Semaphore - 限制并发数
# ============================================================
# 面试官问: 怎么限制异步任务的并发数？
#
# 标准答:
# 用 asyncio.Semaphore：
# - 创建时指定最大并发数
# - async with semaphore: 获取信号量
# - 离开时自动释放
#
# 使用场景:
# - 限制同时打开的文件数
# - 限制同时发起的网络请求数
# - 防止资源耗尽
# ============================================================

async def demo_semaphore():
    """
    用 Semaphore 限制并发数

    运行结果（最多同时执行 2 个任务）:
        开始任务 0
        开始任务 1
        完成任务 0
        完成任务 1
        开始任务 2
        开始任务 3
        ...
    """
    print("=== Semaphore 限制并发 ===")

    # 最多同时执行 2 个任务
    semaphore = asyncio.Semaphore(2)

    async def limited_task(n):
        async with semaphore:  # 获取信号量
            print(f"开始任务 {n}")
            await asyncio.sleep(0.3)
            print(f"完成任务 {n}")
            return n

    tasks = [limited_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(f"结果: {results}")
    print()


# ============================================================
# 8. 异步上下文管理器
# ============================================================
# 面试官问: 异步代码怎么用 with 语句？
#
# 标准答:
# 实现 __aenter__ 和 __aexit__ 方法：
# - __aenter__: 异步进入（可以 await）
# - __aexit__: 异步退出（可以 await）
#
# 用法:
#   async with MyContext() as ctx:
#       await ctx.do_something()
# ============================================================

class AsyncDatabase:
    """
    异步数据库连接（演示异步上下文管理器）

    运行结果:
        连接数据库...
        执行查询: SELECT * FROM users
        断开连接
    """

    def __init__(self, db_name):
        self.db_name = db_name

    async def __aenter__(self):
        """异步进入：建立连接"""
        print("连接数据库...")
        await asyncio.sleep(0.1)  # 模拟连接
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出：关闭连接"""
        print("断开连接")
        await asyncio.sleep(0.1)  # 模拟断开
        return False

    async def query(self, sql):
        """异步查询"""
        print(f"执行查询: {sql}")
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Alice"}]


async def demo_async_context():
    """演示异步上下文管理器"""
    print("=== 异步上下文管理器 ===")

    async with AsyncDatabase("mydb") as db:
        result = await db.query("SELECT * FROM users")
        print(f"结果: {result}")
    print()


# ============================================================
# 9. 异步迭代器和生成器
# ============================================================

class AsyncRange:
    """
    异步迭代器

    实现 __aiter__ 和 __anext__ 方法

    运行结果:
        0
        1
        2
        3
        4
    """

    def __init__(self, stop, delay=0.1):
        self.stop = stop
        self.delay = delay
        self.current = 0

    def __aiter__(self):
        """返回异步迭代器（通常是 self）"""
        return self

    async def __anext__(self):
        """返回下一个值（异步）"""
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        value = self.current
        self.current += 1
        return value


async def async_generator(stop):
    """
    异步生成器（更简洁）

    用 yield 代替 __aiter__ 和 __anext__
    """
    for i in range(stop):
        await asyncio.sleep(0.1)
        yield i


async def demo_async_iteration():
    """演示异步迭代"""
    print("=== 异步迭代器 ===")

    # 异步迭代器
    async for i in AsyncRange(5, delay=0.05):
        print(i)

    print("\n=== 异步生成器 ===")
    # 异步生成器
    async for i in async_generator(5):
        print(i)
    print()


# ============================================================
# 主函数
# ============================================================

async def main():
    """运行所有演示"""
    await demo_gather()
    await demo_create_task()
    await demo_as_completed()
    await demo_timeout()
    await demo_semaphore()
    await demo_async_context()
    await demo_async_iteration()


if __name__ == "__main__":
    asyncio.run(main())
