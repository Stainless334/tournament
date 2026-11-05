from team_reg import register_teams, view_teams, team_list
from fixture import generate_fixture, display_fixture, fixture_list
from record_result import record_result
from standings import display_standings

def main_menu():
    print("\n========== WELCOME TO FOOTBALL LEAGUE ==========")

    while True:
        print("""
        1. Team Registration
        2. View Registered Teams
        3. View Fixtures
        4. Uptdate Fixtures
        5. View Standings
        0. Exit
        """)
        entry = input("Enter a number from 0 to 5 => ")

        if entry == "1":
            register_teams()
        elif entry == "2":
            view_teams()
        elif entry == "3":
            display_fixture()
        elif entry == "4":
            record_result()
        elif entry == "5":
            display_standings(team_list, fixture_list)
        elif entry == "0":
            print("THANK YOU FOR CHOOSING FOOTBALL LEAGUE!!")
            break
        else:
            print("Invalid Input: Enter a number from 0 to 5")

if __name__ == "__main__":
    main_menu()