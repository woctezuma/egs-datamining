import operator

from .metadata_utils import parse_metadata, has_store_page, is_of_interest


def get_namespaces_with_known_store_pages(data):
    known_namespaces = set()

    for data_element in data:
        metadata = parse_metadata(data_element)
        if has_store_page(metadata):
            known_namespaces.add(metadata["namespace"])

    return known_namespaces


def filter_data(data, known_namespaces, verbose=False):
    filtered_data = list()

    for data_element in data:
        metadata = parse_metadata(data_element)
        if is_of_interest(metadata) and (metadata["namespace"] not in known_namespaces):
            small_dict = {
                "title": metadata["title"],
                "namespace": metadata["namespace"],
                "dev": metadata["author"],
            }
            filtered_data.append(small_dict)

    # Reference: https://stackoverflow.com/a/29849371/376454
    filtered_data.sort(key=operator.itemgetter("dev", "title"))

    if verbose:
        print(filtered_data)

    return filtered_data
