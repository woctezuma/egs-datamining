from src.analyzing_utils import fill_in_namespaces, gather_relevant_titles
from src.data_utils import load_data, save_data
from src.filtering_utils import get_namespaces_with_known_store_pages, filter_data
from src.summarizing_utils import summarize


def main():
    data = load_data()
    known_namespaces = get_namespaces_with_known_store_pages(data)
    filtered_data = filter_data(data, known_namespaces, verbose=False)
    sorted_devs = summarize(filtered_data, verbose=True)
    save_data(sorted_devs, fname="data/output.json")

    namespaces = fill_in_namespaces(data, sorted_devs, verbose=True)
    save_data(namespaces, "data/namespaces.json")

    relevant_titles = gather_relevant_titles(
        data, sorted_devs, namespaces, verbose=True
    )
    save_data(relevant_titles, "data/relevant_titles.json")

    return True


if __name__ == "__main__":
    main()
