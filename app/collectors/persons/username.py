from typing import Dict, Any, List
from collectors.base import BaseCollector
from utils.validators import DataValidator
from core.logging import logger

class UsernameCollector(BaseCollector):
    """Collector for username OSINT data"""

    async def collect(self, target: str) -> Dict[str, Any]:
        """Collect username information from social media"""
        if not DataValidator.validate_username(target):
            return {"error": "Invalid username"}

        results = {
            "username": target,
            "platforms": {},
            "found_profiles": []
        }

        platforms = ["twitter", "instagram", "github", "linkedin"]

        try:
            for platform in platforms:
                profile_data = await self._check_platform(target, platform)
                if profile_data:
                    results["platforms"][platform] = profile_data
                    results["found_profiles"].append(platform)

            results["profile_count"] = len(results["found_profiles"])
            logger.info(f"Collected username data for {target}")

        except Exception as e:
            logger.error(f"Error collecting username data for {target}: {str(e)}")
            results["error"] = str(e)

        return results

    async def _check_platform(self, username: str, platform: str) -> Dict[str, Any]:
        """Check if username exists on a specific platform"""
        # For MVP, simulate checks
        # In real implementation, check actual APIs or scraping
        mock_profiles = {
            "twitter": {"exists": True, "url": f"https://twitter.com/{username}"},
            "github": {"exists": True, "url": f"https://github.com/{username}"},
            "instagram": {"exists": False},
            "linkedin": {"exists": True, "url": f"https://linkedin.com/in/{username}"}
        }

        return mock_profiles.get(platform, {"exists": False})