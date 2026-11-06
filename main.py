from data import team_list, fixture_list
from team_reg import register_teams, view_teams
from fixture import generate_fixture, display_fixture
from record_result import record_result
from standings import display_standings
from storage import save_data, load_data
import time

def main_menu():
    print("\n========== WELCOME TO FOOTBALL LEAGUE ==========")
    

    while True:
        print("""
        1. Team Registration
        2. View Registered Teams
        3. Generate Fixtures
        4. View Fixtures
        5. Record Match Result
        6. View Standings
        0. Exit
        """)
        entry = input("Enter a number from 0 to 6 => ")

        if entry == "1":
            result = register_teams()
            if result is True:
                save_data(team_list, fixture_list)
        elif entry == "2":
            view_teams()
        elif entry == "3":
            fixture_result = generate_fixture(team_list)
            if fixture_result is True:
                save_data(team_list, fixture_list)
        elif entry == "4":
            display_fixture()
        elif entry == "5":
            record = record_result()
            if record is True:
                save_data(team_list, fixture_list)
        elif entry == "6":
            display_standings(team_list, fixture_list)
        elif entry == "0":
            print("THANK YOU FOR CHOOSING FOOTBALL LEAGUE!!")
            break
        else:
            print("Invalid Input: Enter a number from 0 to 6")

if __name__ == "__main__":
    if load_data():
        print("Loading saved data...")
        time.sleep(3)
        print("League data loaded successfully!")
    else:
        print("Could not load league data.")
    main_menu()