import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

class DataParser:
    """Utility class for parsing OSINT data"""

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(email_pattern, text)))

    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers from text (basic implementation)"""
        # Basic phone pattern - can be enhanced
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        return list(set(re.findall(phone_pattern, text)))

    @staticmethod
    def extract_usernames(text: str) -> List[str]:
        """Extract potential usernames from text"""
        # Look for @mentions or common username patterns
        username_pattern = r'@(\w+)'
        return list(set(re.findall(username_pattern, text)))

    @staticmethod
    def extract_domains(text: str) -> List[str]:
        """Extract domains from text"""
        domain_pattern = r'\b([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        domains = re.findall(domain_pattern, text)
        return list(set(domains))

    @staticmethod
    def parse_whois(raw_whois: str) -> Dict[str, Any]:
        """Parse WHOIS data into structured format"""
        parsed = {}
        lines = raw_whois.split('\n')

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if key and value:
                    parsed[key] = value

        return parsed

    @staticmethod
    def validate_domain(domain: str) -> bool:
        """Validate domain format"""
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def extract_social_profiles(text: str) -> Dict[str, List[str]]:
        """Extract social media profiles from text"""
        profiles = {
            'twitter': [],
            'linkedin': [],
            'facebook': [],
            'instagram': [],
            'github': []
        }

        # Twitter handles
        twitter_pattern = r'@(\w{1,15})'
        profiles['twitter'] = re.findall(twitter_pattern, text)

        # LinkedIn URLs
        linkedin_pattern = r'linkedin\.com/in/([a-zA-Z0-9-]+)'
        profiles['linkedin'] = re.findall(linkedin_pattern, text)

        # GitHub usernames
        github_pattern = r'github\.com/([a-zA-Z0-9-]+)'
        profiles['github'] = re.findall(github_pattern, text)

        return profiles