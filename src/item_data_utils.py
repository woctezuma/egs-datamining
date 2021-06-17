import json
from pathlib import Path

from src.data_utils import save_data
from src.download_utils import download_from_item_data_tracker


def get_item_data_filename(item_id, folder_name="data/items/"):
    Path(folder_name).mkdir(parents=True, exist_ok=True)

    fname = f"{item_id}.json"

    return folder_name + fname


def load_item_data(item_id, verbose=True):
    fname = get_item_data_filename(item_id)

    try:
        with open(fname, encoding="utf8") as f:
            item_data = json.load(f)
    except FileNotFoundError:
        item_data = download_from_item_data_tracker(item_id, verbose=verbose)
        save_data(item_data, fname)

    return item_data
