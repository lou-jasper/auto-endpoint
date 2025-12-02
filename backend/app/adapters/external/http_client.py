import asyncio
import logging
from typing import Any, Dict, Optional, Union, NoReturn

import httpx

logger = logging.getLogger(__name__)


class AsyncHttpClient:
    """
    一个支持重试、链式配置、自动构建 URL 的 httpx 异步请求封装。
    """

    def __init__(
            self,
            *,
            base_url: Optional[str] = None,
            timeout: Union[int, float, httpx.Timeout] = 30,
            retries: int = 3,
            headers: Optional[Dict[str, str]] = None,
            cookies: Optional[Dict[str, str]] = None,
            auth: Optional[Any] = None,
            verify: Union[bool, str] = True,
            proxy: Optional[Union[str, Dict]] = None,
            limits: Optional[httpx.Limits] = httpx.Limits(),
            params: Optional[Dict[str, str]] = None,
    ) -> None:

        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries
        self.headers = headers or {}  # FIXED
        self.cookies = cookies or {}  # FIXED
        self.params = params or {}  # FIXED
        self.auth = auth
        self.verify = verify
        self.proxy = proxy
        self.limits = limits

        self._client: Optional[httpx.AsyncClient] = None

    # ----------------------------
    # 链式设置（Fluent API）
    # ----------------------------
    def with_base_url(self, base_url: str) -> "AsyncHttpClient":
        self.base_url = base_url
        return self

    def with_timeout(self, timeout: Union[int, float]) -> "AsyncHttpClient":
        self.timeout = timeout
        return self

    def with_retries(self, retries: int) -> "AsyncHttpClient":
        self.retries = retries
        return self

    def with_header(self, key: str, value: str) -> "AsyncHttpClient":
        self.headers[key] = value
        return self

    def with_cookie(self, key: str, value: str) -> "AsyncHttpClient":
        self.cookies[key] = value
        return self

    def with_param(self, key: str, value: str) -> "AsyncHttpClient":
        self.params[key] = value
        return self

    def with_auth(self, auth: Any) -> "AsyncHttpClient":
        self.auth = auth
        return self

    def with_verify(self, verify: Union[bool, str]) -> "AsyncHttpClient":
        self.verify = verify
        return self

    def with_proxies(self, proxy: Optional[Union[str, Dict]]) -> "AsyncHttpClient":
        self.proxy = proxy
        return self

    def with_limits(self, limits: Optional[httpx.Limits]) -> "AsyncHttpClient":
        self.limits = limits
        return self

    # ----------------------------
    # 内部函数
    # ----------------------------
    def _build_url(self, endpoint: str) -> str:
        if not self.base_url:
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _raise_final_error(self, url: str) -> NoReturn:
        raise httpx.HTTPError(f"请求失败（重试{self.retries}次）: {url}")

    async def _ensure_client(self):
        if not self._client:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers,
                cookies=self.cookies,
                auth=self.auth,
                verify=self.verify,
                proxy=self.proxy,
                limits=self.limits,
            )

    # ----------------------------
    # 核心请求方法
    # ----------------------------
    async def _request(
            self,
            method: str,
            endpoint: str,
            *,
            params: Optional[Dict] = None,
            json: Any = None,
            data: Any = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            cookies: Optional[Dict[str, str]] = None,
            timeout: Optional[Union[int, float, httpx.Timeout]] = None,
    ) -> Dict[str, Any]:

        await self._ensure_client()

        url = self._build_url(endpoint)

        # 合并全局 + 局部 headers/cookies/params
        merged_headers = {**self.headers, **(headers or {})}
        merged_cookies = {**self.cookies, **(cookies or {})}
        merged_params = {**self.params, **(params or {})}

        retry_exceptions = (
            httpx.ConnectError,
            httpx.ReadTimeout,
            httpx.WriteTimeout,
            httpx.HTTPStatusError,
        )

        for attempt in range(self.retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=merged_params,
                    json=json,
                    data=data,
                    files=files,
                    headers=merged_headers,
                    cookies=merged_cookies,
                    timeout=timeout,
                )
                response.raise_for_status()

                try:
                    content = response.json()
                except ValueError:
                    content = response.text

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "data": content,
                    "text": response.text,
                }

            except retry_exceptions as e:
                logger.warning("请求失败 (%d/%d): %s", attempt + 1, self.retries, str(e))

                if isinstance(e, httpx.HTTPStatusError) and 400 <= e.response.status_code < 500:
                    raise

                if attempt == self.retries - 1:
                    self._raise_final_error(url)

                await asyncio.sleep(0.5 * (attempt + 1))

        self._raise_final_error(url)

    # ----------------------------
    # 常用方法封装
    # ----------------------------
    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("DELETE", endpoint, **kwargs)

    # ----------------------------
    # Async Context Manager
    # ----------------------------
    async def __aenter__(self) -> "AsyncHttpClient":
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None



