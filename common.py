import os

# Base directory for pyfeed configuration and data
BASE_DIR = os.path.expanduser("~/.pyfeed")
FEEDS_DIR = os.path.join(BASE_DIR, "feeds")
CONFIG_FILE = os.path.join(BASE_DIR, "pyfeedrc")

def ensure_dirs():
    if not os.path.exists(FEEDS_DIR):
        os.makedirs(FEEDS_DIR)
