from fixture import fixture_list


def record_result():
    if not fixture_list:
        print("No Fixture Available.")
        return
    while True:
        
        fixture_id = input("Enter fixture ID (or 0 to go back): ").strip()

        if fixture_id == "0":
            return

        fixture = None

        for each in fixture_list:
            if fixture_id == each["id"]:
                fixture = each
                break

        if fixture is None:
            print("Fixture ID does not exist.")
            continue

        if fixture["status"] == "played":
            print("This fixture has already been played.")
            continue

        break

    while True:
        try:
            home_score = int(input("Enter home score: "))
        except ValueError:
            print("Enter a valid integer.")
            continue

        if home_score < 0:
            print("Score cannot be negative.")
            continue

        break

    # Validate away score
    while True:
        try:
            away_score = int(input("Enter away score: "))
        except ValueError:
            print("Enter a valid integer.")
            continue

        if away_score < 0:
            print("Score cannot be negative.")
            continue

        break

    # Update the fixture after both scores are valid
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"

    print("Result recorded successfully!")