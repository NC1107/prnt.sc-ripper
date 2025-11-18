"""
Configuration file for LightShot Security Research Tool

Modify these settings to customize the behavior of the research tool.
"""

# Default settings for the research tool
DEFAULT_CONFIG = {
    # WebDriver settings
    "HEADLESS_MODE": True,
    "PAGE_LOAD_TIMEOUT": 10,
    "IMPLICIT_WAIT": 5,
    
    # Request settings
    "DEFAULT_DELAY": 1.0,
    "MAX_ATTEMPTS": 1000,
    "TIMEOUT_SECONDS": 5,
    
    # Output settings
    "OUTPUT_DIR": "images",
    "LOG_FILE": "lightshot_research.log",
    "LOG_LEVEL": "INFO",
    
    # Browser options
    "WINDOW_SIZE": "1920,1080",
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # Research parameters
    "URL_PATTERN": {
        "BASE_URL": "https://prnt.sc/",
        "LETTERS": "abcdefghijklmnopqrstuvwxyz",
        "DIGITS": "0123456789",
    },
    
    # CSS selectors for different LightShot page layouts
    "SELECTORS": [
        ".screenshot-image",
        "#screenshot-image",
        ".image",
        "img[src*='image']",
    ],
    
    # Rate limiting and ethical guidelines
    "ETHICAL_GUIDELINES": {
        "RESPECT_RATE_LIMITS": True,
        "MINIMUM_DELAY": 0.5,
        "MAX_REQUESTS_PER_MINUTE": 30,
        "ENABLE_LOGGING": True,
    },
}

# Environment-specific overrides
DEVELOPMENT_CONFIG = {
    "LOG_LEVEL": "DEBUG",
    "HEADLESS_MODE": False,
    "DEFAULT_DELAY": 2.0,
    "MAX_ATTEMPTS": 100,
}

PRODUCTION_CONFIG = {
    "LOG_LEVEL": "INFO",
    "HEADLESS_MODE": True,
    "DEFAULT_DELAY": 1.5,
    "MAX_ATTEMPTS": 10000,
}
