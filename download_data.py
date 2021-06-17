from src.data_utils import get_data_types, get_data_file_name, save_data
from src.download_utils import download_from_data_tracker


def main():
    for data_type in get_data_types():
        data = download_from_data_tracker(data_type)

        if data is not None:
            fname = get_data_file_name(data_type)
            save_data(data, fname=fname)

    return True


if __name__ == "__main__":
    main()
