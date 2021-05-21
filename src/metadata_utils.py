def parse_metadata(data_element):
    try:
        image_url = data_element[7]
    except IndexError:
        image_url = ""

    try:
        slug = data_element[8]
    except IndexError:
        slug = ""

    metadata = {
        "namespace": data_element[1].strip(),
        "title": data_element[2].strip(),
        "category": data_element[3],  # this is a list
        "author": data_element[4].strip(),
        "image": image_url.strip(),
        "slug": slug.strip(),
    }

    return metadata


def is_of_interest(metadata):
    has_codename_for_title = any(
        metadata["title"].endswith(s) for s in ["Audience", "Staging"]
    )
    has_known_author = len(metadata["author"]) > 0
    is_base_game = (
        "games" in metadata["category"] and "addons" not in metadata["category"]
    )

    # When an entry contains 'General', a similar entry without it exists, so we prefer omitting it to avoid duplicates.
    is_dummy_duplicate = "General" in metadata["title"]

    result = (
        has_codename_for_title
        and has_known_author
        and is_base_game
        and (not is_dummy_duplicate)
    )

    return result


def has_store_page(metadata):
    has_known_image = len(metadata["image"]) > 0
    has_known_slug = len(metadata["slug"]) > 0

    result = bool(has_known_image and has_known_slug)

    return result
