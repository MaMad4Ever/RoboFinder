# RoboFinder

RoboFinder is a lightweight Python script that fetches a target's `robots.txt` file and extracts all Disallowed URLs. It's useful for security researchers, bug bounty hunters, and web developers to quickly identify restricted paths.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/RoboFinder.git
cd RoboFinder
```
Note: This script uses only Python standard libraries, so requirements.txt is empty. You don't need to install anything.
Usage

## Basic usage:
```bash
python3 robofinder.py -d example.com
```
Save results to a file and run silently:
```bash
python3 robofinder.py -d example.com -s -o results.txt
```
Show help:
```bash
python3 robofinder.py -h
```
Options
```text

  -h, --help                show this help message and exit
  -d DOMAIN, --domain       Enter the target domain (e.g., example.com or https://example.com)
  -s, --silent              Run silently (no console output except errors)
  -o OUTPUT, --output       Save Disallow URLs to a file
```
Example Output
```text

[*] Fetch Robots txt http://example.com ...
[*] Disallow Path ...
[*] Build Full URLs ...

--- Disallow URLs ---
http://example.com/private/
http://example.com/admin
```
## How It Works

- The script constructs the robots.txt URL from the given domain (adds http:// if no protocol specified).
- Downloads the robots.txt file.
- Parses lines starting with Disallow: and extracts the paths.
- Converts each path to a full URL using the domain.
- Prints or saves the resulting URLs.
