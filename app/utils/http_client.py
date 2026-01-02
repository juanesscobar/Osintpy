import aiohttp
import asyncio
from typing import Dict, Any, Optional
from core.logging import logger

class HttpClient:
    """Async HTTP client for OSINT data collection"""

    def __init__(self, timeout: int = 30, user_agent: str = "OSINT-Tool/1.0"):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.user_agent = user_agent
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"User-Agent": self.user_agent}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make GET request"""
        if not self.session:
            async with aiohttp.ClientSession(timeout=self.timeout, headers={"User-Agent": self.user_agent}) as session:
                return await self._get(session, url, params, **kwargs)
        else:
            return await self._get(self.session, url, params, **kwargs)

    async def _get(self, session: aiohttp.ClientSession, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        try:
            async with session.get(url, params=params, **kwargs) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' in content_type:
                        return await response.json()
                    else:
                        return {"text": await response.text()}
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return {"error": f"HTTP {response.status}", "status": response.status}
        except Exception as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return {"error": str(e)}

    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make POST request"""
        if not self.session:
            async with aiohttp.ClientSession(timeout=self.timeout, headers={"User-Agent": self.user_agent}) as session:
                return await self._post(session, url, data, **kwargs)
        else:
            return await self._post(self.session, url, data, **kwargs)

    async def _post(self, session: aiohttp.ClientSession, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        try:
            async with session.post(url, json=data, **kwargs) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    return {"error": f"HTTP {response.status}", "status": response.status}
        except Exception as e:
            logger.error(f"POST request failed for {url}: {str(e)}")
            return {"error": str(e)}