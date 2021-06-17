def get_prefixes():
    return ["Dev"]


def get_suffixes():
    # Caveat: the order matters for extract_codename()!
    return ["Audience", "Staging", "Dev"]


def extract_codename(title):
    filtered_title = title.strip()

    for s in get_prefixes():
        filtered_title = filtered_title.removeprefix(s).strip()

    for s in get_suffixes():
        filtered_title = filtered_title.removesuffix(s).strip()

    return filtered_title


def summarize(filtered_data, verbose=False):
    devs = dict()

    for e in filtered_data:
        title = e["title"]
        dev = e["dev"]

        codename = extract_codename(title)

        new_set = {codename}
        if dev in devs:
            new_set.update(devs[dev])
        devs[dev] = new_set

    sorted_devs = {
        k: sorted(list(devs[k]))
        for k in sorted(devs, key=lambda x: len(devs[x]), reverse=True)
    }

    if verbose:
        print(sorted_devs)

    return sorted_devs
