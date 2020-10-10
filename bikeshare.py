import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months = ['january','february','march','april','may','june']
Days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filter_city():
    """
    Ask user the city they want to explore.
    Returns:
        (str) city - name of the city to analyze
    """
    #construct a list for the cities we want to study
    list_cities = []
    number_cities = 0

    for city in CITY_DATA:
        list_cities.append(city)
        number_cities += 1
        print(' {0:20}. {1}'.format(number_cities, city.title()))

    # the user will introudce a number in order to recognize which city to analize
    while True:
        try:
            city_number = int(input("\n Please introduce a number for the city between (1 - {}):  ".format(len(list_cities))))
        except:
            continue

        if city_number in range (1, len(list_cities)+1):
            break

    # convert the number choosen into a city name
    city_name = list_cities[city_number - 1]
    return city_name

def get_filter_month():
    """
    Ask user the month they want to explore. Choose a month or all.
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    while True:
        try:
            month = input("Enter the month with a number Ex. January=1, February=2 or all: ")
        except:
            print("        ---->>  Valid input:  1 - 6, all")
            continue

        if month == 'all':
            month = 'all'
            break
        elif month in {'1','2','3','4','5','6'}:
             month = Months[int(month)-1]
             break
        else:
            continue
    return month

def get_filter_day():
    """
    Ask user the day they want to explore. Choose a day or all.
    Return:
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True:
        try:
            day = input("Enter the day with a number Ex. Monday=1, Tuesday=2 or all: ")
        except:
            print("        ---->>  Valid input:  1 - 7, all")
            continue

        if day == 'all':
            day = 'all'
            break
        elif day in {'1','2','3','4','5','6','7'}:
             day = Days[int(day)-1]
             break
        else:
            continue
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_filter_city()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_filter_month()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter_day()

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
    df ['Start Time'] = pd.to_datetime(df['Start Time'])
    df ['month'] = df['Start Time'].dt.month
    df ['day_week'] = df['Start Time'].dt.dayofweek
    df ['hour'] = df['Start Time'].dt.hour

    total_rides = len(df)
    filter_rides = total_rides

    #apply the filters by month or day when specified by the user
    if month != 'all':
        month_i = Months.index(month)+1
        df = df[df.month == month_i]
        month = month.title

    if day != 'all':
        day_i = Days.index(day)
        df = df[df.day_week == day_i]
        day = day.title()

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month = Months[df['month'].mode()[0]-1].title()
    print('Most common month:', month)

    # TO DO: display the most common day of week
    common_day = df['day_week'].mode()[0]
    common_day = Days[common_day].title()
    print('Most common day:', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    filter_rides = len(df)

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_trips = df['Start Station'].value_counts()[start_station]
    print ('Most commonly used start sattion:',start_station)
    print ('{0:30}{1}/{2} trips'.format(' ', start_trips, filter_rides))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_trips = df['End Station'].value_counts()[end_station]
    print ('Most commonly used end station:',end_station)
    print ('{0:30}{1}/{2} trips'.format(' ', end_trips, filter_rides))

    # TO DO: display most frequent combination of start station and end station trip
    df_start_end_station = df.groupby(['Start Station','End Station'])
    count_trip = df_start_end_station['Trip Duration'].count().max()
    most_frequent = df_start_end_station['Trip Duration'].count().idxmax()
    print ('Most frequent trip in between {},{}'.format(most_frequent[0],most_frequent[1]))
    print ('{0:30}{1} trips'.format(' ', most_frequent))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time = int(df['Trip Duration'].sum())
    print('The Total travel time was: ', travel_time, 'seconds')


    # TO DO: display mean travel time
    mean_travel = int(df['Trip Duration'].mean())
    print('The mean travel time was: ', mean_travel, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in range(len(user_types)):
        j = user_types[i]
        user_type = user_types.index[i]
        print ('    {0:21}'.format((user_type + ':')), j)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        for i in range(len(genders)):
            j = genders[i]
            gender = genders.index[i]
            print ('    {0:21}'.format((gender + ':')), j)

     # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Year of Birth...')
        print('Earliest: ', int(df['Birth Year'].min()))
        print('Most recent: ', int(df['Birth Year'].max()))
        print('Most common: ', int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Display raw data upon request
    """
    raw_data = 0
    while True:
        ask = input("\n Display raw data? Enter yes or no. ").lower()
        if ask == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            ask_two = input("Display more data? Yes or No ").lower()
            if ask_two == 'yes':
                raw_data += 5
                print(df.iloc[raw_data : raw_data + 5])
            if ask_two == 'no':
                break
        elif ask == 'no':
            return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
