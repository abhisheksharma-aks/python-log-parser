#!/usr/bin/env python3
"""
parser.py
Simple Python Log Parser for troubleshooting:
- Reads one or more log files
- Extracts ERROR / WARNING / CRITICAL lines
- Counts occurrences of error messages
- Outputs a summary to console and a CSV in ./reports/
Author: Abhishek Sharma (AKS)
"""

import re
import sys
import os
import csv
from collections import Counter
from datetime import datetime

REPORT_DIR = "reports"

LOG_LEVELS = ["ERROR", "WARNING", "CRITICAL", "INFO"]

def parse_file(path):
    counts = Counter()
    matches = []
    level_pattern = re.compile(r"\b(" + "|".join(LOG_LEVELS) + r")\b", re.IGNORECASE)
    try:
        with open(path, "r", errors="ignore") as f:
            for line in f:
                m = level_pattern.search(line)
                if m:
                    level = m.group(1).upper()
                    counts[level] += 1
                    # normalize message: remove timestamp if present
                    msg = re.sub(r'^\[?\d{4}[-/]\d{2}[-/]\d{2}.*?\]?\s*', '', line).strip()
                    matches.append((level, msg))
    except FileNotFoundError:
        print(f"[!] File not found: {path}")
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return counts, matches

def write_report(file_reports):
    os.makedirs(REPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(REPORT_DIR, f"log_summary_{timestamp}.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source_file", "level", "count", "sample_message"])
        for src, data in file_reports.items():
            counts, matches = data
            sample = next((m for l,m in matches if l in ["ERROR","CRITICAL"]), (None, None))[1] if matches else ""
            # write summary for each level
            for level in LOG_LEVELS:
                c = counts.get(level, 0)
                if c > 0:
                    writer.writerow([src, level, c, sample if sample else ""])
    return csv_path

def print_summary(file_reports):
    print("="*40)
    print("Log Parser Summary")
    print("="*40)
    for src, data in file_reports.items():
        counts, matches = data
        print(f"\nFile: {src}")
        for lvl in LOG_LEVELS:
            print(f"  {lvl:8} : {counts.get(lvl,0)}")
    print("\nReports saved to ./reports/")

def main(paths):
    if not paths:
        print("Usage: python3 parser.py <logfile1> [<logfile2> ...]")
        sys.exit(1)
    file_reports = {}
    for p in paths:
        counts, matches = parse_file(p)
        file_reports[p] = (counts, matches)
    csv_path = write_report(file_reports)
    print_summary(file_reports)
    print(f"\nCSV report: {csv_path}")

if __name__ == "__main__":
    main(sys.argv[1:])
