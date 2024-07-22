import csv
from pathlib import Path

from contrib.utils.excel.pandas import XlsxReader

from box import Box

ASSETS_PATH = Path("apps/assets")

home_data = Box.from_yaml(filename=ASSETS_PATH / "home.yml")
catalog_data = Box.from_yaml(filename=ASSETS_PATH / "catalog.yml")
contacts_data = Box.from_yaml(filename=ASSETS_PATH / "contacts.yml")

journal_data = Box.from_yaml(filename=ASSETS_PATH / "journal.yml")
