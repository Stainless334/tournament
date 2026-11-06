import unittest
from contextlib import redirect_stdout
from io import StringIO

import fixture as fixture_module
from data import team_list, fixture_list


class TestFixtures(unittest.TestCase):
    def setUp(self):
        team_list.clear()
        fixture_list.clear()
        team_list.extend([
            {"id": "TM001", "team_name": "Alpha"},
            {"id": "TM002", "team_name": "Beta"},
            {"id": "TM003", "team_name": "Gamma"},
            {"id": "TM004", "team_name": "Delta"},
        ])

    def tearDown(self):
        team_list.clear()
        fixture_list.clear()

    def test_generate_fixture_id(self):
        self.assertEqual(fixture_module.generate_fixture_id(), "M001")
        fixture_list.append({"id": "M001"})
        self.assertEqual(fixture_module.generate_fixture_id(), "M002")

    def test_no_teams_returns_false(self):
        team_list.clear()
        self.assertFalse(fixture_module.generate_fixture(team_list))
        self.assertEqual(fixture_list, [])

    def test_four_teams_generate_six_fixtures(self):
        self.assertTrue(fixture_module.generate_fixture(team_list))
        self.assertEqual(len(fixture_list), 6)

    def test_fixture_ids_are_unique_and_sequential(self):
        fixture_module.generate_fixture(team_list)
        ids = [item["id"] for item in fixture_list]
        self.assertEqual(ids, [f"M{i:03d}" for i in range(1, 7)])
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_self_or_duplicate_reverse_matchups(self):
        fixture_module.generate_fixture(team_list)
        matchups = []
        for item in fixture_list:
            self.assertNotEqual(item["home_id"], item["away_id"])
            matchups.append(frozenset((item["home_id"], item["away_id"])))
        self.assertEqual(len(matchups), len(set(matchups)))

    def test_fixtures_start_pending_with_no_scores(self):
        fixture_module.generate_fixture(team_list)
        for item in fixture_list:
            self.assertEqual(item["status"], "pending")
            self.assertIsNone(item["home_score"])
            self.assertIsNone(item["away_score"])

    def test_cannot_generate_fixtures_twice(self):
        fixture_module.generate_fixture(team_list)
        original_count = len(fixture_list)
        output = StringIO()
        with redirect_stdout(output):
            result = fixture_module.generate_fixture(team_list)
        self.assertFalse(result)
        self.assertEqual(len(fixture_list), original_count)
        self.assertIn("already been generated", output.getvalue())

    def test_display_fixture_when_empty(self):
        fixture_list.clear()
        output = StringIO()
        with redirect_stdout(output):
            fixture_module.display_fixture()
        self.assertIn("No Fixture has been created yet.", output.getvalue())

    def test_display_fixture_shows_match_and_team_names(self):
        fixture_module.generate_fixture(team_list)
        output = StringIO()
        with redirect_stdout(output):
            fixture_module.display_fixture()
        self.assertIn("Alpha(home) vs Beta(away)", output.getvalue())
        self.assertIn("Match ID: M001", output.getvalue())


if __name__ == "__main__":
    unittest.main()
