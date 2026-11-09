import json
import os
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import storage
from data import team_list, fixture_list


class TestStorage(unittest.TestCase):
    def setUp(self):
        team_list.clear()
        fixture_list.clear()
        self.teams = [
            {"id": "TM001", "team_name": "Alpha"},
            {"id": "TM002", "team_name": "Beta"},
        ]
        self.fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "played", "home_score": 2, "away_score": 1
        }]
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = os.path.join(self.temp_dir.name, "league_data.json")
        self.store_patch = patch.object(storage, "STORE", self.store_path)
        self.store_patch.start()

    def tearDown(self):
        self.store_patch.stop()
        self.temp_dir.cleanup()
        team_list.clear()
        fixture_list.clear()

    def write_json(self, data):
        with open(self.store_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def valid_data(self):
        return {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": self.fixtures,
        }

    def test_save_data_writes_expected_structure(self):
        storage.save_data(self.teams, self.fixtures)
        with open(self.store_path, encoding="utf-8") as file:
            saved = json.load(file)
        self.assertEqual(saved, self.valid_data())

    def test_load_valid_data_updates_shared_lists(self):
        self.write_json(self.valid_data())
        self.assertTrue(storage.load_data())
        self.assertEqual(team_list, self.teams)
        self.assertEqual(fixture_list, self.fixtures)

    def test_missing_file_returns_false(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertFalse(storage.load_data())
        self.assertIn("file not found", output.getvalue().lower())

    def test_invalid_json_returns_false(self):
        with open(self.store_path, "w", encoding="utf-8") as file:
            file.write('{"schema_version": 1,')
        output = StringIO()
        with redirect_stdout(output):
            self.assertFalse(storage.load_data())
        self.assertIn("Invalid json syntax", output.getvalue())

    def test_non_dictionary_top_level_is_rejected(self):
        with open(self.store_path, "w", encoding="utf-8") as file:
            file.write("[]")
        self.assertFalse(storage.load_data())

    def test_missing_required_top_level_key_is_rejected(self):
        data = self.valid_data()
        del data["fixtures"]
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_unsupported_schema_version_is_rejected(self):
        data = self.valid_data()
        data["schema_version"] = 2
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_boolean_schema_version_is_rejected(self):
        data = self.valid_data()
        data["schema_version"] = True
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_teams_must_be_a_list(self):
        data = self.valid_data()
        data["teams"] = "not a list"
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_duplicate_team_id_is_rejected(self):
        data = self.valid_data()
        data["teams"].append({"id": "TM001", "team_name": "Another"})
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_invalid_fixture_team_reference_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["away_id"] = "TM999"
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_self_match_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["away_id"] = "TM001"
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_duplicate_matchup_is_rejected_even_if_reversed(self):
        data = self.valid_data()
        data["fixtures"].append({
            "id": "M002", "home_id": "TM002", "away_id": "TM001",
            "status": "pending", "home_score": None, "away_score": None
        })
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_pending_fixture_must_have_none_scores(self):
        data = self.valid_data()
        data["fixtures"][0].update(
            status="pending", home_score=0, away_score=None
        )
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_played_fixture_rejects_boolean_score(self):
        data = self.valid_data()
        data["fixtures"][0]["home_score"] = True
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_played_fixture_rejects_negative_score(self):
        data = self.valid_data()
        data["fixtures"][0]["away_score"] = -1
        self.write_json(data)
        self.assertFalse(storage.load_data())

    def test_failed_load_does_not_mutate_existing_lists(self):
        team_list[:] = [{"id": "TM009", "team_name": "Existing"}]
        fixture_list[:] = []
        original_teams = team_list.copy()
        original_fixtures = fixture_list.copy()
        with open(self.store_path, "w", encoding="utf-8") as file:
            file.write("{broken json")
        self.assertFalse(storage.load_data())
        self.assertEqual(team_list, original_teams)
        self.assertEqual(fixture_list, original_fixtures)


if __name__ == "__main__":
    unittest.main()
