from src.metadata_utils import parse_metadata
from src.summarizing_utils import get_suffixes


def fill_in_namespaces(data, sorted_devs, verbose=False):
    namespaces = dict()

    for dev in sorted_devs:
        print(f"Dev: {dev}")
        for codename in sorted_devs[dev]:
            print(f"- {codename}")

            current_namespaces = set()

            for data_element in data:
                metadata = parse_metadata(data_element)

                if codename in metadata["title"]:
                    if any(s in metadata["title"] for s in get_suffixes()):
                        current_namespaces.add(metadata["namespace"])

            namespaces[codename] = list(current_namespaces)

    if verbose:
        print(namespaces)

    return namespaces


def gather_relevant_titles(data, sorted_devs, namespaces, verbose=False):
    relevant_titles = dict()

    for dev in sorted_devs:
        print(f"\nDev: {dev}")
        for codename in sorted_devs[dev]:
            print(f"- codename: {codename}")

            relevant_titles[codename] = list()

            for namespace in namespaces[codename]:
                print(f"\t- namespace: {namespace}")

                for data_element in data:
                    metadata = parse_metadata(data_element)

                    if namespace == metadata["namespace"]:
                        title = metadata["title"]
                        relevant_titles[codename].append(title)

                        if verbose:
                            print(f"\t\t- {title}")

    return relevant_titles
