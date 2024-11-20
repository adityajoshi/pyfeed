import feedparser
import requests
import os
import csv
from datetime import datetime
from io import BytesIO

RSS_FEEDS = {}


def update():
    """

    :rtype: list
    """
    articles = []
    for source, feed in RSS_FEEDS.items():
        cur_timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        try:
            resp = requests.get(feed, timeout=20.0)
        except requests.ReadTimeout:
            print(f'Timeout when reading RSS {feed}'.ljust(50, " "), "OK")
            continue
        except requests.exceptions.ConnectionError:
            print(f"Error loading {feed}")
            continue

        content = BytesIO(resp.content)
        parsed_feed = feedparser.parse(content)
        new_entries = [
            ("False", entry.get('published', cur_timestamp), entry.get('author', 'unknown'), entry.title, entry.link)
            for entry in parsed_feed.entries]
        source = source.replace(" ","_")
        source = source.replace("-","_")
        csv_file = source + '_records'

        # Load existing records from the CSV
        existing_records = load_existing_records(csv_file)

        # Filter out entries that are already present in the CSV (based on the unique 'link' field)
        unique_entries = [entry for entry in new_entries if entry[3] not in existing_records]

        # Write only unique entries to the CSV file
        if unique_entries:
            write_records_to_csv(unique_entries, csv_file)

        print(f"{source}        OK".rjust(10," "))


def load_existing_records(csv_file):
    """
    Load existing records from the CSV file and return a set of unique links.
    :rtype: set
    """
    feeds_path = os.path.expanduser("~/.pyfeed/feeds/")
    if not os.path.exists(feeds_path):
        raise FileNotFoundError(f"The feeds folder {feeds_path} does not exist.")
    if not os.path.exists(feeds_path + csv_file):
        return set()  # Return empty set if file doesn't exist yet

    existing_links = set()

    with open(feeds_path + csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            if row:  # Ensure row is not empty
                existing_links.add(row[3])  # The link is at index 3 in the tuple
    return existing_links


def write_records_to_csv(records, csv_file):
    feeds_path = os.path.expanduser("~/.pyfeed/feeds/")
    if not os.path.exists(feeds_path):
        raise FileNotFoundError(f"The feeds folder {feeds_path} does not exist.")

    with open(feeds_path + csv_file, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=",")
        # csv_writer.writerow(['id', 'win'])  # Write header

        for record in records:
            csv_writer.writerow(record)

def load_pyfeedrc():
    """Load the configurations from the pyfeedrc file located in $HOME/.pyfeed."""
    pyfeedrc_path = os.path.expanduser("~/.pyfeed/pyfeedrc")
    if not os.path.exists(pyfeedrc_path):
        raise FileNotFoundError(f"The configuration file {pyfeedrc_path} does not exist.")

    config = {}
    with open(pyfeedrc_path, "r") as f:
        # Use exec to execute the Python file in the context of the `config` dictionary.
        exec(f.read(), config)

    # Remove any non-config keys (like __builtins__) from the resulting dictionary.
    config = {k: v for k, v in config.items() if not k.startswith('__')}
    return config

def read_feeds(rss_config):
    global RSS_FEEDS
    RSS_FEEDS.update(rss_config.get("FEEDS",{}))

if __name__ == "__main__":
    try:
        config = load_pyfeedrc()
        read_feeds(config)
        update()
    except Exception as e:
        print(f"Error loading pyfeedrc: {e}")
