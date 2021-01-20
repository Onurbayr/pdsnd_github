import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_month():
    """
    Gets user input for month (january, february, ... , june)
    Returns:
        (str) month - name of the month
    """

    month = input("Which month? January, February, March, April, May, or June? :").lower().strip()
    print()
    while month not in ("january", "february", "march", "april", "may","june"):
        month = input("Please check your typing and choose a month :").lower().strip()
        print()
        pass
    return month

def get_day():
    """
    Gets user input for day of week
    Returns:
        (int) day - number of the day (e.g., 1=Monday 2=Tuesday ...)
    """

    day = input("Which day? Please type your response as an integer (e.g., 1=Monday 2=Tuesday ...) :")
    print()
    while day not in ("1", "2", "3", "4", "5", "6", "7"):
        day = input("Please check your typing and choose between 1 and 7 :")
        print()
        pass
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print()
    print('Hello! Let\'s explore some US bikeshare data!')
    print()

    # gets user input for city (chicago, new york city, washington).
    city = input("Would you like to see data for Chicago, New York, or Washington? \nPlease type the FIRST LETTER of the city :").lower().strip()
    print()
    while city not in ("c","n","w"):
        city = input("Please check your typing (e.g., N=New York) :").lower().strip()
        print()
        pass

    # gets user options for time filter.
    options = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter :").lower().strip()
    print()
    while options not in ("month","day","both","none"):
        options = input("Please check your typing and choose 'month' or 'day' or 'both' or 'none' :").lower().strip()
        print()
        pass

    if options == "month":
        day = "all"
        month = get_month()

    if options == "day":
        month = "all"
        day = get_day()

    if options == "both":
        month = get_month()
        day = get_day()

    if options == "none":
        month = "all"
        day = "all"

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

    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday + 1

    # filters by month if applicable
    if month != 'all':
        # uses the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week if applicable
    if day != 'all':
        # filters by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', months[popular_month - 1])

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', days[popular_day - 1])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start end station'] = df['Start Station'] + " => " + df['End Station']
    poupular_path = df['start end station'].mode()[0]
    print('Most Commonly Used Travel Path:', poupular_path)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, "seconds.")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', average_travel_time, "seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type:\n{}\n".format(user_types))

    # Displays counts of gender. Displays earliest, most recent, and most common year of birth
    if city != 'w':
        gender_types = df['Gender'].value_counts()
        print("Counts of Each Gender:\n{}\n".format(gender_types))
        min_birth = df['Birth Year'].min()
        print("Earliest Year of Birth: {}\n".format(int(min_birth)))
        max_birth = df['Birth Year'].max()
        print("Most Recent Year of Birth: {}\n".format(int(max_birth)))
        popular_birth = df['Birth Year'].mode()[0]
        print("Most Common Year of Birth:", int(popular_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        #print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        #displays row data 5 by 5 according to user preference
        show_data = input('\nWould you like view individual trip data? Enter yes or no.\n')
        df = load_data(city, month, day)
        df.pop('month')
        df.pop('day_of_week')
        row_show_index=0
        while show_data.lower() == 'yes':
            print(df.iloc[0 + row_show_index : 5 + row_show_index])
            row_show_index +=5
            show_data = input('\nWould you like view individual trip data? Enter yes or no.\n')
            pass

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
