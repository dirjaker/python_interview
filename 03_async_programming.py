"""异步编程完整演示"""

import asyncio
import time
from typing import List, Any


# ============================================================
# 1. 协程基础
# ============================================================

async def say_hello(name: str, delay: float) -> str:
    """基础协程"""
    print(f"👋 Hello {name}")
    await asyncio.sleep(delay)  # 挂起协程
    print(f"👋 Goodbye {name}")
    return f"{name} done"


async def basic_demo():
    """基础协程演示"""
    print("\n1. 基础协程:")
    result = await say_hello("Alice", 1)
    print(f"结果: {result}")


# ============================================================
# 2. 并发执行
# ============================================================

async def fetch_data(url: str, delay: float) -> dict:
    """模拟异步请求"""
    print(f"📡 开始请求: {url}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"✅ 完成请求: {url}")
    return {"url": url, "data": f"数据来自 {url}"}


async def concurrent_demo():
    """并发执行演示"""
    print("\n2. 并发执行 (asyncio.gather):")

    urls = [
        ("https://api1.com", 2),
        ("https://api2.com", 1),
        ("https://api3.com", 3),
    ]

    start = time.perf_counter()

    # gather: 并发执行所有协程
    tasks = [fetch_data(url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"总耗时: {elapsed:.2f}s (而非 {sum(d for _, d in urls)}s)")
    print(f"结果: {results}")


# ============================================================
# 3. Task 和 create_task
# ============================================================

async def task_demo():
    """Task 演示"""
    print("\n3. Task (create_task):")

    # 创建 Task（立即开始执行）
    task1 = asyncio.create_task(say_hello("Bob", 2))
    task2 = asyncio.create_task(say_hello("Charlie", 1))

    print("Task 已创建，继续执行其他代码...")
    await asyncio.sleep(0.5)
    print("等待 Task 完成...")

    # 等待所有 Task
    results = await asyncio.gather(task1, task2)
    print(f"结果: {results}")


# ============================================================
# 4. 异步上下文管理器
# ============================================================

class AsyncTimer:
    """异步计时上下文管理器"""

    def __init__(self, label=""):
        self.label = label
        self.start = None
        self.elapsed = None

    async def __aenter__(self):
        print(f"⏱ 开始: {self.label}")
        self.start = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"⏱ 结束: {self.label}, 耗时: {self.elapsed:.4f}s")
        return False


class AsyncDatabase:
    """模拟异步数据库连接"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    async def __aenter__(self):
        print(f"🔌 连接数据库: {self.db_name}")
        await asyncio.sleep(0.1)  # 模拟连接
        self.connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"🔌 断开数据库: {self.db_name}")
        await asyncio.sleep(0.1)  # 模拟断开
        self.connected = False
        return False

    async def query(self, sql):
        if not self.connected:
            raise RuntimeError("未连接数据库")
        await asyncio.sleep(0.1)  # 模拟查询
        return f"查询结果: {sql}"


async def context_manager_demo():
    """异步上下文管理器演示"""
    print("\n4. 异步上下文管理器:")

    async with AsyncTimer("数据库操作"):
        async with AsyncDatabase("mydb") as db:
            result = await db.query("SELECT * FROM users")
            print(f"  {result}")


# ============================================================
# 5. 异步迭代器
# ============================================================

class AsyncRange:
    """异步迭代器"""

    def __init__(self, stop, delay=0.1):
        self.stop = stop
        self.delay = delay
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        self.current += 1
        return self.current - 1


async def async_iterator_demo():
    """异步迭代器演示"""
    print("\n5. 异步迭代器:")

    async for i in AsyncRange(5, delay=0.2):
        print(f"  收到: {i}")


# ============================================================
# 6. 异步生成器
# ============================================================

async def async_generator(n: int, delay: float = 0.1):
    """异步生成器"""
    for i in range(n):
        await asyncio.sleep(delay)
        yield i * 2


async def async_generator_demo():
    """异步生成器演示"""
    print("\n6. 异步生成器:")

    # 方式 1: async for
    async for i in async_generator(5):
        print(f"  生成: {i}")

    # 方式 2: 列表推导
    results = [i async for i in async_generator(5)]
    print(f"  列表: {results}")

    # 方式 3: 带条件的推导
    even_results = [i async for i in async_generator(10) if i % 3 == 0]
    print(f"  能被3整除: {even_results}")


# ============================================================
# 7. 异步队列
# ============================================================

async def producer(queue: asyncio.Queue, name: str, count: int):
    """生产者"""
    for i in range(count):
        await asyncio.sleep(0.1)  # 模拟生产
        item = f"{name}_item_{i}"
        await queue.put(item)
        print(f"📦 {name} 生产: {item}")
    print(f"📦 {name} 完成")


async def consumer(queue: asyncio.Queue, name: str):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:  # 结束信号
            break
        await asyncio.sleep(0.2)  # 模拟处理
        print(f"🔧 {name} 消费: {item}")
        queue.task_done()
    print(f"🔧 {name} 结束")


async def queue_demo():
    """异步队列演示"""
    print("\n7. 异步队列:")

    queue = asyncio.Queue(maxsize=5)

    # 创建生产者和消费者
    producers = [
        producer(queue, "P1", 3),
        producer(queue, "P2", 3),
    ]
    consumers = [
        consumer(queue, "C1"),
        consumer(queue, "C2"),
    ]

    # 启动所有任务
    tasks = producers + consumers

    # 等待生产者完成
    await asyncio.gather(*producers)

    # 发送结束信号
    for _ in consumers:
        await queue.put(None)

    # 等待消费者完成
    await asyncio.gather(*consumers)


# ============================================================
# 8. 超时控制
# ============================================================

async def slow_operation():
    """慢操作"""
    await asyncio.sleep(10)
    return "完成"


async def timeout_demo():
    """超时控制演示"""
    print("\n8. 超时控制:")

    try:
        # 方式 1: asyncio.wait_for
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  ❌ 操作超时")

    # 方式 2: asyncio.timeout (Python 3.11+)
    try:
        async with asyncio.timeout(1.0):
            result = await slow_operation()
    except TimeoutError:
        print("  ❌ 操作超时 (timeout)")


# ============================================================
# 9. 等待多个任务
# ============================================================

async def wait_demo():
    """等待多个任务演示"""
    print("\n9. 等待多个任务:")

    tasks = [
        asyncio.create_task(fetch_data("api1", 2)),
        asyncio.create_task(fetch_data("api2", 1)),
        asyncio.create_task(fetch_data("api3", 3)),
    ]

    # 方式 1: FIRST_COMPLETED
    print("  等待第一个完成...")
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"  完成: {len(done)}, 待处理: {len(pending)}")

    # 取消剩余任务
    for task in pending:
        task.cancel()

    # 方式 2: ALL_COMPLETED (默认)
    tasks2 = [
        asyncio.create_task(fetch_data("api4", 1)),
        asyncio.create_task(fetch_data("api5", 2)),
    ]
    done, _ = await asyncio.wait(tasks2, return_when=asyncio.ALL_COMPLETED)
    print(f"  全部完成: {len(done)}")


# ============================================================
# 10. 异步 Semaphore 限流
# ============================================================

async def limited_fetch(semaphore: asyncio.Semaphore, url: str):
    """带限流的异步请求"""
    async with semaphore:
        print(f"  📡 请求: {url}")
        await asyncio.sleep(0.5)
        return f"数据: {url}"


async def semaphore_demo():
    """Semaphore 限流演示"""
    print("\n10. Semaphore 限流:")

    # 最多同时 3 个请求
    semaphore = asyncio.Semaphore(3)

    urls = [f"https://api{i}.com" for i in range(10)]
    tasks = [limited_fetch(semaphore, url) for url in urls]

    results = await asyncio.gather(*tasks)
    print(f"  完成 {len(results)} 个请求")


# ============================================================
# 11. 异步锁
# ============================================================

class AsyncCounter:
    """异步安全计数器"""

    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            temp = self.value
            await asyncio.sleep(0)  # 让出控制权
            self.value = temp + 1


async def lock_demo():
    """异步锁演示"""
    print("\n11. 异步锁:")

    counter = AsyncCounter()

    # 并发增加
    await asyncio.gather(*[counter.increment() for _ in range(100)])
    print(f"  计数器: {counter.value}")  # 应该是 100


# ============================================================
# 12. 异步异常处理
# ============================================================

async def risky_operation(should_fail: bool):
    """可能失败的操作"""
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError("操作失败")
    return "成功"


async def exception_demo():
    """异步异常处理演示"""
    print("\n12. 异步异常处理:")

    # 方式 1: gather + return_exceptions
    tasks = [
        risky_operation(False),
        risky_operation(True),
        risky_operation(False),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  任务 {i}: 失败 - {result}")
        else:
            print(f"  任务 {i}: {result}")

    # 方式 2: TaskGroup (Python 3.11+)
    print("\n  TaskGroup 示例:")
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(risky_operation(False))
            task2 = tg.create_task(risky_operation(True))
    except* ValueError as eg:
        print(f"  捕获到 {len(eg.exceptions)} 个异常")


# ============================================================
# 13. 实际应用：异步爬虫模式
# ============================================================

async def fetch_page(url: str, session_id: int) -> dict:
    """模拟异步爬取页面"""
    delay = 0.5 + (hash(url) % 10) / 10
    await asyncio.sleep(delay)
    return {
        "url": url,
        "session": session_id,
        "content_length": 1000 + hash(url) % 5000,
    }


async def crawl_demo():
    """异步爬虫演示"""
    print("\n13. 异步爬虫模式:")

    urls = [
        f"https://example.com/page/{i}"
        for i in range(10)
    ]

    # 限制并发数
    semaphore = asyncio.Semaphore(3)

    async def limited_fetch(url, session_id):
        async with semaphore:
            return await fetch_page(url, session_id)

    # 并发爬取
    start = time.perf_counter()
    tasks = [limited_fetch(url, i % 3) for i, url in enumerate(urls)]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start

    print(f"  爬取 {len(results)} 个页面, 耗时: {elapsed:.2f}s")
    for r in results[:3]:
        print(f"  {r['url']}: {r['content_length']} bytes")


# ============================================================
# 14. 实际应用：异步任务调度器
# ============================================================

class AsyncTaskScheduler:
    """异步任务调度器"""

    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = {}
        self.errors = {}

    async def run(self, name: str, coro):
        async with self.semaphore:
            try:
                result = await coro
                self.results[name] = result
                return result
            except Exception as e:
                self.errors[name] = e
                raise

    async def run_all(self, tasks: dict):
        """运行所有任务"""
        coros = [
            self.run(name, coro)
            for name, coro in tasks.items()
        ]
        return await asyncio.gather(*coros, return_exceptions=True)


async def scheduler_demo():
    """任务调度器演示"""
    print("\n14. 任务调度器:")

    scheduler = AsyncTaskScheduler(max_concurrent=3)

    tasks = {
        "task_1": fetch_data("api1", 1),
        "task_2": fetch_data("api2", 2),
        "task_3": fetch_data("api3", 0.5),
        "task_4": fetch_data("api4", 1.5),
        "task_5": fetch_data("api5", 0.8),
    }

    results = await scheduler.run_all(tasks)

    print(f"  成功: {len(scheduler.results)}")
    print(f"  失败: {len(scheduler.errors)}")


# ============================================================
# 运行所有演示
# ============================================================

async def main():
    print("=" * 60)
    print("异步编程演示")
    print("=" * 60)

    await basic_demo()
    await concurrent_demo()
    await task_demo()
    await context_manager_demo()
    await async_iterator_demo()
    await async_generator_demo()
    await queue_demo()
    await timeout_demo()
    await wait_demo()
    await semaphore_demo()
    await lock_demo()
    await exception_demo()
    await crawl_demo()
    await scheduler_demo()


if __name__ == "__main__":
    asyncio.run(main())
