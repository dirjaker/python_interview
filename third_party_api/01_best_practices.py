"""
第三方 API 调用最佳实践 — 面试高频问题
========================================

面试高频问题：
1. 调用第三方 API 时如何处理超时和重试？
2. 什么是熔断器模式？为什么需要它？
3. 如何安全地管理 API Key？
4. 如何处理第三方 API 的限流（Rate Limiting）？
5. 同步 vs 异步调用第三方 API 的取舍？
6. 如何保证 API 调用的幂等性？
7. 如何设计一个 API 调用的降级方案？

核心要点：
- 健壮性：超时、重试、熔断、降级
- 安全性：密钥管理、请求签名、数据校验
- 可观测性：日志、指标、链路追踪
- 性能：连接池、并发控制、缓存
"""

import time
import json
import hashlib
import hmac
import logging
import asyncio
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

import httpx

# ============================================================
# 1. 超时与重试策略
# ============================================================
"""
面试考点：
- 连接超时 vs 读超时 vs 总超时 的区别
- 重试策略：固定间隔 / 指数退避 / 抖动
- 哪些错误应该重试，哪些不应该？
- 如何避免重试风暴（Retry Storm）？

关键点：
- 网络错误、5xx、429 可以重试
- 4xx（除 429）不应该重试（客户端错误）
- 指数退避 + 随机抖动避免惊群效应
- 设置最大重试次数，防止无限重试
"""


@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3               # 最大重试次数
    base_delay: float = 1.0            # 基础延迟（秒）
    max_delay: float = 60.0            # 最大延迟（秒）
    exponential_base: float = 2.0      # 指数底数
    jitter: bool = True                # 是否加随机抖动
    retryable_status: set = field(default_factory=lambda: {429, 500, 502, 503, 504})


class RetryableError(Exception):
    """可重试的错误"""
    pass


def calculate_delay(retry_config: RetryConfig, attempt: int) -> float:
    """
    计算重试延迟（指数退避 + 抖动）

    面试追问：为什么需要抖动（Jitter）？
    答：如果没有抖动，多个客户端在相同时间点失败后，
        会在完全相同的时间点同时重试，导致流量尖峰（惊群效应）。
        抖动将重试时间分散开，平滑流量。
    """
    import random
    delay = min(
        retry_config.base_delay * (retry_config.exponential_base ** attempt),
        retry_config.max_delay
    )
    if retry_config.jitter:
        # 完全抖动：在 [0, delay] 均匀随机
        delay = random.uniform(0, delay)
    return delay


async def call_with_retry(
    func: Callable,
    retry_config: RetryConfig = None,
    *args, **kwargs
) -> Any:
    """
    带重试的 API 调用包装器

    面试追问：为什么不在 func 内部自己处理重试？
    答：重试是横切关注点（cross-cutting concern），
        应该和业务逻辑分离，用装饰器/高阶函数实现，
        这样每个 API 调用都可以复用同一套重试逻辑。
    """
    if retry_config is None:
        retry_config = RetryConfig()

    last_exception = None

    for attempt in range(retry_config.max_retries + 1):
        try:
            result = await func(*args, **kwargs)
            return result
        except httpx.TimeoutException as e:
            last_exception = e
            logging.warning(f"超时 (attempt {attempt + 1}): {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code in retry_config.retryable_status:
                last_exception = e
                # 如果服务器返回 Retry-After 头，使用它
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    delay = float(retry_after)
                else:
                    delay = calculate_delay(retry_config, attempt)
                logging.warning(
                    f"HTTP {e.response.status_code} (attempt {attempt + 1}), "
                    f"等待 {delay:.1f}s 后重试"
                )
                await asyncio.sleep(delay)
                continue
            else:
                raise  # 4xx 错误不重试
        except Exception as e:
            last_exception = e
            logging.warning(f"未知错误 (attempt {attempt + 1}): {e}")

        if attempt < retry_config.max_retries:
            delay = calculate_delay(retry_config, attempt)
            await asyncio.sleep(delay)

    raise last_exception


# ============================================================
# 2. 熔断器模式（Circuit Breaker）
# ============================================================
"""
面试考点：
- 熔断器的三种状态：关闭、打开、半开
- 熔断器和重试的区别？为什么要同时使用？
- 熔断器的阈值怎么设置？

关键点：
- 重试：针对单次请求的容错
- 熔断：针对服务整体健康状况的保护
- 当错误率超过阈值，熔断器打开，直接快速失败
- 经过冷却时间后进入半开状态，试探服务是否恢复
- 防止一个故障的下游服务拖垮整个系统
"""


class CircuitState(Enum):
    """熔断器状态"""
    CLOSED = "closed"       # 正常：请求正常通过
    OPEN = "open"           # 熔断：请求直接失败
    HALF_OPEN = "half_open" # 半开：允许少量请求试探


@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    failure_threshold: int = 5         # 连续失败多少次触发熔断
    recovery_timeout: float = 30.0     # 熔断后多久进入半开状态（秒）
    success_threshold: int = 2         # 半开状态下连续成功多少次关闭熔断
    monitor_window: float = 60.0       # 监控窗口（秒）


class CircuitBreaker:
    """
    熔断器实现

    面试追问：如何在分布式系统中实现熔断器？
    答：单机版可以用内存中的状态机。分布式场景下可以用 Redis
        存储熔断状态，或者使用专门的服务网格（如 Istio）提供的
        熔断能力。Sentinel、Hystrix 也是常用方案。
    """

    def __init__(self, config: CircuitBreakerConfig = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.last_state_change: datetime = datetime.now()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """通过熔断器执行调用"""
        self._check_state_transition()

        if self.state == CircuitState.OPEN:
            raise CircuitBreakerOpenError(
                f"熔断器已打开，拒绝请求。"
                f"将在 {self._time_until_half_open():.0f}s 后尝试恢复"
            )

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _check_state_transition(self):
        """检查是否需要状态转换"""
        if self.state == CircuitState.OPEN:
            # 检查是否可以进入半开状态
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.config.recovery_timeout:
                    self._transition_to(CircuitState.HALF_OPEN)

    def _on_success(self):
        """成功时的处理"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._transition_to(CircuitState.CLOSED)
        else:
            self.failure_count = 0  # 重置连续失败计数

    def _on_failure(self):
        """失败时的处理"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            # 半开状态下失败，立即回到打开状态
            self._transition_to(CircuitState.OPEN)
        elif self.failure_count >= self.config.failure_threshold:
            self._transition_to(CircuitState.OPEN)

    def _transition_to(self, new_state: CircuitState):
        """状态转换"""
        old_state = self.state
        self.state = new_state
        self.last_state_change = datetime.now()
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.success_count = 0
        elif new_state == CircuitState.HALF_OPEN:
            self.success_count = 0
        logging.info(f"熔断器状态变更: {old_state.value} → {new_state.value}")

    def _time_until_half_open(self) -> float:
        """距进入半开状态的剩余时间"""
        if not self.last_failure_time:
            return 0
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return max(0, self.config.recovery_timeout - elapsed)


class CircuitBreakerOpenError(Exception):
    """熔断器打开异常"""
    pass


# ============================================================
# 3. API Key 安全管理
# ============================================================
"""
面试考点：
- API Key 为什么不能硬编码在代码中？
- 如何安全管理 API Key？有哪些方案？
- 如何实现 API Key 的轮转（Rotation）？
- 请求签名的作用是什么？

关键点：
- 环境变量 > 配置文件 > 硬编码（安全性递减）
- 使用 Secret Manager（如 Vault、AWS Secrets Manager）
- Key 轮转：新旧 Key 并行期 → 切换 → 旧 Key 废弃
- 请求签名防止请求被篡改
"""


class APIKeyManager:
    """
    API Key 管理器

    面试追问：如果 API Key 泄露了怎么办？
    答：
    1. 立即吊销泄露的 Key
    2. 生成新 Key 并更新所有使用处
    3. 审计日志：检查泄露 Key 的所有调用记录
    4. 排查泄露途径（代码仓库、日志、网络抓包）
    5. 后续：使用短生命周期 Token、IP 白名单、最小权限原则
    """

    def __init__(self):
        self._keys: dict[str, dict] = {}  # provider -> {key, expires_at, ...}

    def register_key(
        self,
        provider: str,
        key: str,
        expires_in: Optional[int] = None,  # 秒
        metadata: dict = None
    ):
        """
        注册 API Key

        面试追问：为什么要给 Key 设置过期时间？
        答：即使 Key 泄露，过期后自动失效，限制泄露的影响窗口。
            短生命周期的 Key 是零信任安全架构的一部分。
        """
        self._keys[provider] = {
            "key": key,
            "created_at": datetime.now(),
            "expires_at": (
                datetime.now() + timedelta(seconds=expires_in)
                if expires_in else None
            ),
            "metadata": metadata or {},
        }

    def get_key(self, provider: str) -> str:
        """获取 API Key，过期则抛异常"""
        if provider not in self._keys:
            raise KeyError(f"未注册的 API 提供商: {provider}")

        info = self._keys[provider]
        if info["expires_at"] and datetime.now() > info["expires_at"]:
            raise PermissionError(f"API Key 已过期: {provider}")

        return info["key"]

    def rotate_key(self, provider: str, new_key: str, overlap_seconds: int = 3600):
        """
        Key 轮转：新旧 Key 并行期

        面试追问：为什么需要并行期？
        答：分布式系统中，不同节点可能缓存了旧 Key。
            并行期允许旧请求（使用旧 Key）仍然被接受，
            避免轮转瞬间的请求失败。
        """
        old_info = self._keys.get(provider)
        self.register_key(
            provider, new_key,
            metadata={"rotated_from": old_info["key"][:8] + "..." if old_info else None}
        )


def sign_request(secret: str, method: str, path: str, body: str = "") -> str:
    """
    请求签名（HMAC-SHA256）

    面试追问：请求签名和 HTTPS 有什么区别？
    答：
    - HTTPS 保证传输安全（防窃听、防篡改）
    - 请求签名保证请求的完整性（防重放、防篡改）和来源认证
    - 即使 HTTPS 终止于反向代理，签名仍然保护端到端完整性
    - 签名通常包含时间戳，防止重放攻击
    """
    timestamp = str(int(time.time()))
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    signature = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).hexdigest()
    return f"{timestamp}.{signature}"


# ============================================================
# 4. 限流处理（Rate Limiting）
# ============================================================
"""
面试考点：
- 客户端限流 vs 服务端限流
- 常见的限流算法：令牌桶、漏桶、滑动窗口
- 收到 429 响应后应该怎么做？
- 如何在客户端实现自适应限流？

关键点：
- 客户端限流：保护自己不过度调用
- 服务端限流：保护服务不被打垮
- 429 响应的 Retry-After 头要遵守
- 本地限流可以用令牌桶，分布式用 Redis
"""


class TokenBucket:
    """
    令牌桶限流器

    面试追问：令牌桶和漏桶的区别？
    答：
    - 漏桶：以固定速率处理请求，平滑流量，但不允许突发
    - 令牌桶：以固定速率生成令牌，允许桶内积累，
      短时间内可以消耗积累的令牌处理突发流量
    - 令牌桶更灵活，大多数 API 网关用令牌桶
    """

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: 每秒生成的令牌数
            capacity: 桶的最大容量
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.monotonic()

    async def acquire(self, tokens: int = 1) -> float:
        """
        获取令牌，不够则等待

        Returns:
            等待的时间（秒）
        """
        wait_time = 0.0
        while True:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return wait_time
            # 计算需要等待多久
            deficit = tokens - self.tokens
            wait_time = deficit / self.rate
            await asyncio.sleep(wait_time)

    def _refill(self):
        """补充令牌"""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        self.last_refill = now


class AdaptiveRateLimiter:
    """
    自适应限流器

    面试追问：什么是自适应限流？和固定限流有什么区别？
    答：固定限流用预设的 QPS 上限，自适应限流根据服务端
        响应动态调整。如果服务端返回 429 或延迟增大，
        自动降低请求速率；响应正常则逐渐恢复。
        类似 TCP 的拥塞控制（AIMD）。
    """

    def __init__(
        self,
        initial_rate: float = 10.0,
        min_rate: float = 1.0,
        max_rate: float = 100.0,
        decrease_factor: float = 0.5,
        increase_rate: float = 1.0,
    ):
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.decrease_factor = decrease_factor
        self.increase_rate = increase_rate
        self.bucket = TokenBucket(initial_rate, int(initial_rate))

    def on_success(self):
        """成功时：线性增加速率（类似 TCP 慢启动后的线性增长）"""
        self.current_rate = min(
            self.max_rate,
            self.current_rate + self.increase_rate
        )
        self.bucket = TokenBucket(self.current_rate, int(self.current_rate))

    def on_rate_limited(self):
        """被限流时：乘性减少速率（类似 TCP 拥塞避免）"""
        self.current_rate = max(
            self.min_rate,
            self.current_rate * self.decrease_factor
        )
        self.bucket = TokenBucket(self.current_rate, int(self.current_rate))
        logging.warning(f"触发限流，速率降至 {self.current_rate:.1f} req/s")

    async def acquire(self):
        """获取调用许可"""
        await self.bucket.acquire()


# ============================================================
# 5. 超时配置最佳实践
# ============================================================
"""
面试考点：
- 连接超时、读取超时、总超时分别是什么？
- 超时时间怎么设置？设太长/太短各有什么问题？
- 链路超时 vs 单次超时

关键点：
- 连接超时（connect timeout）：TCP 握手时间，通常 5-10s
- 读取超时（read timeout）：等待响应数据，取决于接口
- 总超时（total timeout）：整个请求生命周期
- 超时太长：线程/连接被占用，雪崩
- 超时太短：正常请求被误杀
"""


@dataclass
class TimeoutConfig:
    """
    超时配置

    面试追问：超时设置遵循什么原则？
    答：
    1. 连接超时：通常 3-10s，不宜太长
    2. 读取超时：根据接口 P99 延迟的 2-3 倍设置
    3. 总超时：考虑重试次数，总时间 = 单次超时 × 重试次数
    4. 链路超时：在调用链中逐级递减（A→B→C，A 的超时 > B 的超时）
    """
    connect_timeout: float = 5.0
    read_timeout: float = 30.0
    write_timeout: float = 10.0
    pool_timeout: float = 10.0

    def to_httpx(self) -> httpx.Timeout:
        """转换为 httpx 的 Timeout 对象"""
        return httpx.Timeout(
            connect=self.connect_timeout,
            read=self.read_timeout,
            write=self.write_timeout,
            pool=self.pool_timeout,
        )


# ============================================================
# 6. 连接池管理
# ============================================================
"""
面试考点：
- 为什么要用连接池？
- 连接池的大小怎么设置？
- 连接池满了怎么办？

关键点：
- 复用 TCP 连接，避免频繁握手
- 连接池大小通常 = 目标并发数
- 过大浪费资源，过小请求排队
- 注意连接的 keep-alive 和空闲超时
"""


def create_client(
    base_url: str = "",
    timeout: TimeoutConfig = None,
    max_connections: int = 100,
    max_keepalive: int = 20,
    api_key: str = None,
) -> httpx.AsyncClient:
    """
    创建配置好的 HTTP 客户端

    面试追问：为什么用 AsyncClient 而不是同步的 Client？
    答：
    1. I/O 密集场景下异步性能远优于同步
    2. 可以并发调用多个 API 而不阻塞
    3. 连接池共享，资源利用率更高
    4. FastAPI 等异步框架中必须用异步客户端
    """
    if timeout is None:
        timeout = TimeoutConfig()

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    transport = httpx.AsyncHTTPTransport(
        limits=httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive,
        ),
    )

    return httpx.AsyncClient(
        base_url=base_url,
        timeout=timeout.to_httpx(),
        transport=transport,
        headers=headers,
        follow_redirects=True,
    )


# ============================================================
# 7. 响应验证与错误处理
# ============================================================
"""
面试考点：
- 如何处理 API 返回的非预期格式？
- 是否应该信任第三方 API 的响应？
- 如何优雅地处理 API 版本变更？

关键点：
- 始终验证响应状态码、Content-Type、数据结构
- 不要信任第三方数据，做防御性编程
- 使用 Pydantic 校验响应数据
- 记录原始响应用于排查
"""

from pydantic import BaseModel, ValidationError


class APIResponse(BaseModel):
    """通用 API 响应模型"""
    code: int = 0
    message: str = ""
    data: Any = None


def validate_response(response: httpx.Response, model: type = None) -> Any:
    """
    验证 API 响应

    面试追问：为什么不直接 response.json()？
    答：
    1. 直接 json() 假设响应一定是 JSON，可能崩溃
    2. 不校验结构，后续代码可能拿到 None 或错误类型
    3. 不记录原始响应，排查问题时无据可查
    4. 不处理 API 版本变更（字段名改动、类型变更）
    """
    # 1. 检查状态码
    response.raise_for_status()

    # 2. 检查 Content-Type
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        logging.warning(f"非预期的 Content-Type: {content_type}")

    # 3. 解析 JSON
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        logging.error(f"JSON 解析失败: {e}, 响应体: {response.text[:500]}")
        raise

    # 4. Pydantic 校验（如果提供了模型）
    if model:
        try:
            return model.model_validate(data)
        except ValidationError as e:
            logging.error(f"响应校验失败: {e}, 原始数据: {data}")
            raise

    return data


# ============================================================
# 8. 缓存策略
# ============================================================
"""
面试考点：
- API 响应缓存的策略有哪些？
- 如何处理缓存一致性问题？
- 什么时候不应该缓存？

关键点：
- 时间缓存（TTL）：最简单，适合变化不频繁的数据
- 条件请求（ETag/If-None-Match）：节省带宽
- 本地缓存 + Redis 缓存：多级缓存
- 不缓存：实时数据、一次性 Token、写操作
"""

from collections import OrderedDict


class TTLCache:
    """
    带 TTL 的 LRU 缓存

    面试追问：缓存穿透、击穿、雪崩分别是什么？怎么解决？
    答：
    - 穿透：查询不存在的数据，缓存永远 miss → 布隆过滤器、缓存空值
    - 击穿：热点 Key 过期瞬间大量请求 → 互斥锁、不过期 + 异步更新
    - 雪崩：大量 Key 同时过期 → TTL 加随机偏移、多级缓存
    """

    def __init__(self, maxsize: int = 128, ttl: float = 300):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expires_at = self._cache[key]
            if time.time() < expires_at:
                # 移到末尾（最近使用）
                self._cache.move_to_end(key)
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: float = None):
        if len(self._cache) >= self.maxsize:
            self._cache.popitem(last=False)  # 淘汰最久未用
        expires_at = time.time() + (ttl or self.ttl)
        self._cache[key] = (value, expires_at)


# ============================================================
# 9. 综合示例：健壮的 API 客户端
# ============================================================
"""
面试考点：把上面所有知识点串起来，设计一个生产级的 API 客户端
"""


class RobustAPIClient:
    """
    生产级第三方 API 客户端

    整合了：
    - 超时配置
    - 重试策略（指数退避 + 抖动）
    - 熔断器
    - 限流器
    - 缓存
    - 响应验证
    - 请求签名
    - 结构化日志
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: TimeoutConfig = None,
        retry_config: RetryConfig = None,
        circuit_config: CircuitBreakerConfig = None,
        rate_limit: float = 10.0,
        cache_ttl: float = 300,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout or TimeoutConfig()
        self.retry_config = retry_config or RetryConfig()
        self.circuit = CircuitBreaker(circuit_config)
        self.rate_limiter = AdaptiveRateLimiter(initial_rate=rate_limit)
        self.cache = TTLCache(ttl=cache_ttl)
        self.client: Optional[httpx.AsyncClient] = None

        # 指标统计
        self.stats = {"requests": 0, "successes": 0, "failures": 0, "cache_hits": 0}

    async def __aenter__(self):
        self.client = create_client(
            base_url=self.base_url,
            timeout=self.timeout,
            api_key=self.api_key,
        )
        return self

    async def __aexit__(self, *args):
        if self.client:
            await self.client.aclose()

    async def get(self, path: str, params: dict = None, use_cache: bool = True) -> Any:
        """
        发起 GET 请求（带全套保护）

        调用链：缓存 → 限流 → 熔断 → 重试 → HTTP 请求 → 响应验证
        """
        # 1. 检查缓存
        cache_key = f"GET:{path}:{json.dumps(params, sort_keys=True)}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self.stats["cache_hits"] += 1
                return cached

        # 2. 限流等待
        await self.rate_limiter.acquire()

        # 3. 通过熔断器 + 重试执行请求
        async def _do_request():
            self.stats["requests"] += 1
            response = await self.client.get(path, params=params)
            return validate_response(response)

        try:
            result = await self.circuit.call(
                call_with_retry, _do_request, self.retry_config
            )
            self.stats["successes"] += 1
            self.rate_limiter.on_success()

            # 4. 写入缓存
            if use_cache:
                self.cache.set(cache_key, result)

            return result

        except CircuitBreakerOpenError:
            self.stats["failures"] += 1
            logging.error(f"熔断器打开，拒绝请求: {path}")
            raise
        except Exception as e:
            self.stats["failures"] += 1
            self.rate_limiter.on_rate_limited()
            logging.error(f"请求失败: {path}, 错误: {e}")
            raise


# ============================================================
# 10. 幂等性设计
# ============================================================
"""
面试考点：
- 什么是幂等性？为什么 API 调用需要幂等？
- 如何实现幂等的 API 调用？
- GET/PUT/DELETE/POST 哪些是天然幂等的？

关键点：
- 幂等：执行一次和执行多次的效果相同
- GET/PUT/DELETE 天然幂等，POST 不是
- 实现方式：幂等键（Idempotency Key）
- 客户端生成唯一 ID，服务端去重
"""

import uuid


class IdempotentClient:
    """
    幂等 API 调用客户端

    面试追问：幂等键应该由谁生成？怎么传递？
    答：
    - 客户端生成（UUID），通过 Idempotency-Key 头传递
    - 服务端存储键值对：key → 响应结果
    - 相同 key 的重复请求直接返回缓存的响应
    - 键需要设置过期时间（通常 24-48 小时）
    """

    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self._idempotency_store: dict[str, Any] = {}

    async def post(self, path: str, json_data: dict = None, idempotency_key: str = None) -> Any:
        """带幂等键的 POST 请求"""
        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        # 检查是否已有相同 key 的请求
        if idempotency_key in self._idempotency_store:
            logging.info(f"幂等命中: {idempotency_key}")
            return self._idempotency_store[idempotency_key]

        response = await self.client.post(
            path,
            json=json_data,
            headers={"Idempotency-Key": idempotency_key},
        )
        result = validate_response(response)

        # 缓存响应（只缓存成功的）
        if response.status_code < 400:
            self._idempotency_store[idempotency_key] = result

        return result


# ============================================================
# 面试速查
# ============================================================
"""
速记口诀：超重熔限签，缓幂日验连

超时配置 → 重试策略 → 熔断器 → 限流器 → 请求签名
缓存策略 → 幂等设计 → 日志监控 → 响应验证 → 连接池

常见追问：
Q: 一个第三方 API 调用超时了，你的系统会怎样？
A: 超时触发重试（指数退避），连续失败触发熔断，
   熔断后请求快速失败，可以降级返回默认值或缓存数据。

Q: 第三方 API 价格突然涨了怎么办？
A: 1) 缓存减少调用次数
   2) 限流控制成本
   3) 准备备选 API（多供应商策略）
   4) 非核心功能降级

Q: 如何监控第三方 API 的健康状况？
A: 1) 记录每次调用的延迟、状态码
   2) 计算错误率、P50/P99 延迟
   3) 熔断器状态变更时告警
   4) 定期健康检查（Heartbeat）
"""

if __name__ == "__main__":
    # ===== 演示：完整调用流程 =====
    async def demo():
        print("=" * 60)
        print("第三方 API 调用最佳实践 演示")
        print("=" * 60)

        # --- 熔断器演示 ---
        print("\n--- 熔断器演示 ---")
        breaker = CircuitBreaker(CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=5.0,
            success_threshold=2,
        ))
        print(f"初始状态: {breaker.state.value}")

        # 模拟连续失败
        for i in range(4):
            try:
                await breaker.call(asyncio.sleep, 0)  # 模拟调用
                print(f"  调用 {i+1}: 成功")
            except Exception:
                print(f"  调用 {i+1}: 失败")
                print(f"  状态: {breaker.state.value}")

        print(f"\n熔断器状态: {breaker.state.value}")
        print(f"快速失败测试...")
        try:
            await breaker.call(asyncio.sleep, 0)
        except CircuitBreakerOpenError as e:
            print(f"  拒绝请求: {e}")

        # --- 令牌桶限流演示 ---
        print("\n--- 令牌桶限流演示 ---")
        bucket = TokenBucket(rate=5.0, capacity=10)
        print(f"速率: 5 req/s, 容量: 10")

        # 消耗所有令牌
        for i in range(12):
            wait = await bucket.acquire(1)
            if wait > 0:
                print(f"  请求 {i+1}: 等待 {wait:.2f}s")
            else:
                print(f"  请求 {i+1}: 立即通过")

        # --- 缓存演示 ---
        print("\n--- TTL 缓存演示 ---")
        cache = TTLCache(maxsize=3, ttl=2.0)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        print(f"key1: {cache.get('key1')}")
        print(f"key2: {cache.get('key2')}")
        print(f"key3: {cache.get('key3')}")

        print("\n等待 3 秒...")
        await asyncio.sleep(3)
        print(f"key1 (过期后): {cache.get('key1')}")

        # --- 请求签名演示 ---
        print("\n--- 请求签名演示 ---")
        sig = sign_request("my-secret-key", "POST", "/api/v1/chat", '{"msg":"hello"}')
        print(f"签名: {sig}")

        # --- 统计信息 ---
        print("\n--- 统计信息模板 ---")
        client_stats = {
            "requests": 100,
            "successes": 95,
            "failures": 5,
            "cache_hits": 30,
            "avg_latency_ms": 120.5,
            "p99_latency_ms": 450.0,
            "circuit_state": "closed",
        }
        for k, v in client_stats.items():
            print(f"  {k}: {v}")

        print("\n✅ 演示完成")

    asyncio.run(demo())
