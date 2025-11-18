# LightShot Security Research Tool

A security research tool that demonstrates vulnerabilities in LightShot's URL structure by exploring predictable URL patterns.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red)](LICENSE)

## Overview

This tool systematically accesses LightShot screenshots through predictable URL patterns to demonstrate security vulnerabilities in URL structure design. LightShot uses a simple pattern (`[a-z][a-z][0-9][0-9][0-9][0-9]`) that makes URLs guessable, highlighting the importance of cryptographically secure URL generation.

## Disclaimer

**For educational and security research purposes only.** Do not use this tool for unauthorized access or malicious purposes. Always respect rate limits and terms of service.

## Requirements

- Python 3.8 or higher
- Google Chrome browser

## Installation

```bash
git clone https://github.com/NC1107/prnt.sc-ripper.git
cd prnt.sc-ripper
pip install -r requirements.txt
```

ChromeDriver will be automatically downloaded and managed by `webdriver-manager` on first run.

## Usage

Basic usage:

```bash
python main.py
```

With options:

```bash
python main.py --max-attempts 500 --delay 2.0 --visible
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Directory to save screenshots | `images` |
| `--max-attempts` | Maximum number of URLs to attempt | `1000` |
| `--delay` | Delay between requests (seconds) | `1.0` |
| `--visible` | Run browser in visible mode | `False` |

## Project Structure

```
prnt.sc-ripper/
├── main.py              # Main application
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── setup.py            # Setup and validation script
├── README.md           # Documentation
├── LICENSE             # License information
└── images/             # Screenshot output directory
```

## Features

- Object-oriented design with comprehensive error handling
- Configurable rate limiting and delays
- Detailed logging to file and console
- Command-line interface for flexible usage
- Cross-platform support (Windows, macOS, Linux)

## Security Concepts Demonstrated

1. **Predictable URL patterns** and enumeration vulnerabilities
2. **Information disclosure** through publicly accessible content
3. Importance of **rate limiting** and access controls
4. Need for **cryptographically secure** URL generation

## Logging

Detailed logs are saved to `lightshot_research.log` including:
- Successful captures
- Failed attempts
- Progress updates
- Error messages

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your improvements.

## License

Educational Use Only. See [LICENSE](LICENSE) for details.

## Responsible Disclosure

If you discover security vulnerabilities while using this tool, report them responsibly to the affected service and allow time for remediation before public disclosure.

## Contact

- GitHub: [@NC1107](https://github.com/NC1107)
- LinkedIn: [Nicholas Conn](https://www.linkedin.com/in/nicholas-conn-41b1b120a/)
- Email: 188623nc@gmail.com