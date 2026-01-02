from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
from utils.http_client import HttpClient
from core.logging import logger

class BaseCollector(ABC):
    """Base class for OSINT data collectors"""

    def __init__(self, http_client: Optional[HttpClient] = None):
        self.http_client = http_client or HttpClient()
        self.name = self.__class__.__name__

    @abstractmethod
    async def collect(self, target: str) -> Dict[str, Any]:
        """Collect data for the given target"""
        pass

    async def _safe_request(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make a safe HTTP request with error handling"""
        try:
            response = await self.http_client.get(url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Error in {self.name} collecting from {url}: {str(e)}")
            return None

    def _validate_target(self, target: str) -> bool:
        """Validate the target before collecting"""
        if not target or not isinstance(target, str):
            return False
        return True

    async def collect_with_retry(self, target: str, max_retries: int = 3) -> Dict[str, Any]:
        """Collect data with retry logic"""
        for attempt in range(max_retries):
            try:
                if not self._validate_target(target):
                    return {"error": "Invalid target"}

                result = await self.collect(target)
                return result
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {self.name}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return {"error": f"Collection failed after {max_retries} attempts: {str(e)}"}