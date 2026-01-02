import re
from typing import Optional

class DataValidator:
    """Utility class for validating OSINT data"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format"""
        if not email or not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def validate_domain(domain: str) -> bool:
        """Validate domain name format"""
        if not domain or not isinstance(domain, str):
            return False
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain.strip()))

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format (alphanumeric, underscore, dash)"""
        if not username or not isinstance(username, str):
            return False
        pattern = r'^[a-zA-Z0-9_-]{3,30}$'
        return bool(re.match(pattern, username.strip()))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number (basic validation)"""
        if not phone or not isinstance(phone, str):
            return False
        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone.strip())
        # Check if it's digits only and reasonable length
        return clean_phone.isdigit() and 7 <= len(clean_phone) <= 15

    @staticmethod
    def validate_ruc(ruc: str) -> bool:
        """Validate RUC format (Paraguay)"""
        if not ruc or not isinstance(ruc, str):
            return False
        # RUC in Paraguay is typically 9 digits
        clean_ruc = ruc.strip().replace('-', '').replace('.', '')
        return clean_ruc.isdigit() and len(clean_ruc) == 9

    @staticmethod
    def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
        """Sanitize text input by removing potentially harmful characters"""
        if not text:
            return ""
        # Remove null bytes and other control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        if max_length:
            sanitized = sanitized[:max_length]
        return sanitized.strip()

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            return False
        pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))*)?$'
        return bool(re.match(pattern, url.strip()))

    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """Validate IPv4 address"""
        if not ip or not isinstance(ip, str):
            return False
        pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip.strip()))