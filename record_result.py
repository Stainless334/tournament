from data import fixture_list
import time


def record_result():
    result_recorded = False
    if not fixture_list:
        print("No Fixture Available.")
        return False
    while True:
        while True:

            fixture_id = input("Enter fixture ID (or 0 to go back): ").strip()

            if fixture_id == "0":
                print("Returning to main menu...")
                time.sleep(2)
                return result_recorded

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

        fixture["home_score"] = home_score
        fixture["away_score"] = away_score
        fixture["status"] = "played"
        result_recorded = True
        print("Result recorded successfully!")
        

        while True:
            choice = input("Would you like to record another result? (yes/no): ").strip().lower()

            if choice == "yes":
                break
            elif choice == "no":
                print("Returning to main menu...")
                time.sleep(3)
                return result_recorded
            
            else:
                print("Please enter yes or no.")
