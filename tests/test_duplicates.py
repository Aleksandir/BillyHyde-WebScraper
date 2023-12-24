import json
import unittest

from src.data_scraper import duplicate_check


class TestDuplicateCheck(unittest.TestCase):
    def test_no_duplicates(self):
        # Create a JSON file with no duplicate products
        data = ["product1", "product2", "product3"]
        with open("test_data.json", "w") as f:
            json.dump(data, f)

        # Call the duplicate_check function
        duplicate_check("test_data.json")

        # Assert that no duplicate products are found
        self.assertEqual("No duplicate products found.", captured_output())

    def test_duplicates(self):
        # Create a JSON file with duplicate products
        data = ["product1", "product2", "product1"]
        with open("test_data.json", "w") as f:
            json.dump(data, f)

        # Call the duplicate_check function
        duplicate_check("test_data.json")

        # Assert that duplicate products are found
        self.assertEqual("Duplicate products found: {'product1'}", captured_output())

    def captured_output():
        # Capture the printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        return captured_output.getvalue().strip()


if __name__ == "__main__":
    unittest.main()
