from team_reg import team_list
from fixture import fixture_list

import json
import os
STORE = "data/league_data.json"

def save_data(team_list, fixture_list):

    data = {
        "schema_version": 1,
        "teams": team_list,
        "fixtures": fixture_list
    }
   
    os.makedirs("data", exist_ok=True)

    with open(STORE, "w", encoding="utf-8") as save_file:
        json.dump(data, save_file, indent=4)

def load_data():
    
    try:
        with open(STORE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: Invalid json syntax detected!")
        return False
    except FileNotFoundError:
        print("Error: League data file not found!")
        return False
    if not isinstance(data, dict):
        print("Error: Invalid league data structure!")
        return False
    required_top_keys = ("schema_version", "teams", "fixtures")
    if any(key not in data for key in required_top_keys):
        print("Error: Missing required data!")
        return False
    if data["schema_version"] != 1:
        print("Error: Invalid version!")
        return False
    if not isinstance(data["teams"], list):
        print("Error: Invalid team data!")
        return False
    if not isinstance(data["fixtures"], list):
        print("Error: Invalid fixture data!")
        return False
    team_ids = set()
    for team in data["teams"]:
        if not isinstance(team, dict):
            print("Error: Invalid team data!")
            return False
        if not isinstance(team["id"], str) or team["id"].strip() == "":
            return False
        if "id" not in team or "team_name" not in team:
            print("Error: Invalid team data!")
            return False
        if team["id"] in team_ids:
            print("Error: Invalid team data!")
            return False
        team_ids.add(team["id"])
        if (
            not isinstance(team["team_name"], str)
            or team["team_name"].strip() == ""
            or len(team["team_name"]) < 2
            or len(team["team_name"]) > 30
        ):
            print("Error: Invalid team data!")
            return False
    fixture_ids = set()
    matchups = set()
    required_keys = ("id", "home_id", "away_id", "status", "home_score", "away_score")
    
    for fixture in data["fixtures"]:
        if not isinstance(fixture, dict):
            print("Error: Invalid fixture data!")
            return False
        if not isinstance(fixture["id"], str) or fixture["id"].strip() == "":
            return False
        if any(key not in fixture for key in required_keys):
            print("Error: Invalid fixture data!")
            return False
        if fixture["id"] in fixture_ids:
            print("Error: Invalid fixture data!")
            return False
        fixture_ids.add(fixture["id"])
        if(
            not isinstance(fixture["home_id"], str) 
            or not isinstance(fixture["away_id"], str) 
            or fixture["home_id"].strip() == "" 
            or fixture["away_id"].strip() == ""
        ):
            print("Error: Invalid fixture data!")
            return False
        if fixture["home_id"] not in team_ids or fixture["away_id"] not in team_ids:
            print("Error: Invalid fixture data!")
            return False
        if fixture["home_id"] == fixture["away_id"]:
            print("Error: Invalid fixture data!")
            return False
        matchup = frozenset((fixture["home_id"], fixture["away_id"]))
        if matchup in matchups:
            print("Error: Invalid fixture data!")
            return False
        matchups.add(matchup)
        if not isinstance(fixture["status"], str) or fixture["status"] not in ("pending", "played"):
            print("Error: Invalid fixture data!")
            return False
        if fixture["status"] == "pending" and (
            fixture["home_score"] is not None or 
            fixture["away_score"] is not None
        ):
            print("Error: Invalid fixture data!")
            return False
        if fixture["status"] == "played" and (
            not isinstance(fixture["home_score"], int) or 
            type(fixture["home_score"]) is bool or 
            fixture["home_score"] < 0
        ):
            print("Error: Invalid fixture data!")
            return False
        if fixture["status"] == "played" and (
            not isinstance(fixture["away_score"], int) or 
            type(fixture["away_score"]) is bool or 
            fixture["away_score"] < 0
        ):
            print("Error: Invalid fixture data!")
            return False
    team_list[:] = data["teams"]
    fixture_list[:] = data["fixtures"]
    return True

if load_data():
    print("League data loaded successfully!")
else:
    print("Could not load league data.")