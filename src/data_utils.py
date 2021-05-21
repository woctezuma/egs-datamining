import json


def get_data_types():
    return ["items", "offers"]


def get_data_file_name(data_type, base_fname="list.json", folder_name="data/"):
    fname = data_type + "_" + base_fname

    return folder_name + fname


def load_data():
    # These two JSON files were manually downloaded and renamed beforehand:
    # - https://github.com/srdrabx/items-tracker/blob/master/database/list.json -> data/items_list.json (1.04 MB)
    # - https://github.com/srdrabx/offers-tracker/blob/master/database/list.json -> data/offers_list.json (1.43 MB)

    data = list()

    for data_type in get_data_types():
        with open(get_data_file_name(data_type), encoding="utf8") as f:
            new_data = json.load(f)

        data += new_data

    return data


def save_data(data, fname):
    with open(fname, "w", encoding="utf8") as f:
        json.dump(data, f)

    return True
