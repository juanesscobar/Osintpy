from typing import Dict, Any, List
from collectors.base import BaseCollector
from utils.validators import DataValidator
from core.logging import logger

class SubdomainCollector(BaseCollector):
    """Collector for subdomain enumeration"""

    async def collect(self, target: str) -> Dict[str, Any]:
        """Enumerate subdomains for a domain"""
        if not DataValidator.validate_domain(target):
            return {"error": "Invalid domain"}

        results = {
            "domain": target,
            "subdomains": [],
            "active_subdomains": [],
            "total_found": 0
        }

        try:
            # Common subdomain prefixes to check
            common_prefixes = [
                'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
                'blog', 'shop', 'app', 'mobile', 'm', 'secure', 'ssl', 'vpn',
                'remote', 'portal', 'webmail', 'email', 'smtp', 'pop', 'imap'
            ]

            found_subdomains = []

            for prefix in common_prefixes:
                subdomain = f"{prefix}.{target}"
                if await self._check_subdomain_exists(subdomain):
                    found_subdomains.append(subdomain)
                    results["active_subdomains"].append(subdomain)

            results["subdomains"] = found_subdomains
            results["total_found"] = len(found_subdomains)

            logger.info(f"Found {len(found_subdomains)} subdomains for {target}")

        except Exception as e:
            logger.error(f"Error collecting subdomains for {target}: {str(e)}")
            results["error"] = str(e)

        return results

    async def _check_subdomain_exists(self, subdomain: str) -> bool:
        """Check if a subdomain exists by attempting DNS resolution"""
        try:
            import socket
            socket.gethostbyname(subdomain)
            return True
        except socket.gaierror:
            return False