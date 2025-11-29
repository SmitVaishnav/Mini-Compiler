#!/usr/bin/env python3
# run.py
"""Simple runner script for MiniLang interpreter."""

import sys
import os

# Add parent directory to path so we can import mini_lang
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_lang.main import main

if __name__ == '__main__':
    main()

