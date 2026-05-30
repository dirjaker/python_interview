"""
标准库 01: collections 模块
=============================

面试高频问题:
1. defaultdict 和 dict 有什么区别？
2. Counter 怎么用？
3. deque 和 list 的区别？

核心要点:
- Counter: 计数器，统计元素出现次数
- defaultdict: 带默认值的字典
- deque: 双端队列，两端操作 O(1)
- namedtuple: 命名元组，增强可读性
- OrderedDict: 有序字典（Python 3.7+ 普通 dict 也有序）
- ChainMap: 链式映射
"""


import collections


# ============================================================
# 1. Counter - 计数器
# ============================================================
# 面试官问: 怎么统计列表中每个元素出现的次数？
#
# 标准答:
# 1. collections.Counter(list) — 最简洁
# 2. defaultdict(int) — 手动计数
# 3. dict.get(key, 0) + 1 — 基础方法
#
# Counter 的优势:
# - 一行代码搞定
# - 支持 most_common(n) 获取 Top N
# - 支持数学运算（加减交并）
# ============================================================

def demo_counter():
    """Counter 演示"""
    print("=" * 60)
    print("1. Counter - 计数器")
    print("=" * 60)

    # 基础用法
    text = "abracadabra"
    counter = collections.Counter(text)
    print(f"字符统计: {counter}")
    print(f"最常见 3 个: {counter.most_common(3)}")

    # 从列表创建
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    word_count = collections.Counter(words)
    print(f"单词统计: {word_count}")

    # 计数器运算
    c1 = collections.Counter(a=3, b=1)
    c2 = collections.Counter(a=1, b=2)

    print(f"\nc1 = {c1}")
    print(f"c2 = {c2}")
    print(f"c1 + c2 = {c1 + c2}")    # 加法
    print(f"c1 - c2 = {c1 - c2}")    # 减法（只保留正数）
    print(f"c1 & c2 = {c1 & c2}")    # 交集（取最小）
    print(f"c1 | c2 = {c1 | c2}")    # 并集（取最大）
    print()


# ============================================================
# 2. defaultdict - 默认字典
# ============================================================
# 面试官问: defaultdict 和普通 dict 有什么区别？
#
# 标准答:
# - defaultdict: 访问不存在的 key 时，自动创建默认值
# - dict: 访问不存在的 key 会抛出 KeyError
#
# 常见用法:
# - defaultdict(int): 计数
# - defaultdict(list): 分组
# - defaultdict(set): 分组（去重）
# - defaultdict(dict): 嵌套字典
# ============================================================

def demo_defaultdict():
    """defaultdict 演示"""
    print("=" * 60)
    print("2. defaultdict - 默认字典")
    print("=" * 60)

    # 分组
    words = ["apple", "banana", "avocado", "blueberry", "cherry"]
    grouped = collections.defaultdict(list)
    for word in words:
        grouped[word[0]].append(word)
    print(f"按首字母分组: {dict(grouped)}")

    # 计数
    counter = collections.defaultdict(int)
    for word in words:
        counter[word] += 1
    print(f"单词计数: {dict(counter)}")

    # 嵌套字典
    tree = lambda: collections.defaultdict(tree)
    taxonomy = tree()
    taxonomy["动物"]["哺乳类"]["猫科"]["猫"] = "家猫"
    taxonomy["动物"]["哺乳类"]["猫科"]["虎"] = "东北虎"
    print(f"嵌套结构: {dict(taxonomy)}")
    print()


# ============================================================
# 3. deque - 双端队列
# ============================================================
# 面试官问: deque 和 list 有什么区别？
#
# 标准答:
# | 操作       | list    | deque   |
# |-----------|---------|---------|
# | append    | O(1)*   | O(1)    |
# | appendleft| O(n)    | O(1)    |
# | pop       | O(1)    | O(1)    |
# | popleft   | O(n)    | O(1)    |
# | insert    | O(n)    | O(n)    |
# | 随机访问  | O(1)    | O(n)    |
#
# 使用场景:
# - 频繁在两端操作 → deque
# - 需要随机访问 → list
# - 需要 maxlen（自动丢弃旧元素）→ deque
# ============================================================

def demo_deque():
    """deque 演示"""
    print("=" * 60)
    print("3. deque - 双端队列")
    print("=" * 60)

    # 基础操作
    dq = collections.deque([1, 2, 3, 4, 5], maxlen=5)
    print(f"初始: {dq}")

    dq.append(6)      # 右端添加，自动丢弃左端的 1
    print(f"append(6): {dq}")

    dq.appendleft(0)  # 左端添加，自动丢弃右端的 6
    print(f"appendleft(0): {dq}")

    # 旋转
    dq.rotate(2)
    print(f"rotate(2): {dq}")

    dq.rotate(-2)
    print(f"rotate(-2): {dq}")

    # 作为栈（后进先出）
    print("\n作为栈:")
    stack = collections.deque()
    stack.append(1)
    stack.append(2)
    stack.append(3)
    print(f"pop: {stack.pop()}")  # 3

    # 作为队列（先进先出）
    print("\n作为队列:")
    queue = collections.deque()
    queue.append(1)
    queue.append(2)
    queue.append(3)
    print(f"popleft: {queue.popleft()}")  # 1
    print()


# ============================================================
# 4. namedtuple - 命名元组
# ============================================================
# 面试官问: namedtuple 有什么用？
#
# 标准答:
# namedtuple 是一个带字段名的 tuple：
# - 可以用 .name 访问，比 [index] 更可读
# - 不可变（像 tuple）
# - 比 class 更轻量
#
# 使用场景:
# - 替代简单的 class（只有属性，没有方法）
# - 函数返回多个值
# - 数据库查询结果
# ============================================================

def demo_namedtuple():
    """namedtuple 演示"""
    print("=" * 60)
    print("4. namedtuple - 命名元组")
    print("=" * 60)

    # 定义
    Point = collections.namedtuple("Point", ["x", "y"])
    p = Point(3, 4)

    print(f"Point: {p}")
    print(f"p.x={p.x}, p.y={p.y}")  # 用名字访问

    # 转换为字典
    print(f"_asdict(): {p._asdict()}")

    # 创建新实例（修改一个字段）
    p2 = p._replace(x=10)
    print(f"_replace(x=10): {p2}")

    # 带默认值（Python 3.6+）
    Employee = collections.namedtuple("Employee", ["name", "age", "dept"], defaults=["IT"])
    e = Employee("Alice", 30)
    print(f"\nEmployee: {e}")
    print()


# ============================================================
# 5. ChainMap - 链式映射
# ============================================================
# 面试官问: ChainMap 是什么？
#
# 标准答:
# ChainMap 将多个字典组合成一个视图：
# - 查找时按顺序查找，返回第一个匹配的
# - 修改只影响第一个字典
#
# 使用场景:
# - 配置管理（默认配置 + 用户配置 + 环境变量）
# - 变量作用域
# ============================================================

def demo_chainmap():
    """ChainMap 演示"""
    print("=" * 60)
    print("5. ChainMap - 链式映射")
    print("=" * 60)

    defaults = {"color": "red", "size": "medium", "debug": False}
    user_prefs = {"color": "blue", "debug": True}
    env_vars = {"HOST": "localhost"}

    # 优先级: user_prefs > defaults
    settings = collections.ChainMap(user_prefs, defaults)
    print(f"color: {settings['color']}")    # blue（user_prefs 优先）
    print(f"size: {settings['size']}")      # medium（从 defaults 获取）
    print(f"debug: {settings['debug']}")    # True

    # 添加新的映射层
    settings = settings.new_child(env_vars)
    print(f"\n添加 env_vars 层:")
    print(f"HOST: {settings['HOST']}")
    print(f"color: {settings['color']}")
    print()


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    demo_counter()
    demo_defaultdict()
    demo_deque()
    demo_namedtuple()
    demo_chainmap()
