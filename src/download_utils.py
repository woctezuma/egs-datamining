import requests


def get_data_tracker_url(data_type):
    url = f"https://raw.githubusercontent.com/srdrabx/{data_type}-tracker/master/database/list.json"

    return url


def download_from_data_tracker(data_type="items", url=None):
    if url is None:
        url = get_data_tracker_url(data_type)
    response = requests.get(url=url)

    if response.ok:
        data = response.json()
    else:
        print(
            f"Data could not be downloaded from {url}. Status code {response.status_code} was returned."
        )
        data = None

    return data
