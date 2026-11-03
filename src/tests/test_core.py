import os
import tempfile
import unittest
from app import create_app

class Week2CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.temp.name, "test.db")
        self.app = create_app({"TESTING": True, "DATABASE": self.db,
                               "TRAINING_DATA": os.path.join(os.path.dirname(__file__), "..", "sample_training_data.csv")})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_home_page(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_submit_request_and_predict_category(self):
        response = self.client.post("/requests/new", data={
            "description": "The kitchen sink pipe is leaking", "category": ""
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Service request submitted", response.data)
        self.assertIn(b"Plumbing", response.data)

    def test_selected_category_is_saved_as_final_category(self):
        response = self.client.post("/requests/new", data={
            "description": "The kitchen sink pipe is leaking", "category": "Electrical"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Final category:</b> Electrical", response.data)

    def test_short_description_is_rejected(self):
        response = self.client.post("/requests/new", data={"description": "leak", "category": ""})
        self.assertEqual(response.status_code, 400)

    def test_saved_request_appears_in_list(self):
        self.client.post("/requests/new", data={"description": "Refrigerator is not cooling", "category": ""})
        response = self.client.get("/requests")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Refrigerator", response.data)

if __name__ == "__main__":
    unittest.main()
