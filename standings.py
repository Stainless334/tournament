def calculate_standings(team_list, fixture_list):
    standings = {}

    for team in team_list:
        standings[team["id"]] = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0   
        }

    

    
