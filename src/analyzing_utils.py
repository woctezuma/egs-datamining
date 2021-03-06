from src.item_data_utils import load_item_data
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
    is_dummy = len(image_url) == 0 or not image_url.startswith("http")
    return is_dummy


def get_image_url_suffixe_for_display(metadata):
    image_url = metadata["image"]
    if not is_dummy_image_url(image_url):
        suffixe = f" -> image: {image_url}"
    else:
        suffixe = ""
    return suffixe


def get_key_image_url_suffixe_for_display(item_data):
    try:
        key_images = item_data["keyImages"]
    except (KeyError, TypeError):
        key_images = []

    suffixe = ""
    for image_no, key_image in enumerate(key_images, start=1):
        image_url = key_image["url"]

        image_url = fix_whitespaces_in_url(image_url)

        if not is_dummy_image_url(image_url):
            suffixe += f" -> key_image n°{image_no}: {image_url}"

    return suffixe


def fix_whitespaces_in_url(url):
    return url.replace(" ", "%20")


def is_dummy_save_folder(save_folder):
    is_dummy = save_folder is None or len(save_folder) == 0
    return is_dummy


def get_save_folder_suffixe_for_display(item_data):
    try:
        cloud_save_folder = item_data["customAttributes"]["CloudSaveFolder"]["value"]
    except (TypeError, KeyError) as e:
        cloud_save_folder = None

    if not is_dummy_save_folder(cloud_save_folder):
        suffixe = f" -> CloudSaveFolder: {cloud_save_folder}"
    else:
        suffixe = ""
    return suffixe


def gather_relevant_titles(
    data, sorted_devs, namespaces, request_item_data=False, verbose=False
):
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

                        # NB: "id" is interpreted as an id for "items", no matter if it comes from "items" or "offers".
                        # Therefore, for "offers", download of "item" data will fail, and returned data will be None.
                        if request_item_data:
                            item_id = metadata["id"]
                            item_data = load_item_data(item_id=item_id, verbose=False)
                        else:
                            item_data = None

                        if verbose:
                            slug_suffixe = get_slug_suffixe_for_display(metadata)
                            image_url_suffixe = get_image_url_suffixe_for_display(
                                metadata
                            )
                            save_folder_suffixe = get_save_folder_suffixe_for_display(
                                item_data
                            )
                            key_image_url_suffixe = (
                                get_key_image_url_suffixe_for_display(item_data)
                            )
                            suffixe = (
                                slug_suffixe
                                + image_url_suffixe
                                + save_folder_suffixe
                                + key_image_url_suffixe
                            )
                            print(f"\t\t- {title}{suffixe}")

    return relevant_titles
