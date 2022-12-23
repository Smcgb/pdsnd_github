import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv',
              'dc': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    while city.lower() not in CITY_DATA:
        print('Please select a city from the following list: Chicago, New York City, Washington')
        city = input()

    #  get user input for month (all, january, february, ... , june)
    list_of_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']

    while month.lower() not in list_of_months:
        print('What month would you like to filter by? Please enter a month (NON-ABBREVIATED) from January to June or enter "all" to apply no month filter.')
        month = input()
    
    #  get user input for day of week (all, monday, tuesday, ... sunday)
    LIST_OF_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    while day.lower() not in LIST_OF_DAYS:
        print('What day of the week would you like to filter by? Please enter a day of the week (NON-ABBREVIATED) or enter "all" to apply no day filter.')
        day = input()


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
    # load city data into a dataframe based on city name input from get_filters() return

    df = pd.read_csv(CITY_DATA[city.lower()])

    # Create time datetime attribute for filtering
    df['Start Time'] = pd.to_datetime(df['Start Time']) 

    # use extra datetime functions to allow easier matching of input
    df['month'] = df['Start Time'].dt.month_name()

    df['day_of_week'] = df['Start Time'].dt.day_name()

    df['hour'] = df['Start Time'].dt.hour

    # capitalize for exact pandas matching on DOW and MOY
    month = month.capitalize()
    day = day.capitalize()


    
    if month.lower() != 'all':
        df = df[df['month'] == month]

    if day.lower() != 'all':
        df = df[df['day_of_week'] == day]


    return df

def preview_data(df):
    '''
    Shows 5 lines starting from index 0 from the reference dataframe 
    if the user inputs yes. Uses a while loop to iterate over next 5 lines
    until user enters terminate no command.
    '''
    
    start, fin = 0, 5

    while True:
        next_five = input('\nWould you like to see the first 5 lines of the data? Enter yes or no.\n')
        if next_five.lower() == 'yes':
            print(df.iloc[start:fin])
            start += 5
            fin += 5
        elif next_five.lower() == 'no':
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    #most popular month
    pop_month = df['month'].mode()[0]

    print(f"Most Frequent Month and number of trips:\n \
    {pop_month}: {len(df[df['month'] == pop_month])}\n")

    #popular day
    pop_day = df['day_of_week'].mode()[0]

    print(f"Most Frequent Day and number of trips:\n \
    {pop_day}: {len(df[df['day_of_week'] == pop_day])}\n")

    #popular hour
    pop_hour = df['hour'].mode()[0]

    print(f"Most Frequent hour and number of  trips:\n \
    {pop_hour}: {len(df[df['hour'] == pop_hour])}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print(f"Most Departure station and number of trips:\n \
    {pop_start}: {len(df[df['Start Station'] == pop_start])}\n")
    # display most commonly used start station


    #  display most commonly used start station
    pop_start = df['Start Station'].mode()[0]

    print(f"Most Departure station and number of trips:\n \
    {pop_start}: {len(df[df['Start Station'] == pop_start])}\n")

    # display most commonly used end station
    pop_end = df['End Station'].mode()[0]

    print(f"Most Frequent arrival station and number of trips:\n \
    {pop_end}: {len(df[df['End Station'] == pop_end])}\n")

    #  display most commonly used end station
    pop_end = df['End Station'].mode()[0]

    print(f"Most Frequent arrival station and number of trips:\n \
    {pop_end}: {len(df[df['End Station'] == pop_end])}\n")

    # display most frequent combination of start station and end station trip
    pop_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print(f"The most popular trip was from {pop_combo[0]} to {pop_combo[1]} with {len(df[(df['Start Station'] == pop_combo[0]) & (df['End Station'] == pop_combo[1])])} trips")
    #  display most frequent combination of start station and end station trip

    pop_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print(f"The most popular trip was from {pop_combo[0]} to {pop_combo[1]} with {len(df[(df['Start Station'] == pop_combo[0]) & (df['End Station'] == pop_combo[1])])} trips")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def convert(seconds):
    '''
    Uses divmod to make time reporting in seconds
    reflect normal time reporting of h/m/s
    '''
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return f'{hour}:{min}:{sec}'


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time

    sum_seconds = df['Trip Duration'].sum()

    converted_ttl_time = convert(sum_seconds)
    
    print(f"Total Travel Time: {converted_ttl_time} h/m/s")


    #  display mean travel time

    mean_seconds = df['Trip Duration'].mean()

    converted_avg_time = convert(mean_seconds)

    print(f"Average Travel Time: {converted_avg_time} h/m/s")

    #  display median travel time

    median_seconds = df['Trip Duration'].median()

    converted_med_time = convert(median_seconds)

    print(f"Median Travel Time: {converted_med_time} h/m/s")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User Type Data

    if 'User Type' in df.columns:
        print(f"User Type\n{df['User Type'].value_counts().to_string()}\n")
    else:
        print("User type data not found")

    # Gender Data

    if "Gender" in df.columns:
        print(f"Gender\n{df['Gender'].value_counts().to_string()}\n")
    else:
        print("Gender data not found")

    # Birth Year Data

    if 'Birth Year' in df.columns:
         print(f"Earliest Birth Year {df['Birth Year'].min()}\n \
                    Most Recent Birth Year {df['Birth Year'].max()} \n \
                    Most common Birth Year {df['Birth Year'].mode()}")
    else:
        print("Birth Year data not found")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        preview_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
