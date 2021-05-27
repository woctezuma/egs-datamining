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


def is_dummy_slug(slug):
    is_dummy = len(slug) == 0 or slug == "[]"
    return is_dummy


def get_slug_suffixe_for_display(metadata):
    slug = metadata["slug"]
    if not is_dummy_slug(slug):
        suffixe = f" (slug: {slug})"
    else:
        suffixe = ""
    return suffixe


def is_dummy_image_url(image_url):
    is_dummy = len(image_url) == 0
    return is_dummy


def get_image_url_suffixe_for_display(metadata):
    image_url = metadata["image"]
    if not is_dummy_image_url(image_url):
        suffixe = f" -> image: {image_url}"
    else:
        suffixe = ""
    return suffixe


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
                            slug_suffixe = get_slug_suffixe_for_display(metadata)
                            image_url_suffixe = get_image_url_suffixe_for_display(
                                metadata
                            )
                            suffixe = slug_suffixe + image_url_suffixe
                            print(f"\t\t- {title}{suffixe}")

    return relevant_titles
