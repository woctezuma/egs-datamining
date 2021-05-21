import requests

from src.data_utils import get_data_types, get_data_file_name, save_data


def get_data_tracker_url(data_type):
    url = f"https://raw.githubusercontent.com/srdrabx/{data_type}-tracker/master/database/list.json"

    return url


def download_from_data_tracker(data_type):
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


def main():
    for data_type in get_data_types():
        data = download_from_data_tracker(data_type)

        if data is not None:
            fname = get_data_file_name(data_type)
            save_data(data, fname=fname)

    return True


if __name__ == "__main__":
    main()
