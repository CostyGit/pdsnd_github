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
        (str) month - name of the month to filter by, or "no filter" to apply no month filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """
    Get user input for city (chicago, new york city, washington).
    """
    while True:
        city = str(input('Would you like to explore data for Chicago, New York City, or Washington?').lower().strip())
        if city not in ['chicago', 'new york city', 'washington']:
            print('Please enter valid city.')
            continue
        else:
            print('Great! Let\'s explore the data for {}.'.format(city.title()))
            break

    """
    Get user input for month (no filter, january, february, ... , june)
    """
    while True:
        month = str(input('Which month would you like to explore? January, February, March, April, May, or June? Please type out the full month name. Type "no filter" for no month filter.').lower().strip())
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'no filter']:
            print('Please enter valid input.')
            continue
        else:
            print('Alright! {} it is.'.format(month.title() ))
            break

    print('-'*40)
    return city, month


def load_data(city, month):
    """
    Loads data for the specified city and filters by month if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create new column
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'no filter':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        # filter by month to create the new dataframe

    return df


def time_stats(df, month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'no filter':
        df['month'] = df['Start Time'].dt.month_name()
        popular_month = df['month'].mode()[0]
        print('Most popular month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()

    popular_weekday = df['day_of_week'].mode()[0]

    print('Most popular day of the week:', popular_weekday)

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

    # extract most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    # extract display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    # extract most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + df['End Station']

    most_frequent_combination = df.groupby(['start_end']).size().idxmax()

    print('Most Popular Start Station:', popular_start_station)

    print('Most Popular End Station:', popular_end_station)

    print('Most frequent combination of start and end station:', most_frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # extract total travel time
    total_travel_time = df['Trip Duration'].sum()

    # extract display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel_time)

    print('Mean Travel Time:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:

        user_gender = df['Gender'].value_counts()

        print(user_gender.to_string())
    else:
        print('No information about gender available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        earliest_yob = df['Birth Year'].min()

        print('Earliest year of birth:', int(earliest_yob))

        most_recent_yob = df['Birth Year'].max()

        print('Most recent year of birth:', int(most_recent_yob))

        most_common_yob = df['Birth Year'].mode()[0].astype(int)

        print('Most common year of birth:', most_common_yob)
    else:
        print('No information about year of birth available.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Asks user if they want to explore raw data.
    """
    while True:
        ask_raw_data = str(input('Would you like to see individual trip data? Type yes or no?').lower().strip())
        if ask_raw_data not in ['yes', 'no']:
            print('Please type yes or no.')
        elif ask_raw_data == 'yes':
            start_loc = 0
            keep_asking = True
            while (keep_asking):
                print(df.iloc[start_loc:start_loc + 5])
                start_loc += 5
                more_rows = str(input('Display more data?').lower())
                if more_rows == 'no':
                    keep_asking = False
        else:
            break

def main():
    while True:
        city, month = get_filters()
        df = load_data(city, month)

        time_stats(df, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
