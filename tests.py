from unittest import TestCase

import download_data
import filter_codenames
import src.analyzing_utils
import src.data_utils
import src.filtering_utils
import src.metadata_utils as meta
import src.summarizing_utils


class TestDataUtilsMethods(TestCase):
    def test_get_data_types(self):
        data_types = src.data_utils.get_data_types()
        self.assertEqual(len(data_types), 2)
        self.assertIn("items", data_types)
        self.assertIn("offers", data_types)

    def test_get_data_file_name(self):
        data_types = src.data_utils.get_data_types()
        for data_type in data_types:
            fname = src.data_utils.get_data_file_name(data_type)
            expected_fname = f"data/{data_type}_list.json"
            self.assertEqual(fname, expected_fname)

    def test_load_data(self):
        data = src.data_utils.load_data()
        self.assertGreater(len(data), 0)

    def test_save_data(self):
        dummy_output = {"test": 123}
        dummy_fname = "temp.json"
        flag = src.data_utils.save_data(dummy_output, dummy_fname)
        self.assertTrue(flag)


class TestMetaDataUtilsMethods(TestCase):
    def test_parse_metadata_from_items(self):
        data_element = [
            "12160a20dbb645d7a3672959b5d7ed03",
            "phlox",
            "Griftlands",
            ["games", "applications"],
            "Klei Entertainment",
            1551704831,
            1618503565,
        ]
        metadata = meta.parse_metadata(data_element)
        self.assertEqual(len(metadata), 9)

    def test_parse_metadata_from_offers(self):
        data_element = [
            "3299949f391a4dbb9e0c4b28b683992c",
            "phlox",
            "Griftlands",
            ["games", "games/edition/base", "games/edition", "applications"],
            "Klei Entertainment",
            1551705084,
            1618503526,
            "https://cdn1.epicgames.com/phlox/offer/EGS_Griftlands_KleiEntertainment_S2-860x1148-5fc47bd45ab3e9271046563fa33b5081.jpg",
            "griftlands/home",
        ]
        metadata = meta.parse_metadata(data_element)
        self.assertEqual(len(metadata), 9)

    def test_is_of_interest(self):
        metadata = {
            "title": "PythonAudience",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertTrue(meta.is_of_interest(metadata))

        metadata = {
            "title": "PythonStaging",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertTrue(meta.is_of_interest(metadata))

        metadata = {
            "title": "PythonGeneralAudience",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(meta.is_of_interest(metadata))

        metadata = {
            "title": "PythonGeneralAudienceStaging",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(meta.is_of_interest(metadata))

        metadata = {
            "title": "Python",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(meta.is_of_interest(metadata))

        metadata = {
            "title": "PythonAudience",
            "author": "Tim Sweeney",
            "category": ["games", "addons"],
        }
        self.assertFalse(meta.is_of_interest(metadata))

        metadata = {
            "title": "PythonAudience",
            "author": "",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(meta.is_of_interest(metadata))

    def test_has_store_page(self):
        metadata = {"image": "123", "slug": "456"}
        self.assertTrue(meta.has_store_page(metadata))

        metadata = {"image": "123", "slug": ""}
        self.assertFalse(meta.has_store_page(metadata))

        metadata = {"image": "", "slug": "456"}
        self.assertFalse(meta.has_store_page(metadata))

        metadata = {"image": "", "slug": ""}
        self.assertFalse(meta.has_store_page(metadata))


class TestFilteringUtilsMethods(TestCase):
    def test_get_namespaces_with_known_store_pages(self):
        data = src.data_utils.load_data()
        known_namespaces = src.filtering_utils.get_namespaces_with_known_store_pages(
            data
        )
        self.assertGreater(len(known_namespaces), 0)

    def test_filter_data(self):
        data = src.data_utils.load_data()
        known_namespaces = src.filtering_utils.get_namespaces_with_known_store_pages(
            data
        )
        filtered_data = src.filtering_utils.filter_data(
            data, known_namespaces, verbose=True
        )
        self.assertGreater(len(filtered_data), 0)


class TestSummarizingUtilsMethods(TestCase):
    def test_get_prefixes(self):
        prefixes = src.summarizing_utils.get_prefixes()
        self.assertEqual(len(prefixes), 1)
        self.assertIn("Dev", prefixes)

    def test_get_suffixes(self):
        suffixes = src.summarizing_utils.get_suffixes()
        self.assertEqual(len(suffixes), 3)
        self.assertEqual(["Audience", "Staging", "Dev"], suffixes)  # the order matters!

    def test_extract_codename(self):
        codename = "Python"
        for prefixe in ["", "Dev"]:
            for suffixe in [
                "",
                "Audience",
                "Staging",
                "StagingAudience",
                "Dev",
                "DevAudience",
                "DevStaging",
                "DevStagingAudience",
            ]:
                self.assertEqual(
                    src.summarizing_utils.extract_codename(
                        f"{prefixe}{codename}{suffixe}"
                    ),
                    codename,
                )

    def test_summarize(self):
        data = src.data_utils.load_data()
        known_namespaces = src.filtering_utils.get_namespaces_with_known_store_pages(
            data
        )
        filtered_data = src.filtering_utils.filter_data(
            data, known_namespaces, verbose=False
        )
        sorted_devs = src.summarizing_utils.summarize(filtered_data, verbose=True)
        self.assertGreater(len(sorted_devs), 0)


class TestAnalyzingUtilsMethods(TestCase):
    def test_fill_in_namespaces(self):
        data = src.data_utils.load_data()
        known_namespaces = src.filtering_utils.get_namespaces_with_known_store_pages(
            data
        )
        filtered_data = src.filtering_utils.filter_data(data, known_namespaces)
        sorted_devs = src.summarizing_utils.summarize(filtered_data)
        namespaces = src.analyzing_utils.fill_in_namespaces(
            data, sorted_devs, verbose=True
        )
        self.assertGreater(len(namespaces), 0)

    def test_gather_relevant_titles(self):
        data = src.data_utils.load_data()
        known_namespaces = src.filtering_utils.get_namespaces_with_known_store_pages(
            data
        )
        filtered_data = src.filtering_utils.filter_data(data, known_namespaces)
        sorted_devs = src.summarizing_utils.summarize(filtered_data)
        namespaces = src.analyzing_utils.fill_in_namespaces(data, sorted_devs)
        relevant_titles = src.analyzing_utils.gather_relevant_titles(
            data, sorted_devs, namespaces, verbose=True
        )
        self.assertGreater(len(relevant_titles), 0)


class TestDownloadDataMethods(TestCase):
    def test_get_data_tracker_url(self):
        url = download_data.get_data_tracker_url(data_type="dummy")
        self.assertTrue(url.startswith("https://raw.githubusercontent.com/srdrabx/"))
        self.assertTrue(url.endswith("-tracker/master/database/list.json"))

    def test_download_from_data_tracker(self):
        data = download_data.download_from_data_tracker(data_type="dummy")
        self.assertTrue(data is None)

    def test_main(self):
        flag = download_data.main()
        self.assertTrue(flag)


class TestFilterCodenamesMethods(TestCase):
    def test_main(self):
        flag = filter_codenames.main()
        self.assertTrue(flag)
