from team_reg import team_list
fixture_list = []

def generate_fixture_id():
    numbers = [
        int(each["id"][1:])
        for each in fixture_list
        if each["id"].startswith("M") and each["id"][1:].isdigit()
    ]

    next_number = max(numbers, default=0) + 1
    return f"M{next_number:03d}"

def generate_fixture(team_list):
    length = len(team_list)

    if fixture_list:
        print("Fixtures have already been generated!")
        return

    for i in range(length):
        for j in range(i + 1, length):
            fixture = {
                "id": generate_fixture_id(),
                "home_id": team_list[i]["id"],
                "away_id": team_list[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixture_list.append(fixture)

    print("Fixture Generated!")
def display_fixture():
    if not fixture_list:
        print("No Fixture has been created yet.")
        return
    print("\n===== ALL FIXTURES =====")
    for fixture in fixture_list:
        home_name = ""
        away_name = ""

        for team in team_list:
            if team["id"] == fixture["home_id"]:
                home_name = team["team_name"]

            if team["id"] == fixture["away_id"]:
                away_name = team["team_name"]

        print(

            f"Match ID: {fixture["id"]}\n"
            f"{home_name}(home) vs {away_name}(away)\n"
            f"Status: {fixture["status"]}\n"
            f"{home_name} score: {fixture["home_score"]}\n"
            f"{away_name} score: {fixture["away_score"]}\n"
            
        )
        print("="*40)
