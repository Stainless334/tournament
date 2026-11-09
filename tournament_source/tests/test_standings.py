import unittest
from contextlib import redirect_stdout
from io import StringIO

from standings import calculate_standings, display_standings


class TestStandings(unittest.TestCase):
    def setUp(self):
        self.teams = [
            {"id": "TM001", "team_name": "Alpha"},
            {"id": "TM002", "team_name": "Beta"},
            {"id": "TM003", "team_name": "Gamma"},
        ]

    def test_empty_league_returns_empty_rankings(self):
        self.assertEqual(calculate_standings([], []), [])

    def test_pending_fixture_does_not_affect_statistics(self):
        fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "pending", "home_score": None, "away_score": None
        }]
        rankings = calculate_standings(self.teams, fixtures)
        alpha = next(row for row in rankings if row["team_name"] == "Alpha")
        self.assertEqual(alpha["played"], 0)
        self.assertEqual(alpha["points"], 0)

    def test_win_updates_all_statistics(self):
        fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "played", "home_score": 3, "away_score": 1
        }]
        rankings = calculate_standings(self.teams, fixtures)
        alpha = next(row for row in rankings if row["team_name"] == "Alpha")
        beta = next(row for row in rankings if row["team_name"] == "Beta")
        self.assertEqual((alpha["played"], alpha["wins"], alpha["points"]), (1, 1, 3))
        self.assertEqual((beta["played"], beta["losses"], beta["points"]), (1, 1, 0))
        self.assertEqual(alpha["goal_difference"], 2)

    def test_draw_awards_one_point_each(self):
        fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "played", "home_score": 2, "away_score": 2
        }]
        rankings = calculate_standings(self.teams, fixtures)
        for row in rankings:
            if row["team_name"] in ("Alpha", "Beta"):
                self.assertEqual(row["draws"], 1)
                self.assertEqual(row["points"], 1)

    def test_sorting_uses_points_then_goal_difference_then_goals_for(self):
        fixtures = [
            {"id": "M001", "home_id": "TM001", "away_id": "TM002",
             "status": "played", "home_score": 2, "away_score": 0},
            {"id": "M002", "home_id": "TM001", "away_id": "TM003",
             "status": "played", "home_score": 1, "away_score": 0},
        ]
        rankings = calculate_standings(self.teams, fixtures)
        self.assertEqual(rankings[0]["team_name"], "Alpha")

    def test_alphabetical_name_breaks_complete_tie(self):
        teams = [
            {"id": "TM001", "team_name": "zulu"},
            {"id": "TM002", "team_name": "Alpha"},
        ]
        rankings = calculate_standings(teams, [])
        self.assertEqual(rankings[0]["team_name"], "Alpha")

    def test_display_marks_league_in_progress_if_fixture_pending(self):
        fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "pending", "home_score": None, "away_score": None
        }]
        output = StringIO()
        with redirect_stdout(output):
            display_standings(self.teams, fixtures)
        self.assertIn("LEAGUE STATUS: IN PROGRESS", output.getvalue())
        self.assertNotIn("CHAMPION:", output.getvalue())

    def test_display_announces_champion_when_all_fixtures_played(self):
        fixtures = [{
            "id": "M001", "home_id": "TM001", "away_id": "TM002",
            "status": "played", "home_score": 2, "away_score": 0
        }]
        output = StringIO()
        with redirect_stdout(output):
            display_standings(self.teams, fixtures)
        self.assertIn("LEAGUE STATUS: COMPLETED", output.getvalue())
        self.assertIn("CHAMPION: ALPHA", output.getvalue())


if __name__ == "__main__":
    unittest.main()
