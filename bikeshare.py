import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './chicago.csv',
              'newyork': './new_york_city.csv',
              'washington': './washington.csv' }

def ask_until(prompt, valid_set):
    """Prompt until user's answer is in valid_set."""
    while True:
        ans = input(prompt).lower()
        if ans in valid_set:
            return ans
        print("Invalid input. Please try again.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'newyork', 'washington']
    valid_month =['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    city = ask_until("Would you like to see statistics for Chicago, NewYork, or Washington?\n",  valid_cities)
    while True:
        filter_data = input("Would you like to filter the data (by month and day) or not? Enter yes or no\n").lower()
        if filter_data == 'yes':
            # TO DO: get user input for month (all, january, february, ... , june)
            month = ask_until("Which month? January, February, March, April, May, June or All?\n",  valid_month)
            day = ask_until("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n",  valid_day)
            break
        elif filter_data == 'no':
            print("You dont want filter data.\n")
            month = 'no'
            day = 'no'
            break
        print("Invalid filter. Please try again\n")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour       
    df['day_of_week'] = df['Start Time'].dt.day_name()        
    df['month_name'] = df['Start Time'].dt.month_name()
    df_city = df
    if month != 'all':
        df = df[df['month_name'].str.lower() == month.lower()]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]
    return df, df_city


def time_stats(city, df_city ):
    """Displays statistics on the most frequent times of travel in specificed city."""

    print('\nCalculating The Most Frequent Times of Travel in '+ city.upper() +' (No time filter applied)...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df_city['month_name'].mode()[0]
    print("Most common month:", popular_month)

    # TO DO: display the most common day of week
    popular_day = df_city['day_of_week'].mode()[0]
    print("Most common day of week:", popular_day)

    # TO DO: display the most common start hour
    popular_hour = df_city['hour'].mode()[0]
    print("Most common hour of day:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip (Time filter applied)...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most common start station:", popular_start_station)

    # TO DO: display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print("Most common end station:", popular_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    df = df.copy()
    df['route']  = df['Start Station'] + " → " + df['End Station']
    popular_route = df['route'].mode()[0]
    print("Most common route:", popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration (Time filter applied)...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time ' + str(total))
    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()
    print('Average travel time ' + str(mean))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_counts(title, series):
    print(f"{title}:")
    for item, count in series.value_counts().to_dict().items():
        print(f"{item}: {count}")

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats (Time filter applied)...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print_counts("User Type", df['User Type'])
   
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print_counts("Gender", df['Gender'])
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])

        print("Earliest year of birth:", earliest)
        print("Most recent year of birth:", most_recent)
        print("Most common year of birth:", most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_raw_data(city, df_city):
    i = 0
    while True:
        print(df_city.iloc[i:i+5])
        show_data = input('\nWould you like to view more data in '+ city + '? Enter yes or no.\n')
        if show_data.lower() != 'yes':
            break
        i +=5
        if i >= len(df_city):
            print("\nNo more data to display")
            break
def main():
    
    while True:
        city, month, day = get_filters()
        if month == 'no' and day == 'no':
            break
        df, df_city = load_data(city, month, day)
        time_stats(city, df_city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart analanys process? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    while True:
        valid_cities = ['chicago', 'newyork', 'washington']
        viewed_city = ask_until("Would you like to see data for Chicago, NewYork, or Washington?\n",  valid_cities)
        df_city = pd.read_csv(CITY_DATA[viewed_city])
        display_raw_data(viewed_city,df_city)
        restart = input('\nWould you like to restart process to view data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
