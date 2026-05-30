"""
魔法方法 02: 字符串表示与比较运算
==================================

面试高频问题:
1. __str__ 和 __repr__ 的区别？
2. 为什么定义了 __eq__ 还要定义 __hash__？
3. @total_ordering 是什么？

核心要点:
- __str__: 面向用户，print() 时调用，要求可读性
- __repr__: 面向开发者，交互式环境显示，要求明确性
- __eq__: 判断相等，定义后会丢失默认的 hash（变成不可哈希）
- __hash__: 哈希值，用于 set/dict 的 key
"""


from functools import total_ordering


# ============================================================
# 1. __str__ vs __repr__
# ============================================================
# 面试官问: __str__ 和 __repr__ 有什么区别？
#
# 标准答:
# | 特性     | __str__          | __repr__           |
# |---------|------------------|---------------------|
# | 目标用户 | 终端用户          | 开发者              |
# | 可读性   | 要求好读          | 要求明确（能还原对象）|
# | 调用方式 | print(), str()   | 交互式环境, repr()  |
# | 必须实现 | 否               | 是（调试必备）       |
#
# 最佳实践:
# - 总是实现 __repr__（方便调试）
# - 只在需要用户友好输出时实现 __str__
# - __repr__ 应该返回能重建对象的字符串，如 "Vector(x=3, y=4)"
# - 如果没实现 __str__，print() 会 fallback 到 __repr__
# ============================================================

class Vector:
    """
    二维向量类 - 演示 __str__ 和 __repr__

    运行结果:
        str: (3, 4)                  # 面向用户：简洁
        repr: Vector(x=3, y=4)      # 面向开发者：能还原对象
        print 直接调用: (3, 4)       # print() 用 __str__
        list 中显示: [Vector(x=1, y=2), Vector(x=3, y=4)]  # list 用 __repr__
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """
        面向用户的可读表示

        调用时机:
            - print(obj)
            - str(obj)
            - f"{obj}"
        """
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """
        面向开发者的明确表示

        调用时机:
            - 交互式环境直接输入 obj
            - repr(obj)
            - 对象在容器中显示（如 list, dict）
            - f"{obj!r}"

        最佳实践:
            返回能用 eval() 重建对象的字符串
        """
        return f"Vector(x={self.x}, y={self.y})"

    # 没有 __str__ 时，print() 会使用 __repr__
    # 所以至少要实现 __repr__


# ============================================================
# 2. __eq__ 和 __hash__ 的关系
# ============================================================
# 面试官问: 为什么定义了 __eq__ 后对象就不能放入 set 了？
#
# 标准答:
# Python 的规则是：
# - 如果定义了 __eq__ 但没定义 __hash__，对象会变成不可哈希（unhashable）
# - 这是为了保证一致性：如果 a == b，那么 hash(a) 必须等于 hash(b)
# - 默认的 __hash__ 是基于 id() 的，自定义 __eq__ 后就不一致了
#
# 解决方案:
# - 如果对象需要可变（属性可改）：只定义 __eq__，不定义 __hash__（不可放入 set/dict）
# - 如果对象需要不可变（属性不可改）：同时定义 __eq__ 和 __hash__
# - 如果用 @dataclass(frozen=True)，会自动同时生成两者
# ============================================================

@total_ordering
class Temperature:
    """
    温度类 - 演示比较运算符

    @total_ordering 的作用:
        只需要定义 __eq__ 和 __lt__，
        它会自动生成 __le__, __gt__, __ge__

    运行结果:
        Temperature(20°C) == Temperature(20°C): True
        Temperature(20°C) < Temperature(30°C): True
        Temperature(20°C) > Temperature(30°C): False
        Temperature(20°C) <= Temperature(30°C): True
        sorted: [Temperature(10°C), Temperature(20°C), Temperature(30°C)]
    """

    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        """
        判断相等 ==

        注意:
            1. 要检查类型，避免不同类型比较出错
            2. 定义 __eq__ 后，默认的 __hash__ 会变成 None（不可哈希）
            3. 如果要让对象可哈希，需要同时定义 __hash__
        """
        if not isinstance(other, Temperature):
            return NotImplemented  # 返回 NotImplemented 让 Python 尝试 other.__eq__
        return self.celsius == other.celsius

    def __lt__(self, other):
        """
        小于比较 <

        注意:
            返回 NotImplemented 而不是 raise TypeError
            Python 会尝试 other.__gt__ 来处理
        """
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius

    def __hash__(self):
        """
        哈希值 - 用于 set 和 dict

        规则:
            1. 相等的对象必须有相同的哈希值
            2. 不相等的对象尽量有不同的哈希值（减少冲突）
            3. 哈希值在对象生命周期内应该不变

        实现技巧:
            用所有参与 __eq__ 判断的属性来计算哈希
        """
        return hash(self.celsius)

    def __repr__(self):
        return f"Temperature({self.celsius}°C)"


# ============================================================
# 3. 容器协议 - 让对象表现得像 list/dict
# ============================================================
# 面试官问: 怎么让一个类支持 len() 和 in 操作？
#
# 标准答:
# 实现容器协议的魔法方法：
# - __len__: 支持 len(obj)
# - __getitem__: 支持 obj[key] 和迭代
# - __contains__: 支持 item in obj
# - __iter__: 支持 for 循环
# - __setitem__: 支持 obj[key] = value
# - __delitem__: 支持 del obj[key]
# ============================================================

class SortedList:
    """
    有序列表 - 演示容器协议

    特点:
        1. 自动排序（插入时维护顺序）
        2. 支持所有容器操作

    运行结果:
        SortedList: SortedList([1, 2, 3, 5, 8])
        len: 5
        3 in list: True
        list[0]: 1
        reversed: [8, 5, 3, 2, 1]
        for 循环: 1 2 3 5 8
    """

    def __init__(self, data=None):
        self._data = sorted(data) if data else []

    def __len__(self):
        """
        支持 len(obj)

        要求: 返回非负整数
        """
        return len(self._data)

    def __getitem__(self, index):
        """
        支持 obj[key]

        参数:
            index: 可以是整数（索引）或 slice（切片）

        注意:
            实现了 __getitem__，对象就自动支持迭代！
            Python 遇到 for x in obj 时，会尝试调用 obj.__iter__()，
            如果没有，就用 __getitem__ 配合 0, 1, 2, ... 来迭代
        """
        return self._data[index]

    def __setitem__(self, index, value):
        """支持 obj[key] = value"""
        # 插入后重新排序
        self._data[index] = value
        self._data.sort()

    def __delitem__(self, index):
        """支持 del obj[key]"""
        del self._data[index]

    def __contains__(self, item):
        """
        支持 item in obj

        优化:
            对于有序列表，可以用二分查找 O(log n)
            这里为了简单用线性查找 O(n)
        """
        return item in self._data

    def __iter__(self):
        """
        支持 for 循环

        返回一个迭代器对象（这里直接返回 list 的迭代器）
        """
        return iter(self._data)

    def __reversed__(self):
        """支持 reversed(obj)"""
        return reversed(self._data)

    def __add__(self, other):
        """
        支持 obj1 + obj2

        注意:
            返回新对象，不修改原对象（不可变语义）
        """
        if isinstance(other, SortedList):
            return SortedList(self._data + other._data)
        return NotImplemented

    def __iadd__(self, other):
        """
        支持 obj1 += obj2

        注意:
            这是就地修改，修改原对象并返回 self
        """
        if isinstance(other, SortedList):
            self._data.extend(other._data)
            self._data.sort()
            return self
        return NotImplemented

    def __repr__(self):
        return f"SortedList({self._data})"


# ============================================================
# 主函数
# ============================================================

def demo_string_repr():
    """演示 __str__ vs __repr__"""
    print("=" * 60)
    print("1. __str__ vs __repr__")
    print("=" * 60)

    v = Vector(3, 4)
    print(f"str: {str(v)}")        # 调用 __str__
    print(f"repr: {repr(v)}")      # 调用 __repr__
    print(f"print 直接调用: {v}")   # print() 调用 __str__
    print(f"f-string !r: {v!r}")   # !r 强制用 __repr__

    # 在容器中显示的是 __repr__
    vectors = [Vector(1, 2), Vector(3, 4)]
    print(f"list 中显示: {vectors}")  # 调用每个元素的 __repr__
    print()


def demo_comparison():
    """演示比较运算符"""
    print("=" * 60)
    print("2. 比较运算符")
    print("=" * 60)

    t1 = Temperature(20)
    t2 = Temperature(30)
    t3 = Temperature(20)

    print(f"{t1} == {t3}: {t1 == t3}")   # True
    print(f"{t1} < {t2}: {t1 < t2}")     # True
    print(f"{t1} > {t2}: {t1 > t2}")     # False
    print(f"{t1} <= {t2}: {t1 <= t2}")   # True（@total_ordering 自动生成）

    # 排序
    temps = [Temperature(30), Temperature(10), Temperature(20)]
    print(f"sorted: {sorted(temps)}")

    # 哈希（可以用作 dict 的 key）
    temp_dict = {Temperature(100): "沸点", Temperature(0): "冰点"}
    print(f"dict 查找: {temp_dict[Temperature(100)]}")
    print()


def demo_container():
    """演示容器协议"""
    print("=" * 60)
    print("3. 容器协议")
    print("=" * 60)

    sl = SortedList([5, 3, 8, 1, 2])
    print(f"SortedList: {sl}")
    print(f"len: {len(sl)}")
    print(f"3 in list: {3 in sl}")
    print(f"list[0]: {sl[0]}")
    print(f"reversed: {list(reversed(sl))}")

    # for 循环
    print("for 循环:", end=" ")
    for x in sl:
        print(x, end=" ")
    print()

    # 合并
    sl2 = SortedList([4, 6])
    print(f"sl + sl2: {sl + sl2}")

    # 切片
    print(f"sl[1:3]: {sl[1:3]}")
    print()


if __name__ == "__main__":
    demo_string_repr()
    demo_comparison()
    demo_container()
