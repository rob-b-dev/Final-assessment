import csv  # Import csv module to handle csv data.


# Class to load, manage and display Disneyland review data.
class DisneylandReviewAnalyser:


    # Constructor method - initialise attributes.
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []  # Store dataset rows.


    # Load data from csv file into class instance.
    def load_data(self):
        # Open csv file with newline='' to encourage cross-platform compatibility.
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            # Use DictReader to automatically assign field names from the header.
            reader = csv.DictReader(csvfile)
            # Loop through and append data
            for row in reader:
                self.data.append(row)

        # Confirm successful load.
        print('Finished reading the dataset.')
        print(f'Number of rows in dataset: {len(self.data)}')


    # -------------------- Helper methods --------------------
    def return_to_main_menu(self):
        print('Returning to main menu...')
        raise StopIteration # Exit at the programs first function call - main menu in this instance.
    

    def gather_reviews_by_park(self):
        park_set = set() # Create set to ensure no repetition.

        for row in self.data:
            park_set.add(row['Branch']) # Loop through and add branches of parks to set.

        # Map letters to park names
        park_options = {chr(65 + i): park for i, park in enumerate(park_set)}

        # Continuous loop until break
        while True:
            print("Select the Park you wish to see the Reviews for:")
            for letter, branch in park_options.items():
                print(f"[{letter}] {branch}")
            print("[X] Return to main menu")

            choice = input("").strip().upper()

            if choice == 'X':
                self.return_to_main_menu()
            elif choice in park_options:
                selected_park = park_options[choice]
                print(f"You have selected {selected_park}")
                return selected_park
                
            else:
                print("Invalid option. Please try again.")
        


    def gather_reviews_by_location(self, dataset_scope):
        # Gather locations from park_reviews and sort alphabetically.
        locations = sorted({row['Reviewer_Location'] for row in dataset_scope}) # Data gathered from argument 'dataset_scope', as the scope can vary. It could be the entire dataset or a segment of it.
        
        # Loop through index and values of sorted locations.
        for i, location in enumerate(locations, 1):
            print(f"[{i}] {location}")  # Number locations.
        
        # Validation
        while True:
            choice = input("Select the Location number for the Park you wish to see the reviews for: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(locations):
                selected_location = locations[int(choice) - 1]
                return selected_location
            else:
                print('Invalid option. Please try again.')


    # -------------------- Sub-menu handlers --------------------
    def view_data_menu(self):
        while True:
            view_option = input('''
Please enter one of the following options:
[A] View Reviews by Park
[B] Number of Reviews by Park and Reviewer Location
[C] Average Score per Year by Park
[D] Average Score per Year by Reviewer Location
[X] Return to Main Menu
''').strip().upper()

            if view_option == 'A':
                self.view_reviews_by_park()
            elif view_option == 'B':
                self.view_reviews_by_park_and_location()
            elif view_option == 'C':
                self.average_score_per_year_by_park()
            elif view_option == 'D':
                self.average_score_per_year_by_location()
            elif view_option == 'X':
                self.return_to_main_menu()
            else:
                print('Invalid option. Please try again.')
            


    def visualise_data_menu(self):
        while True:
            visualise_option = input('''
Please enter one of the following options:
[A] Most reviewed Parks
[B] Park Ranking by Nationality
[C] Average Popular Month by Park
[X] Return to Main Menu                          
''').strip().upper()

            if visualise_option == 'A':
                print('Visualising: Most Reviewed Parks')
            elif visualise_option == 'B':
                print('Visualising: Park Ranking by Nationality')
            elif visualise_option == 'C':
                print('Visualising: Most Popular Month by Park')
            elif visualise_option == 'X':
                self.return_to_main_menu()
            else:
                print('Invalid option. Please try again.')


    # -------------------- View data methods --------------------
    def view_reviews_by_park(self):
        # Gather and display reviews based on park branch.
        selected_park = self.gather_reviews_by_park()
        [print(row) for row in self.data if row['Branch'] == selected_park]


    def view_reviews_by_park_and_location(self):
             # Gather reviews based on park branch.
            selected_park = self.gather_reviews_by_park()
            park_reviews = [row for row in self.data if row['Branch'] == selected_park]

            selected_location = self.gather_reviews_by_location(park_reviews)
            for row in park_reviews:
                    if row['Reviewer_Location'] == selected_location:
                        print(row)


    def average_score_per_year_by_park(self):
        print('Showing average Score per Year by Park (functionality pending) ...')


    def average_score_per_year_by_location(self):
        print('Showing average Score per Year by Location (functionality pending) ...')


    # -------------------- Main menu --------------------
    def run(self):
        print('''
--------------------------
Disneyland Review Analyser
--------------------------
''')

        self.load_data()  # Load data on program start

        # Loop continuously until break
        while True:
            try:
                menu_choice = input('''
Please enter the letter which corresponds with your desired menu choice:
[A] View Data
[B] Visualise Data
[X] Exit
''').strip().upper()

                if menu_choice == 'A':
                    print('You have chosen option A - View Data')
                    self.view_data_menu()
                elif menu_choice == 'B':
                    print('You have chosen option B - Visualise Data')
                    self.visualise_data_menu()
                elif menu_choice == 'X':
                    print('Exiting program...')
                    break
                else:
                    print('Invalid option. Please try again.')
            except StopIteration:
                # Catch controlled exit from sub-menus so program doesnt crash.
                continue


# # Run main function - entry point
# if __name__ == '__main__':
file_path = './data/disneyland_reviews.csv'  # Define file path.

analyser = DisneylandReviewAnalyser(file_path)  # Create instance and run program.
analyser.run()
