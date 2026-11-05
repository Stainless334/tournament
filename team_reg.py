team_list = []

def generate_team_id():
    numbers = [
        int(each["id"][2:])
        for each in team_list
        if each["id"].startswith("TM") and each["id"][2:].isdigit()
    ]

    next_number = max(numbers, default=0) + 1
    return f"TM{next_number:03d}"

def register_teams():
    while True:

        print("Enter the number of teams from 4 to 8 (or 0 to go back)")

        team = input(">>> ").strip()

        try:
            team = int(team)
        except ValueError:
            print("Invalid: Please enter a number.")
            continue

        if team == 0:
            return

        if team < 4 or team > 8:
            print("Number out of range!")
            continue
        break

    for each in range(team):

        while True:
            team_name = input(
                f"Enter a team name for team {chr(65 + each)}: "
            ).strip()

            if not team_name:
                print("Team name cannot be empty. Try again.")
                continue
            if len(team_name) < 2 or len(team_name) > 30:
                print("Lenght of team_name be between 2 and 30")

            if any(team_name.casefold() == existing["team_name"].casefold()
                   for existing in team_list):
                print("This team already exists. Please enter a different name.")
                continue

            teams = {
                "id": generate_team_id(),
                "team_name": team_name
            }

            team_list.append(teams)
            break
    print(f"{team} Teams Registered Successfully!!")

def view_teams():
    if not team_list:
        print("No team has register yet.")
        return
    print("\n ======= REISTERED TEAMS ========")
    for each in team_list:
        print(f"{each["id"]} => {each["team_name"]}")