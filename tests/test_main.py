import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import main


class TestMainMenu(unittest.TestCase):
    @patch("builtins.input", side_effect=["0"])
    def test_menu_exits(self, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            main.main_menu()
        self.assertIn("THANK YOU FOR CHOOSING FOOTBALL LEAGUE", output.getvalue())

    @patch("builtins.input", side_effect=["invalid", "0"])
    def test_invalid_menu_choice_is_reported(self, mocked_input):
        output = StringIO()
        with redirect_stdout(output):
            main.main_menu()
        self.assertIn("Invalid Input", output.getvalue())


if __name__ == "__main__":
    unittest.main()
