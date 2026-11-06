import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import team_reg
from data import team_list, fixture_list


class TestTeamRegistration(unittest.TestCase):
    def setUp(self):
        team_list.clear()
        fixture_list.clear()

    def tearDown(self):
        team_list.clear()
        fixture_list.clear()

    def test_generate_first_team_id(self):
        self.assertEqual(team_reg.generate_team_id(), "TM001")

    def test_generate_next_team_id(self):
        team_list.extend([
            {"id": "TM001", "team_name": "Alpha"},
            {"id": "TM002", "team_name": "Beta"},
        ])
        self.assertEqual(team_reg.generate_team_id(), "TM003")

    @patch("builtins.input", side_effect=["0"])
    def test_registration_can_be_cancelled(self, mocked_input):
        self.assertFalse(team_reg.register_teams())
        self.assertEqual(team_list, [])

    @patch("builtins.input", side_effect=["3", "0"])
    def test_team_count_below_minimum_is_rejected(self, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            result = team_reg.register_teams()
        self.assertFalse(result)
        self.assertEqual(team_list, [])
        self.assertIn("Number out of range!", output.getvalue())

    @patch("builtins.input", side_effect=["4", "Red Comets", "Blue Stars",
                                          "Green Lions", "Golden Eagles"])
    def test_registers_four_teams(self, mocked_input):
        self.assertTrue(team_reg.register_teams())
        self.assertEqual(len(team_list), 4)
        self.assertEqual([t["id"] for t in team_list],
                         ["TM001", "TM002", "TM003", "TM004"])

    @patch("builtins.input", side_effect=["4", "Red Comets", " red comets ",
                                          "Blue Stars", "Green Lions",
                                          "Golden Eagles"])
    def test_duplicate_name_is_rejected_case_insensitively(self, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            result = team_reg.register_teams()
        self.assertTrue(result)
        self.assertEqual(len(team_list), 4)
        self.assertIn("This team already exists", output.getvalue())

    def test_registration_blocked_after_fixtures_exist(self):
        fixture_list.append({"id": "M001"})
        output = StringIO()
        with redirect_stdout(output):
            result = team_reg.register_teams()
        self.assertFalse(result)
        self.assertIn("No registration after Fixture", output.getvalue())

    def test_view_teams_when_empty(self):
        output = StringIO()
        with redirect_stdout(output):
            team_reg.view_teams()
        self.assertIn("No team has register yet.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
