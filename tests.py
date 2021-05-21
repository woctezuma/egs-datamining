from unittest import TestCase

import download_data
import filter_codenames
import src.data_utils
import src.filtering_utils
import src.metadata_utils
import src.summarizing_utils


class TestDataUtilsMethods(TestCase):
    def test_get_data_types(self):
        data_types = src.data_utils.get_data_types()
        self.assertEqual(len(data_types), 2)
        self.assertIn("items", data_types)
        self.assertIn("offers", data_types)

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
        metadata = src.metadata_utils.parse_metadata(data_element)
        self.assertEqual(len(metadata), 6)

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
        metadata = src.metadata_utils.parse_metadata(data_element)
        self.assertEqual(len(metadata), 6)

    def test_is_of_interest(self):
        metadata = {
            "title": "PythonAudience",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertTrue(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "PythonStaging",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertTrue(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "PythonGeneralAudience",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "PythonGeneralStaging",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "Python",
            "author": "Tim Sweeney",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "PythonAudience",
            "author": "Tim Sweeney",
            "category": ["games", "addons"],
        }
        self.assertFalse(src.metadata_utils.is_of_interest(metadata))

        metadata = {
            "title": "PythonAudience",
            "author": "",
            "category": ["games", "NOTaddons"],
        }
        self.assertFalse(src.metadata_utils.is_of_interest(metadata))

    def test_has_store_page(self):
        metadata = {"image": "123", "slug": "456"}
        self.assertTrue(src.metadata_utils.has_store_page(metadata))

        metadata = {"image": "123", "slug": ""}
        self.assertFalse(src.metadata_utils.has_store_page(metadata))

        metadata = {"image": "", "slug": "456"}
        self.assertFalse(src.metadata_utils.has_store_page(metadata))

        metadata = {"image": "", "slug": ""}
        self.assertFalse(src.metadata_utils.has_store_page(metadata))


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
        self.assertEqual(src.summarizing_utils.extract_codename("DevPython"), "Python")
        self.assertEqual(src.summarizing_utils.extract_codename("PythonDev"), "Python")
        self.assertEqual(
            src.summarizing_utils.extract_codename("PythonDevStaging"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("PythonDevStagingAudience"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("PythonStaging"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("PythonStagingAudience"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("PythonAudience"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("DevPythonDevStagingAudience"),
            "Python",
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("DevPythonStagingAudience"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("DevPythonStaging"), "Python"
        )
        self.assertEqual(
            src.summarizing_utils.extract_codename("DevPythonAudience"), "Python"
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
