import logging
import requests
import time

from urllib.parse import urljoin
from typing import Optional, Any

logger = logging.getLogger(__name__)


class Scraper():
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key
        self.base_url = base_url or "https://scrapeapi.pangolinfo.com"
        if not self.api_key:
            raise ValueError("API key is required")

    def _prepare_headers(self):
        """生成请求头，包含认证信息"""
        headers = {"Content-Type": "application/json"}
        headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
        retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> dict:
        if not headers:
            headers = self._prepare_headers()
        for i in range(retries):
            try:
                response = requests.request(method, url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException:
                if i < retries - 1:
                    time.sleep(backoff_factor * (2**i))
                else:
                    raise
        raise RuntimeError("Unexpected end of retry loop")

    def scrape(self, uri: Optional[str] = None, **kwargs: Any) -> Any:
        """
        发起抓取请求。

        :param uri: 可选的API路径，默认为 '/api/v2/scrape'
        :param kwargs: 请求体参数
        :return: 请求响应
        """
        # 使用 urljoin 安全拼接，避免重复斜杠问题
        path = uri or "/api/v1/scrape"
        endpoint = urljoin(self.base_url, path)

        # 记录请求信息（注意：生产环境可能需隐藏敏感数据）
        logger.debug("POST %s with body: %s", endpoint, kwargs)

        # 调用底层请求方法
        return self._request("POST", endpoint, data=kwargs)
