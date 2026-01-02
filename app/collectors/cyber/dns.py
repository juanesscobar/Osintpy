import dns.resolver
from typing import Dict, Any, List
from collectors.base import BaseCollector
from utils.validators import DataValidator
from core.logging import logger

class DNSCollector(BaseCollector):
    """Collector for DNS records"""

    async def collect(self, target: str) -> Dict[str, Any]:
        """Collect DNS records for a domain"""
        if not DataValidator.validate_domain(target):
            return {"error": "Invalid domain"}

        results = {
            "domain": target,
            "records": {},
            "nameservers": [],
            "mx_records": []
        }

        try:
            # Query different DNS record types
            record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS']

            for record_type in record_types:
                records = await self._query_dns(target, record_type)
                if records:
                    results["records"][record_type] = records

            # Get nameservers
            ns_records = results["records"].get("NS", [])
            results["nameservers"] = [str(r) for r in ns_records]

            # Get MX records
            mx_records = results["records"].get("MX", [])
            results["mx_records"] = [str(r) for r in mx_records]

            logger.info(f"Collected DNS data for {target}")

        except Exception as e:
            logger.error(f"Error collecting DNS data for {target}: {str(e)}")
            results["error"] = str(e)

        return results

    async def _query_dns(self, domain: str, record_type: str) -> List[str]:
        """Query specific DNS record type"""
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, record_type)
            return [str(rdata) for rdata in answers]
        except Exception as e:
            logger.debug(f"No {record_type} records for {domain}: {str(e)}")
            return []