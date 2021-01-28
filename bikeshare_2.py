import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to view? '\
                'I have chicago, new york city or washington.\n')
    while True:
        if city.lower() in ['chicago', 'new york city', 'washington']:
            city = city.lower()
            break
        print('Hmm... I do not  have data for that city, enter Chicago, New York City or Washington')
        city = input('Try again: ')

    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to view? \n' \
            'Please type either: all, january, february, march, april, may or june. \n')
    while True:
        if month.lower() in ['all','january','february','march','april','may','june']:
            month = month.lower()
            break
        print('Hmm... I do not have data for that month. I only have: \n' \
        'all, january, february, march, april, may or june')
        month = input('Try again: ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week would you like to view? Please type either:' \
            '\nall, monday, tuesday, wednesday, thursday, friday, saturday or sunday. \n')
    while True:
        if day.lower() in ['all','monday','tuesday','wednesday','thursday',\
        'friday','saturday','sunday']:
            day = day.lower()
            break
        print('Hmm... I do not have data for that day. Please type either: \
        \nall, monday, tuesday, wednesday, thursday, friday, saturday or sunday')
        day = input('Try again: ')

    print('\nGreat! You chose the following: \nCity = {}\nMonth = {}\n' \
            'Day = {}'.format(city.title(),month.title(),day.title()))

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hours'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_raw_data(df):
    """Displays raw data, if requested, in groupings of five lines."""
    i = 0
    raw = input("Would you like to see the first five lines of raw data?\n").lower()
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            raw = input("Would you like to see five more lines?\n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_int = df['month'].mode()[0]
    popular_month = months[month_int - 1].title()

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    popular_hour = df['hours'].mode()[0]
    print('The busiest month, day and hour respectively are: {}, {} and'\
            ' {} o\'clock'.format(popular_month,popular_day,popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Combi'] = df['Start Station'] + ' to ' + df['End Station']
    combi = df['Combi'].mode()[0]

    print('Most common start and end stations respectively are: {}'\
        ' and {}.'.format(start_station, end_station))
    print('Most common trip is: {}'.format(combi))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time /= 3600

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time /= 60

    print('Total time: {} hours.'.format(round(total_time,1)))
    print('Average time: {} minutes.'.format(round(mean_time,1)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of users are: \n', user_types)

    # Display counts of gender
    if 'Gender' not in df.columns:
        print("No gender or birth data for Washington.")
    else:
        gender = df['Gender'].value_counts()

        # Display earliest, most recent, and most common year of birth
        youngest = int(df['Birth Year'].max())
        oldest = int(df['Birth Year'].min())
        common_birth = int(df['Birth Year'].mode()[0])

        print('Gender of users is: \n', gender)
        print('Max, min and most common birth years respectively are: '\
            '{}, {} and {}.'.format(youngest, oldest, common_birth))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in 'yes':
            break


if __name__ == "__main__":
	main()
