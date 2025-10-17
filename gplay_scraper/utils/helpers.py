"""Helper functions for data processing and manipulation.

This module contains utility functions for:
- Text unescaping and cleaning
- JSON string cleaning
- Date parsing and calculations
- Install metrics calculations
"""

import re
import json
from html import unescape
from typing import Any, List, Optional, Dict
from datetime import datetime, timezone


def unescape_text(s: Optional[str]) -> Optional[str]:
    """Unescape HTML entities and remove HTML tags from text.
    
    Args:
        s: Input string with HTML
        
    Returns:
        Cleaned text without HTML tags
    """
    if s is None:
        return None
    
    text = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = text.replace("<b>", "").replace("</b>", "")
    text = text.replace("<i>", "").replace("</i>", "")
    text = text.replace("<u>", "").replace("</u>", "")
    text = text.replace("<strong>", "").replace("</strong>", "")
    text = text.replace("<em>", "").replace("</em>", "")
    
    text = re.sub(r'<[^>]+>', '', text)
    
    return unescape(text).strip()


def clean_json_string(json_str: str) -> str:
    """Clean malformed JSON string from Google Play Store.
    
    Args:
        json_str: Raw JSON string
        
    Returns:
        Cleaned JSON string
    """
    json_str = re.sub(r',\s*sideChannel:\s*\{\}', '', json_str)
    
    json_str = re.sub(r'([{,]\s*)([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', r'\1"\2":', json_str)
    
    json_str = re.sub(r'\bfunction\s*\([^)]*\)\s*\{[^}]*\}', 'null', json_str)
    json_str = re.sub(r'\bundefined\b', 'null', json_str)
    
    json_str = re.sub(r":\s*'([^']*)'", r': "\1"', json_str)
    
    json_str = re.sub(r'(\])\s*(\[)', r'\1,\2', json_str)
    json_str = re.sub(r'(\})\s*(\{)', r'\1,\2', json_str)
    
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    
    json_str = re.sub(r',,+', ',', json_str)
    
    json_str = re.sub(r':\s*\$([0-9.]+)', r': "$\1"', json_str)
    
    json_str = re.sub(r'"version"\s*:\s*([0-9.]+)(?=\s*[,}])', r'"version": "\1"', json_str)
    
    return json_str


def alternative_json_clean(json_str: str) -> str:
    """Alternative JSON cleaning method using bracket matching.
    
    Args:
        json_str: Raw JSON string
        
    Returns:
        Cleaned JSON string
    """
    data_start = json_str.find('data:')
    if data_start != -1:
        bracket_start = json_str.find('[', data_start)
        if bracket_start != -1:
            bracket_count = 0
            pos = bracket_start
            
            while pos < len(json_str):
                if json_str[pos] == '[':
                    bracket_count += 1
                elif json_str[pos] == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        data_end = pos + 1
                        break
                pos += 1
            
            if bracket_count == 0:
                data_array = json_str[bracket_start:data_end]
                
                try:
                    parsed_array = json.loads(data_array)
                    
                    return json.dumps({
                        "key": "ds:5",
                        "hash": "13",
                        "data": parsed_array
                    })
                except json.JSONDecodeError:
                    pass
    
    json_str = re.sub(r'\bNaN\b', 'null', json_str)
    return clean_json_string(json_str)

def parse_release_date(release_date_str: Optional[str]) -> Optional[datetime]:
    """Parse release date string to datetime object.
    
    Args:
        release_date_str: Date string in format 'Mon DD, YYYY'
        
    Returns:
        Datetime object or None if parsing fails
    """
    if release_date_str is None:
        return None
    try:
        return datetime.strptime(release_date_str, "%b %d, %Y")
    except (ValueError, TypeError):
        return None


def calculate_app_age(release_date_str: Optional[str], current_date: datetime) -> Optional[int]:
    """Calculate app age in days since release.
    
    Args:
        release_date_str: Release date string
        current_date: Current date for calculation
        
    Returns:
        Number of days since release or None
    """
    release_date = parse_release_date(release_date_str)
    if release_date is None:
        return None
    
    if current_date.tzinfo is not None and release_date.tzinfo is None:
        release_date = release_date.replace(tzinfo=timezone.utc)
    
    days_since_release = (current_date - release_date).days
    return max(0, days_since_release)


def parse_installs_string(installs_str: str) -> Optional[int]:
    """Parse install count string to integer.
    
    Args:
        installs_str: Install count string (e.g., '1,000,000+')
        
    Returns:
        Integer install count or None
    """
    if installs_str is None:
        return None
    
    cleaned_str = installs_str.replace(',', '').replace('+', '')
    try:
        return int(cleaned_str)
    except (ValueError, TypeError):
        return None


def calculate_daily_installs(install_count, release_date_str: Optional[str], current_date: datetime) -> Optional[int]:
    """Calculate average daily installs since release.
    
    Args:
        install_count: Total install count
        release_date_str: Release date string
        current_date: Current date for calculation
        
    Returns:
        Average daily installs or None
    """
    if isinstance(install_count, str):
        install_count = parse_installs_string(install_count)
    
    if install_count is None or release_date_str is None:
        return None
    
    release_date = parse_release_date(release_date_str)
    if release_date is None:
        return None
    
    if current_date.tzinfo is not None and release_date.tzinfo is None:
        release_date = release_date.replace(tzinfo=timezone.utc)
    
    days_since_release = (current_date - release_date).days
    if days_since_release <= 0:
        return 0
    
    return int(install_count / days_since_release)


def calculate_monthly_installs(install_count, release_date_str: Optional[str], current_date: datetime) -> Optional[int]:
    """Calculate average monthly installs since release.
    
    Args:
        install_count: Total install count
        release_date_str: Release date string
        current_date: Current date for calculation
        
    Returns:
        Average monthly installs or None
    """
    if isinstance(install_count, str):
        install_count = parse_installs_string(install_count)
    
    if install_count is None or release_date_str is None:
        return None
    
    release_date = parse_release_date(release_date_str)
    if release_date is None:
        return None
    
    if current_date.tzinfo is not None and release_date.tzinfo is None:
        release_date = release_date.replace(tzinfo=timezone.utc)
    
    days_since_release = (current_date - release_date).days
    if days_since_release <= 0:
        return 0
    
    months_since_release = days_since_release / 30.44
    return int(install_count / months_since_release)
