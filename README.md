# Python Log Parser

## Overview
Simple Python Log Parser to extract and summarize log levels (ERROR, WARNING, CRITICAL, INFO) from one or more log files. Designed as a practical troubleshooting tool for IT Support to quickly identify frequent errors and create a CSV summary.

## Features
- Scans log files for ERROR/WARNING/CRITICAL/INFO
- Counts occurrences by level
- Saves a CSV summary in `./reports/`
- WSL and Linux friendly

## Requirements
- Python 3.8+
- No external libraries required

## How to run
1. Clone the repository:
   ```bash
   git clone https://github.com/abhisheksharma-aks/python-log-parser
   cd python-log-parser
