import csv  # Import csv module to handle csv data.
import matplotlib.pyplot as plt


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
            # Loop through and append data.
            for row in reader:
                self.data.append(row)

        # Confirm successful load.
        print('Finished reading the dataset.')
        print(f'Number of rows in dataset: {len(self.data)}')


    # -------------------- Helper methods --------------------
    def return_to_main_menu(self):
        print('Returning to main menu...')
        raise StopIteration # Exit at the programs first function call - main menu in this instance.
    

    def gather_park(self):
        park_set = {row['Branch'] for row in self.data} # Create set to ensure no repetition.

        # Create dictionary to map latters to parks.
        park_options = {chr(65 + i): park for i, park in enumerate(park_set)}

        # Continuous loop until break.
        while True:
            print("Select the Park you wish to see the Reviews for:")
            for letter, branch in park_options.items():
                print(f"[{letter}] {branch}")

            choice = input("").strip().upper()

            if choice in park_options:
                selected_park = park_options[choice]
                print(f"You have selected {selected_park}")
                return selected_park
            else:
                print("Invalid option. Please try again.")
        

    def gather_location(self, dataset_scope):
        # Gather locations as set and sort alphabetically.
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


    def gather_year(self, dataset_scope, placeholder): # Dataset scope used for flexibility.
        # Dates and years gathered from desired scope as sets to ensure no unnecessary repitition.
        dates = {row['Year_Month'] for row in dataset_scope}
        years = sorted({date.split('-')[0] for date in dates if date != 'missing'})
        
        year_options = {chr(65 + i): park for i, park in enumerate(years)}

        for letter, year in year_options.items():
            print(f'[{letter}] {year}')
        
        while True:
            
            choice = input(f"Select the Year for the Park you wish to see the {placeholder} for: ").strip().upper()

            if choice in year_options:
                selected_year = year_options[choice]
                print(f"You have selected {selected_year}")
                return selected_year
            else:
                print("Invalid option. Please try again.")

    
    def calculate_average_score(self, dataset_scope): # Dataset scope used for flexibility.
        total_score = sum(int(row['Rating']) for row in dataset_scope)
        average_score = total_score / len(dataset_scope)
        return round(average_score, 1)


    # -------------------- Sub-menu handlers --------------------
    def view_data_menu(self):
        while True:
            try:
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
                    self.view_average_score_per_year_by_park()
                elif view_option == 'D':
                    self.view_average_score_per_year_by_location()
                elif view_option == 'X':
                    self.return_to_main_menu()
                else:
                    print('Invalid option. Please try again.')
            except StopIteration:
                # Catch controlled exit from sub-menus so program doesnt crash.
                break
            

    def visualise_data_menu(self):
        while True:
            try:
                visualise_option = input('''
Please enter one of the following options:
[A] Most reviewed Parks
[B] Park Ranking by Nationality
[C] Average Popular Month by Park
[X] Return to Main Menu                          
''').strip().upper()

                if visualise_option == 'A':
                    self.visualise_reviewcount_by_park()
                elif visualise_option == 'B':
                    self.visualise_toplocations_by_average_score()
                elif visualise_option == 'C':
                    print('Visualising: Most Popular Month by Park')
                elif visualise_option == 'X':
                    self.return_to_main_menu()
                else:
                    print('Invalid option. Please try again.')
            except StopIteration:
                # Catch controlled exit from sub-menus so program doesnt crash.
                break


    # -------------------- View data methods --------------------
    def view_reviews_by_park(self):
        selected_park = self.gather_park()
        [print(row) for row in self.data if row['Branch'] == selected_park]


    def view_reviews_by_park_and_location(self):
        # Gather reviews based on park branch.
        selected_park = self.gather_park()
        park_reviews = [row for row in self.data if row['Branch'] == selected_park]

        selected_location = self.gather_location(park_reviews)
        [print(row) for row in park_reviews if row['Reviewer_Location'] == selected_location]


    def view_average_score_per_year_by_park(self):
        selected_park = self.gather_park()
        park_reviews = [row for row in self.data if row['Branch'] == selected_park]

        # Allow users to choose between a specific year or all years.
        choice = input("Do you want to view the average for [A]ll years or a [S]pecific year? ").strip().upper()

        if choice == 'S':
            # Gather specific year.
            selected_year = self.gather_year(park_reviews, 'Average Score')
            year_reviews = [row for row in park_reviews if row['Year_Month'].startswith(selected_year)]
            average_score = self.calculate_average_score(year_reviews)
            print(f"Average Score for the Park {selected_park} in the Year {selected_year}: {average_score}")
        else:
            # Gather all years as set and sort.
            all_years = sorted({row['Year_Month'].split('-')[0] for row in park_reviews if row['Year_Month'] != 'missing'})
            # Loop through each year and gather average score for each year.
            for year in all_years:
                year_reviews = [row for row in park_reviews if row['Year_Month'].startswith(year)]
                average_score = self.calculate_average_score(year_reviews)
                print(f"{year}: {average_score}")


    def view_average_score_per_year_by_location(self):
        selected_location = self.gather_location(self.data)
        location_reviews = [row for row in self.data if row['Reviewer_Location'] == selected_location]

        # Allow users to choose between a specific year or all years.
        choice = input("Do you want to view the average for [A]ll years or a [S]pecific year? ").strip().upper()

        if choice == 'S':
            # Gather specific year from helper function.
            selected_year = self.gather_year(location_reviews, 'Average Score')
            year_reviews = [row for row in location_reviews if row['Year_Month'].startswith(selected_year)]
            average_score = self.calculate_average_score(year_reviews)
            print(f"Average Score for all parks in {selected_location} in the Year {selected_year}: {average_score}")
        else:
            # Gather all years as set and sort.
            all_years = sorted({row['Year_Month'].split('-')[0] for row in location_reviews if row['Year_Month'] != 'missing'})
            # Loop through each year and gather average score for each year.
            for year in all_years:
                year_reviews = [row for row in location_reviews if row['Year_Month'].startswith(year)]
                average_score = self.calculate_average_score(year_reviews)
                print(f"{year}: {average_score}")
    

    def visualise_reviewcount_by_park(self):
        park_set = {row['Branch'] for row in self.data} # Create set to ensure no repetition.
        # Create dictionary to map review numbers to park.
        branch_counts = {park: len([row for row in self.data if row['Branch'] == park]) for park in park_set}
        # Convert to list.
        sizes = list(branch_counts.values())
        
        plt.figure(figsize=(10, 8))
        wedges, texts, autotexts = plt.pie(
            sizes,
            autopct=lambda p: int(p * sum(sizes) / 100) # Allow sizes to be displayed in wedges.
            )

        labels = [branch for branch in branch_counts.keys()]
        plt.legend(wedges, labels, title="Parks", loc="center left")
        plt.setp(autotexts, size=10, color='white', weight='bold')
        plt.title('Number of Reviews per Park')
        plt.show()


    def visualise_toplocations_by_average_score(self):
        selected_park = self.gather_park()
        park_reviews = [row for row in self.data if row['Branch'] == selected_park]

        # List comprehension to reduce code - creates dictioanry of average values assigned to each location for a specific park.
        location_average_scores = { location: sum(int(row['Rating']) for row in park_reviews if row['Reviewer_Location'] == location) / 
                                    len([row for row in park_reviews if row['Reviewer_Location'] == location]) for location in {row['Reviewer_Location'] for row in park_reviews}
                                    }

        # Gather top 10 average values.
        top_10_average_scores = sorted(location_average_scores.items(), key=lambda x: x[1], reverse=True)[:10]

        # Gather top 20 average values.
        top_10_average_scores = sorted(location_average_scores.items(), key=lambda x: x[1], reverse=True)[10:20]

        # Unpack locations and average_scores from top 10 values.
        locations, average_scores = zip(*top_10_average_scores)
        
        def defaultOptions():
            plt.ylabel('Average Score')
            plt.xlabel('Locations')
            plt.title(f'Top 10 Locations by Average Score for {selected_park}')
            plt.xticks(rotation=45, ha='right')
            plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(locations, average_scores, color='blue', width=0.3)
        defaultOptions()

        plt.figure(figsize=(10, 5))
        plt.bar(locations, average_scores, color='blue', width=0.3)
        defaultOptions()

    
    def visualise_average_score_per_month(self):
        selected_park = self.gather_park()
        park_reviews = [row for row in self.data if row['Branch'] == selected_park]

        # while True:

        #     choice = input('Would you like to display the Average Rating across Months from a [S]pecific Year or [A]ll Years? ').strip().upper()


    # -------------------- Main menu --------------------
    def run(self):
        print('''
--------------------------
Disneyland Review Analyser
--------------------------
''')

        self.load_data()  # Load data on program start.

        # Loop continuously until break.
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


# Run main function - entry point.
if __name__ == '__main__':
    file_path = './data/disneyland_reviews.csv'  # Define file path.

    analyser = DisneylandReviewAnalyser(file_path)  # Create instance and run program.
    analyser.run()