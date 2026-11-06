import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import record_result as result_module
from data import fixture_list


class TestRecordResult(unittest.TestCase):
    def setUp(self):
        fixture_list.clear()
        fixture_list.append({
            "id": "M001",
            "home_id": "TM001",
            "away_id": "TM002",
            "status": "pending",
            "home_score": None,
            "away_score": None,
        })

    def tearDown(self):
        fixture_list.clear()

    def test_no_fixtures_returns_false(self):
        fixture_list.clear()
        self.assertFalse(result_module.record_result())

    @patch("builtins.input", return_value="0")
    @patch("record_result.time.sleep")
    def test_zero_returns_false_when_nothing_recorded(self, mocked_sleep, mocked_input):
        self.assertFalse(result_module.record_result())

    @patch("builtins.input", side_effect=["M001", "2", "1", "no"])
    @patch("record_result.time.sleep")
    def test_records_result_and_returns_true(self, mocked_sleep, mocked_input):
        self.assertTrue(result_module.record_result())
        self.assertEqual(fixture_list[0]["status"], "played")
        self.assertEqual(fixture_list[0]["home_score"], 2)
        self.assertEqual(fixture_list[0]["away_score"], 1)

    @patch("builtins.input", side_effect=["M001", "2", "1", "yes", "0"])
    @patch("record_result.time.sleep")
    def test_returning_after_recording_keeps_success_flag(self, mocked_sleep, mocked_input):
        self.assertTrue(result_module.record_result())
        self.assertEqual(fixture_list[0]["status"], "played")

    @patch("builtins.input", side_effect=["M001", "-1", "2", "1", "no"])
    @patch("record_result.time.sleep")
    def test_negative_score_is_rejected(self, mocked_sleep, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            self.assertTrue(result_module.record_result())
        self.assertIn("Score cannot be negative.", output.getvalue())
        self.assertEqual(fixture_list[0]["home_score"], 2)

    @patch("builtins.input", side_effect=["M001", "abc", "2", "1", "no"])
    @patch("record_result.time.sleep")
    def test_non_integer_score_is_rejected(self, mocked_sleep, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            self.assertTrue(result_module.record_result())
        self.assertIn("Enter a valid integer.", output.getvalue())

    @patch("builtins.input", side_effect=["M001", "0"])
    @patch("record_result.time.sleep")
    def test_already_played_fixture_is_not_recorded_again(self, mocked_sleep, mocked_input):
        fixture_list[0].update(status="played", home_score=1, away_score=0)
        output = StringIO()
        with redirect_stdout(output):
            result_module.record_result()
        self.assertIn("already been played", output.getvalue())
        self.assertEqual(fixture_list[0]["home_score"], 1)


if __name__ == "__main__":
    unittest.main()
