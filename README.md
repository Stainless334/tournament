# Football League Management System

A Python command-line application for managing a football league. It allows users to register teams, generate fixtures, record match results, calculate league standings, determine the champion, and save league data for future sessions.

## Features

- **Team Registration:** Register 4–8 teams with unique names. Team names are trimmed and checked case-insensitively to prevent duplicates.
- **Fixture Generation:** Automatically generates a single round-robin tournament where every team plays every other team once.
- **Fixture Management:** Assigns unique match IDs and tracks fixtures as pending or played.
- **Match Results:** Records nonnegative integer scores and prevents a fixture from being played more than once.
- **League Standings:** Calculates matches played, wins, draws, losses, goals scored, goals conceded, goal difference, and points.
- **Ranking System:** Ranks teams by:
  1. Points
  2. Goal difference
  3. Goals scored
  4. Alphabetical team name
- **Champion Detection:** Announces the champion when every fixture has been completed. Otherwise, the league is labelled **IN PROGRESS**.
- **Data Persistence:** Saves and loads league information using JSON.
- **Data Validation:** Checks loaded data for invalid structures, duplicate IDs, invalid matchups, and inconsistent scores.

## Technologies

- Python 3
- JSON for data storage
- Python `unittest` for automated testing

The project uses Python's standard library and does not require external packages.

## Project Structure

```text
football-league/
│
├── main.py              # Main menu and application entry point
├── data.py              # Shared team and fixture lists
├── team_reg.py          # Team registration and display
├── fixture.py           # Fixture generation and display
├── record_result.py     # Match result recording
├── standings.py         # Standings calculation and champion detection
├── storage.py           # JSON saving, loading and validation
│
├── data/
│   └── league_data.json # Saved league information (created automatically)
│
└── tests/
    ├── test_team_reg.py
    ├── test_fixture.py
    ├── test_record_result.py
    ├── test_standings.py
    ├── test_storage.py
    └── test_main.py
```

## How to Run

Clone or download the project and navigate to its root directory.

Start the application:

```bash
python3 main.py
```

The main menu provides these options:

| Option | Function |
|---|---|
| 1 | Team Registration |
| 2 | View Registered Teams |
| 3 | Generate Fixtures |
| 4 | View Fixtures |
| 5 | Record Match Result |
| 6 | View Standings |
| 0 | Exit |

## Tournament Rules

- A minimum of 4 and maximum of 8 teams can be registered.
- Each team plays every other team exactly once.
- The total number of fixtures is calculated using:

  `n × (n - 1) / 2`

- A win awards 3 points.
- A draw awards 1 point to each team.
- A loss awards 0 points.
- Match results cannot be negative or recorded twice.
- The champion is announced only after all fixtures have been played.

## Data Storage

League information is stored in:

```text
data/league_data.json
```

The JSON file uses schema version `1` and stores registered teams and fixtures.

The application saves data after successful team registration, fixture generation, and match result recording. When restarted, it attempts to load the previously saved league data.

## Running Automated Tests

The project includes automated tests for its main features.

Run the test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The current test suite contains **51 tests**, all of which passed in the latest test run.

## Project Goal

This project demonstrates practical Python programming concepts, including:

- Functions and modules
- Lists and dictionaries
- Loops and conditional logic
- Input validation and error handling
- Sorting and calculations
- File handling and JSON
- Data validation
- Automated testing with `unittest`

It is designed as a practical Python project that demonstrates how to build a modular, data-driven command-line application.