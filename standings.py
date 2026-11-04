def calculate_standings(team_list, fixture_list):
    standings = {}

    for team in team_list:
        standings[team["id"]] = {
            "team_name": team["team_name"],
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0   
        }
    
    
    for fixture in fixture_list:
        if fixture["status"] != "played":
            continue
        home_stats = standings[fixture["home_id"]]
        away_stats = standings[fixture["away_id"]]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        home_stats["goals_for"] += home_score
        away_stats["goals_for"] += away_score

        home_stats["goals_against"] += away_score
        away_stats["goals_against"] += home_score

        home_stats["played"] += 1
        away_stats["played"] += 1

        if home_score > away_score:
            home_stats["wins"] += 1
            away_stats["losses"] += 1
            home_stats["points"] += 3

        elif home_score == away_score:
            home_stats["draws"] += 1
            away_stats["draws"] += 1
            home_stats["points"] += 1
            away_stats["points"] += 1

        else:
            home_stats["losses"] += 1
            away_stats["wins"] += 1
            away_stats["points"] += 3


    for stand in standings.values(): 
        stand["goal_difference"] = stand["goals_for"] - stand["goals_against"]

    rankings = list(standings.values())
    rankings = sorted(
        rankings,
        key=lambda team: (-team["points"],-team["goal_difference"], -team["goals_for"], team["team_name"].casefold()),
    )

    return rankings

def display_standings(team_list, fixture_list):
    rankings = calculate_standings(team_list, fixture_list)
    print("\n======= FOOTBALL LEAGUE STANDINGS =======")
    print("")
    print("Pos | Club                | MP | W  | D  | L  | GF  | GA  | GD  | Pts ")
    print("-"*95)

    for index, stats in enumerate(rankings, start=1):
        print(f"{index:<4} | {stats['team_name']:<25} | {stats['played']:>4} | {stats['wins']:>4} | {stats['draws']:>4} | {stats['losses']:>4} | {stats['goals_for']:>5} | {stats['goals_against']:>5} | {stats['goal_difference']:>5} | {stats['points']:>5}")
        