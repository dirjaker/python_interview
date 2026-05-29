"""常用标准库演示"""

import os
import sys
import json
import csv
import re
import time
import datetime
import pathlib
import collections
import itertools
import functools
import operator
import heapq
import bisect
import copy
import pprint
import random
import math
import hashlib
import base64
import urllib.parse
import threading
import queue
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


# ============================================================
# 1. collections 模块
# ============================================================

def demo_collections():
    """collections 模块演示"""
    print("=" * 60)
    print("1. collections 模块")
    print("=" * 60)

    # Counter — 计数器
    print("\n1.1 Counter:")
    text = "abracadabra"
    counter = collections.Counter(text)
    print(f"  '{text}' 字符统计: {counter}")
    print(f"  最常见 3 个: {counter.most_common(3)}")

    # 计数器运算
    c1 = collections.Counter(a=3, b=1)
    c2 = collections.Counter(a=1, b=2)
    print(f"  c1 + c2 = {c1 + c2}")
    print(f"  c1 - c2 = {c1 - c2}")  # 只保留正数
    print(f"  c1 & c2 = {c1 & c2}")  # 取最小
    print(f"  c1 | c2 = {c1 | c2}")  # 取最大

    # defaultdict — 默认字典
    print("\n1.2 defaultdict:")
    dd = collections.defaultdict(list)
    words = ["apple", "banana", "avocado", "blueberry", "cherry"]
    for word in words:
        dd[word[0]].append(word)
    print(f"  按首字母分组: {dict(dd)}")

    # 嵌套 defaultdict
    tree = lambda: collections.defaultdict(tree)
    taxonomy = tree()
    taxonomy["动物"]["哺乳类"]["猫科"]["猫"] = "家猫"
    taxonomy["动物"]["哺乳类"]["猫科"]["虎"] = "东北虎"
    print(f"  嵌套结构: {dict(taxonomy)}")

    # OrderedDict — 有序字典 (Python 3.7+ 普通 dict 也有序)
    print("\n1.3 OrderedDict:")
    od = collections.OrderedDict()
    od["first"] = 1
    od["second"] = 2
    od["third"] = 3
    print(f"  OrderedDict: {od}")
    od.move_to_end("first")
    print(f"  移动 first 到末尾: {od}")

    # deque — 双端队列
    print("\n1.4 deque:")
    dq = collections.deque([1, 2, 3, 4, 5], maxlen=5)
    print(f"  初始: {dq}")
    dq.append(6)
    print(f"  append(6): {dq}")  # 自动移除最左边
    dq.appendleft(0)
    print(f"  appendleft(0): {dq}")
    dq.rotate(2)
    print(f"  rotate(2): {dq}")
    dq.extend([7, 8])
    print(f"  extend([7,8]): {dq}")

    # namedtuple — 命名元组
    print("\n1.5 namedtuple:")
    Point = collections.namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"  Point: {p}")
    print(f"  p.x={p.x}, p.y={p.y}")
    print(f"  _asdict(): {p._asdict()}")
    p2 = p._replace(x=10)
    print(f"  _replace(x=10): {p2}")

    # ChainMap — 链式映射
    print("\n1.6 ChainMap:")
    defaults = {"color": "red", "size": "medium"}
    user_prefs = {"color": "blue"}
    settings = collections.ChainMap(user_prefs, defaults)
    print(f"  color: {settings['color']}")  # user_prefs 优先
    print(f"  size: {settings['size']}")    # 从 defaults 获取


# ============================================================
# 2. itertools 模块
# ============================================================

def demo_itertools():
    """itertools 模块演示"""
    print("\n" + "=" * 60)
    print("2. itertools 模块")
    print("=" * 60)

    # chain — 链接迭代器
    print("\n2.1 chain:")
    result = list(itertools.chain([1, 2], [3, 4], [5]))
    print(f"  chain: {result}")

    # chain.from_iterable
    nested = [[1, 2], [3, 4], [5]]
    result = list(itertools.chain.from_iterable(nested))
    print(f"  chain.from_iterable: {result}")

    # product — 笛卡尔积
    print("\n2.2 product:")
    result = list(itertools.product([1, 2], ['a', 'b']))
    print(f"  product: {result}")

    # permutations — 排列
    print("\n2.3 permutations:")
    result = list(itertools.permutations([1, 2, 3], 2))
    print(f"  P(3,2): {result}")

    # combinations — 组合
    print("\n2.4 combinations:")
    result = list(itertools.combinations([1, 2, 3, 4], 2))
    print(f"  C(4,2): {result}")

    # combinations_with_replacement
    result = list(itertools.combinations_with_replacement([1, 2], 3))
    print(f"  C'(2,3): {result}")

    # groupby — 分组
    print("\n2.5 groupby:")
    data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
    data.sort(key=lambda x: x[0])  # 必须先排序
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"  {key}: {list(group)}")

    # islice — 切片迭代器
    print("\n2.6 islice:")
    counter = itertools.count(10, 2)
    result = list(itertools.islice(counter, 5))
    print(f"  islice(count(10,2), 5): {result}")

    # takewhile / dropwhile
    print("\n2.7 takewhile / dropwhile:")
    data = [1, 3, 5, 2, 4, 6]
    result = list(itertools.takewhile(lambda x: x < 5, data))
    print(f"  takewhile(<5): {result}")
    result = list(itertools.dropwhile(lambda x: x < 5, data))
    print(f"  dropwhile(<5): {result}")

    # accumulate — 累积
    print("\n2.8 accumulate:")
    data = [1, 2, 3, 4, 5]
    result = list(itertools.accumulate(data))
    print(f"  accumulate: {result}")
    result = list(itertools.accumulate(data, operator.mul))
    print(f"  accumulate(mul): {result}")

    # starmap
    print("\n2.9 starmap:")
    pairs = [(2, 3), (4, 5), (6, 7)]
    result = list(itertools.starmap(operator.mul, pairs))
    print(f"  starmap(mul): {result}")


# ============================================================
# 3. functools 模块
# ============================================================

def demo_functools():
    """functools 模块演示"""
    print("\n" + "=" * 60)
    print("3. functools 模块")
    print("=" * 60)

    # lru_cache
    print("\n3.1 lru_cache:")

    @functools.lru_cache(maxsize=128)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    start = time.perf_counter()
    result = fibonacci(100)
    elapsed = time.perf_counter() - start
    print(f"  fib(100) = {result}, 耗时: {elapsed:.6f}s")
    print(f"  缓存信息: {fibonacci.cache_info()}")

    # partial — 偏函数
    print("\n3.2 partial:")
    def power(base, exponent):
        return base ** exponent

    square = functools.partial(power, exponent=2)
    cube = functools.partial(power, exponent=3)
    print(f"  square(5) = {square(5)}")
    print(f"  cube(3) = {cube(3)}")

    # reduce — 归约
    print("\n3.3 reduce:")
    result = functools.reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
    print(f"  sum = {result}")
    result = functools.reduce(operator.mul, [1, 2, 3, 4, 5])
    print(f"  product = {result}")

    # 求最大值
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    oldest = functools.reduce(lambda a, b: a if a["age"] > b["age"] else b, data)
    print(f"  最年长: {oldest}")

    # total_ordering
    print("\n3.4 total_ordering:")

    @functools.total_ordering
    class Student:
        def __init__(self, name, grade):
            self.name = name
            self.grade = grade

        def __eq__(self, other):
            return self.grade == other.grade

        def __lt__(self, other):
            return self.grade < other.grade

        def __repr__(self):
            return f"Student('{self.name}', {self.grade})"

    students = [Student("Alice", 90), Student("Bob", 85), Student("Charlie", 90)]
    print(f"  排序: {sorted(students)}")
    print(f"  Alice >= Bob: {students[0] >= students[1]}")

    # cmp_to_key
    print("\n3.5 cmp_to_key:")
    def compare(a, b):
        return (a > b) - (a < b)

    data = [3, 1, 4, 1, 5, 9, 2, 6]
    result = sorted(data, key=functools.cmp_to_key(compare))
    print(f"  排序: {result}")


# ============================================================
# 4. dataclasses 模块
# ============================================================

def demo_dataclasses():
    """dataclasses 模块演示"""
    print("\n" + "=" * 60)
    print("4. dataclasses 模块")
    print("=" * 60)

    @dataclass
    class Point:
        x: float
        y: float

        def distance_to(self, other: 'Point') -> float:
            return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    print("\n4.1 基础 dataclass:")
    p1 = Point(1, 2)
    p2 = Point(4, 6)
    print(f"  p1 = {p1}")
    print(f"  距离 = {p1.distance_to(p2):.2f}")

    # 带默认值
    @dataclass
    class Config:
        host: str = "localhost"
        port: int = 8000
        debug: bool = False

    print("\n4.2 带默认值:")
    config = Config()
    print(f"  默认: {config}")
    config2 = Config(port=9000, debug=True)
    print(f"  自定义: {config2}")

    # field 控制
    @dataclass
    class User:
        name: str
        age: int
        password: str = field(repr=False)  # 不在 repr 中显示
        created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    print("\n4.3 field 控制:")
    user = User("Alice", 30, "secret123")
    print(f"  user = {user}")  # password 不显示

    # 不可变 dataclass
    @dataclass(frozen=True)
    class ImmutablePoint:
        x: float
        y: float

    print("\n4.4 不可变 dataclass:")
    p = ImmutablePoint(1, 2)
    print(f"  p = {p}")
    try:
        p.x = 10
    except Exception as e:
        print(f"  修改失败: {e}")

    # 继承
    @dataclass
    class Shape:
        color: str = "red"

    @dataclass
    class Circle(Shape):
        radius: float = 1.0

    @dataclass
    class Rectangle(Shape):
        width: float = 1.0
        height: float = 1.0

    print("\n4.5 继承:")
    c = Circle(radius=5, color="blue")
    r = Rectangle(width=3, height=4)
    print(f"  圆: {c}")
    print(f"  矩形: {r}")


# ============================================================
# 5. enum 模块
# ============================================================

def demo_enum():
    """enum 模块演示"""
    print("\n" + "=" * 60)
    print("5. enum 模块")
    print("=" * 60)

    # 基础枚举
    print("\n5.1 基础枚举:")

    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    print(f"  Color.RED = {Color.RED}")
    print(f"  Color.RED.value = {Color.RED.value}")
    print(f"  Color(1) = {Color(1)}")
    print(f"  Color['RED'] = {Color['RED']}")

    # auto()
    print("\n5.2 auto():")

    class Status(Enum):
        PENDING = auto()
        RUNNING = auto()
        SUCCESS = auto()
        FAILED = auto()

    for status in Status:
        print(f"  {status.name} = {status.value}")

    # 字符串枚举
    print("\n5.3 字符串枚举:")

    class HttpMethod(str, Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"

    print(f"  HttpMethod.GET = {HttpMethod.GET}")
    print(f"  可直接作为字符串: {HttpMethod.GET + '/api'}")

    # 带方法的枚举
    print("\n5.4 带方法的枚举:")

    class Planet(Enum):
        MERCURY = (3.303e+23, 2.4397e6)
        VENUS = (4.869e+24, 6.0518e6)
        EARTH = (5.976e+24, 6.37814e6)

        def __init__(self, mass, radius):
            self.mass = mass
            self.radius = radius

        @property
        def surface_gravity(self):
            G = 6.67300E-11
            return G * self.mass / (self.radius ** 2)

    print(f"  Earth 重力: {Planet.EARTH.surface_gravity:.2f} m/s²")

    # Flag (位运算)
    print("\n5.5 Flag:")

    class Permission(Flag):
        READ = auto()
        WRITE = auto()
        EXECUTE = auto()

    perms = Permission.READ | Permission.WRITE
    print(f"  权限: {perms}")
    print(f"  有 READ 权限: {Permission.READ in perms}")
    print(f"  有 EXECUTE 权限: {Permission.EXECUTE in perms}")


# ============================================================
# 6. pathlib 模块
# ============================================================

def demo_pathlib():
    """pathlib 模块演示"""
    print("\n" + "=" * 60)
    print("6. pathlib 模块")
    print("=" * 60)

    # 创建 Path 对象
    print("\n6.1 基础用法:")
    p = pathlib.Path(".")
    print(f"  当前目录: {p.absolute()}")

    # 路径操作
    print("\n6.2 路径操作:")
    p = pathlib.Path("/home/user/documents/file.txt")
    print(f"  name: {p.name}")
    print(f"  stem: {p.stem}")
    print(f"  suffix: {p.suffix}")
    print(f"  parent: {p.parent}")
    print(f"  parts: {p.parts}")

    # 路径拼接
    print("\n6.3 路径拼接:")
    base = pathlib.Path("/home/user")
    file_path = base / "documents" / "file.txt"
    print(f"  拼接: {file_path}")

    # 创建临时文件演示
    print("\n6.4 文件操作:")
    temp_dir = pathlib.Path("/tmp/pathlib_demo")
    temp_dir.mkdir(exist_ok=True)

    # 写入文件
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, pathlib!", encoding="utf-8")
    print(f"  写入: {test_file}")

    # 读取文件
    content = test_file.read_text(encoding="utf-8")
    print(f"  内容: {content}")

    # 遍历目录
    print("\n6.5 遍历目录:")
    for item in temp_dir.iterdir():
        print(f"  {item.name} (文件: {item.is_file()})")

    # 清理
    test_file.unlink()
    temp_dir.rmdir()


# ============================================================
# 7. re 模块（正则表达式）
# ============================================================

def demo_re():
    """re 模块演示"""
    print("\n" + "=" * 60)
    print("7. re 模块（正则表达式）")
    print("=" * 60)

    # 基础匹配
    print("\n7.1 基础匹配:")
    text = "我的手机号是 13812345678，邮箱是 test@example.com"
    phone = re.search(r"1[3-9]\d{9}", text)
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
    print(f"  手机号: {phone.group() if phone else '未找到'}")
    print(f"  邮箱: {email.group() if email else '未找到'}")

    # findall
    print("\n7.2 findall:")
    text = "价格: 100元, 200元, 300元"
    prices = re.findall(r"\d+", text)
    print(f"  价格: {prices}")

    # 分组
    print("\n7.3 分组:")
    text = "2024-01-15, 2024-12-31"
    pattern = r"(\d{4})-(\d{2})-(\d{2})"
    matches = re.findall(pattern, text)
    for year, month, day in matches:
        print(f"  {year}年{month}月{day}日")

    # 命名分组
    print("\n7.4 命名分组:")
    text = "John Smith, Jane Doe"
    pattern = r"(?P<first>\w+) (?P<last>\w+)"
    for match in re.finditer(pattern, text):
        print(f"  {match.group('first')} -> {match.group('last')}")

    # 替换
    print("\n7.5 替换:")
    text = "Hello World 2024"
    result = re.sub(r"\d+", "XXXX", text)
    print(f"  替换: {result}")

    # 编译正则
    print("\n7.6 编译正则:")
    email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    emails = email_pattern.findall("a@b.com, c@d.org")
    print(f"  邮箱: {emails}")


# ============================================================
# 8. json 模块
# ============================================================

def demo_json():
    """json 模块演示"""
    print("\n" + "=" * 60)
    print("8. json 模块")
    print("=" * 60)

    # 编码
    print("\n8.1 编码:")
    data = {
        "name": "张三",
        "age": 30,
        "scores": [90, 85, 95],
        "active": True,
        "address": None
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"  JSON:\n{json_str}")

    # 解码
    print("\n8.2 解码:")
    parsed = json.loads(json_str)
    print(f"  解析: {parsed}")

    # 自定义编码
    print("\n8.3 自定义编码:")

    class User:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    def user_encoder(obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age, "__type__": "User"}
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    user = User("Alice", 30)
    json_str = json.dumps(user, default=user_encoder, ensure_ascii=False)
    print(f"  User JSON: {json_str}")

    # 文件读写
    print("\n8.4 文件读写:")
    temp_file = "/tmp/test.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(temp_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"  从文件加载: {loaded['name']}")

    os.remove(temp_file)


# ============================================================
# 9. logging 模块
# ============================================================

def demo_logging():
    """logging 模块演示"""
    print("\n" + "=" * 60)
    print("9. logging 模块")
    print("=" * 60)

    # 基础配置
    print("\n9.1 基础日志:")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    logger = logging.getLogger("demo")
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")

    # 使用 StreamHandler 捕获输出
    print("\n9.2 自定义 Handler:")

    class ListHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(self.format(record))

    custom_logger = logging.getLogger("custom")
    custom_logger.setLevel(logging.DEBUG)

    list_handler = ListHandler()
    list_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    custom_logger.addHandler(list_handler)

    custom_logger.info("测试消息 1")
    custom_logger.warning("测试消息 2")
    print(f"  捕获的日志: {list_handler.records}")


# ============================================================
# 10. hashlib 模块
# ============================================================

def demo_hashlib():
    """hashlib 模块演示"""
    print("\n" + "=" * 60)
    print("10. hashlib 模块")
    print("=" * 60)

    text = "Hello, World!"

    # MD5
    print("\n10.1 MD5:")
    md5 = hashlib.md5(text.encode()).hexdigest()
    print(f"  '{text}' -> {md5}")

    # SHA256
    print("\n10.2 SHA256:")
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    print(f"  '{text}' -> {sha256}")

    # Base64
    print("\n10.3 Base64:")
    encoded = base64.b64encode(text.encode()).decode()
    print(f"  编码: {encoded}")
    decoded = base64.b64decode(encoded).decode()
    print(f"  解码: {decoded}")


# ============================================================
# 11. 常见数据结构实现
# ============================================================

def demo_data_structures():
    """常见数据结构演示"""
    print("\n" + "=" * 60)
    print("11. 常见数据结构")
    print("=" * 60)

    # LRU Cache
    print("\n11.1 LRU Cache:")

    class LRUCache:
        def __init__(self, capacity):
            self.cache = collections.OrderedDict()
            self.capacity = capacity

        def get(self, key):
            if key not in self.cache:
                return -1
            self.cache.move_to_end(key)
            return self.cache[key]

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    lru = LRUCache(3)
    lru.put("a", 1)
    lru.put("b", 2)
    lru.put("c", 3)
    print(f"  get('a'): {lru.get('a')}")
    lru.put("d", 4)  # 淘汰 'b'
    print(f"  get('b'): {lru.get('b')}")  # -1

    # 堆
    print("\n11.2 堆 (heapq):")
    data = [5, 3, 7, 1, 9, 2]
    heapq.heapify(data)
    print(f"  最小堆: {data}")
    print(f"  heappop: {heapq.heappop(data)}")

    # Top K
    print(f"  最大的 3 个: {heapq.nlargest(3, [5, 3, 7, 1, 9, 2])}")

    # 二分查找
    print("\n11.3 二分查找 (bisect):")
    sorted_list = [1, 3, 5, 7, 9]
    idx = bisect.bisect_left(sorted_list, 5)
    print(f"  bisect_left([1,3,5,7,9], 5) = {idx}")

    bisect.insort(sorted_list, 6)
    print(f"  insort(6): {sorted_list}")


# ============================================================
# 12. 设计模式实现
# ============================================================

def demo_design_patterns():
    """设计模式演示"""
    print("\n" + "=" * 60)
    print("12. 设计模式")
    print("=" * 60)

    # 单例模式
    print("\n12.1 单例模式:")

    class Singleton:
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, value=None):
            if not hasattr(self, '_initialized'):
                self.value = value
                self._initialized = True

    s1 = Singleton("first")
    s2 = Singleton("second")
    print(f"  s1 is s2: {s1 is s2}")
    print(f"  s1.value: {s1.value}")

    # 观察者模式
    print("\n12.2 观察者模式:")

    class EventEmitter:
        def __init__(self):
            self._listeners = {}

        def on(self, event, callback):
            if event not in self._listeners:
                self._listeners[event] = []
            self._listeners[event].append(callback)

        def emit(self, event, *args, **kwargs):
            for callback in self._listeners.get(event, []):
                callback(*args, **kwargs)

    emitter = EventEmitter()
    emitter.on("data", lambda x: print(f"  收到: {x}"))
    emitter.emit("data", 42)

    # 策略模式
    print("\n12.3 策略模式:")

    class SortStrategy(ABC):
        @abstractmethod
        def sort(self, data):
            pass

    class BubbleSort(SortStrategy):
        def sort(self, data):
            return sorted(data)

    class ReverseSort(SortStrategy):
        def sort(self, data):
            return sorted(data, reverse=True)

    class Sorter:
        def __init__(self, strategy):
            self.strategy = strategy

        def sort(self, data):
            return self.strategy.sort(data)

    data = [3, 1, 4, 1, 5]
    sorter = Sorter(BubbleSort())
    print(f"  正序: {sorter.sort(data)}")
    sorter.strategy = ReverseSort()
    print(f"  逆序: {sorter.sort(data)}")


# ============================================================
# 运行所有演示
# ============================================================

if __name__ == "__main__":
    demo_collections()
    demo_itertools()
    demo_functools()
    demo_dataclasses()
    demo_enum()
    demo_pathlib()
    demo_re()
    demo_json()
    demo_logging()
    demo_hashlib()
    demo_data_structures()
    demo_design_patterns()
