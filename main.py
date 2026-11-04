from team_reg import register_teams, view_teams, team_list
from fixture import generate_fixture, display_fixture
from record_result import record_result

def main_menu():
    while True:
        print("\n========== WELCOME TO FOOTBALL LEAGUE ==========")
        print("""
        1. Team Registration
        2. View Registered Teams
        3. Create Fixture
        4. View Fixtures
        5. Uptdate Fixtures
        0. Exit
        """)
        entry = input("Enter a number from 0 to 5 => ")

        if entry == "1":
            register_teams()
        elif entry == "2":
            view_teams()
        elif entry == "3":
            generate_fixture(team_list)
        elif entry == "4":
            display_fixture()
        elif entry == "5":
            record_result()
        elif entry == "0":
            print("THANK YOU FOR CHOOSING FOOTBALL LEAGUE!!")
            break
        else:
            print("Invalid Input: Enter a number from 0 to 5")

if __name__ == "__main__":
    main_menu()