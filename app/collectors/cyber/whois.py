import whois
from typing import Dict, Any
from collectors.base import BaseCollector
from utils.validators import DataValidator
from utils.parsers import DataParser
from core.logging import logger

class WhoisCollector(BaseCollector):
    """Collector for WHOIS information"""

    async def collect(self, target: str) -> Dict[str, Any]:
        """Collect WHOIS information for a domain"""
        if not DataValidator.validate_domain(target):
            return {"error": "Invalid domain"}

        results = {
            "domain": target,
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "updated_date": None,
            "name_servers": [],
            "status": [],
            "emails": [],
            "raw_whois": None
        }

        try:
            # Query WHOIS information
            w = whois.whois(target)

            if w:
                results.update({
                    "registrar": w.registrar,
                    "creation_date": str(w.creation_date) if w.creation_date else None,
                    "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                    "updated_date": str(w.updated_date) if w.updated_date else None,
                    "name_servers": w.name_servers or [],
                    "status": w.status or [],
                    "emails": w.emails or [],
                    "raw_whois": str(w)
                })

                # Parse additional info from raw WHOIS
                if results["raw_whois"]:
                    parsed = DataParser.parse_whois(results["raw_whois"])
                    results.update(parsed)

            logger.info(f"Collected WHOIS data for {target}")

        except Exception as e:
            logger.error(f"Error collecting WHOIS data for {target}: {str(e)}")
            results["error"] = str(e)

        return results