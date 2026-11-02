team_list = []

def register_teams():
    print("Enter the number of teams from 4 to 8")

    team = input("Your answer: ").strip()

    try:
        team = int(team)
    except ValueError:
        print("Invalid: Please enter a number.")
        return

    if team < 4 or team > 8:
        print("Number out of range!")
        return

    for each in range(team):

        while True:
            team_name = input(
                f"Enter a team name for team {chr(65 + each)}: "
            ).strip()

            if not team_name:
                print("Team name cannot be empty. Try again.")
                continue

            if any(team_name.casefold() == existing.casefold()
                   for existing in team_list):
                print("This team already exists. Please enter a different name.")
                continue

            team_list.append(team_name.capitalize())
            break

    return team_list


