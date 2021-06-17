import requests


def get_data_tracker_url(data_type):
    url = f"https://raw.githubusercontent.com/srdrabx/{data_type}-tracker/master/database/list.json"

    return url


def get_item_data_tracker_url(item_id):
    url = f"https://raw.githubusercontent.com/srdrabx/items-tracker/master/database/items/{item_id}.json"

    return url


def download_from_data_tracker(data_type="items", url=None, verbose=True):
    if url is None:
        url = get_data_tracker_url(data_type)
    response = requests.get(url=url)

    if response.ok:
        data = response.json()
    else:
        if verbose:
            print(
                f"Data could not be downloaded from {url}. Status code {response.status_code} was returned."
            )
        data = None

    return data


def download_from_item_data_tracker(item_id, verbose=True):
    url = get_item_data_tracker_url(item_id)
    item_data = download_from_data_tracker(url=url, verbose=verbose)

    return item_data
