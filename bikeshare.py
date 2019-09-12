# Import section
import time
import pandas as pd
import numpy as np
import json

#Global Data types

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months =   ['all','january','february','march','april','may','june']

days   =   ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']

#Functions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
  
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid   inputs
    while True :
        city = str(input('\nChoose which city you want to explore : chicago , new york city , washington\n')).lower()
        
        try:
            if city not in CITY_DATA:
                print('\noops! the city you entered is not valid, choose a city from either chicago, newyork,washington:\n')
                continue
            else:
                break
        except ValueError as N:
            print("Exception occurred: {}".format(N))
                   
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('\nchoose a month you would like to explore("january to june") or choose \"all\"\n')).lower()
        
        try:
            if month not in months:
                print('\nsorry!, the month entered is not valid.please enter the month between january to june\n')
                continue
            else:
                break
        except ValueError as N:
            print('exception occurred:{}'.format(N))
  
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('\nCould you type one of the week day you want to analyze? or choose \"all\"\n')).lower()
       
        try:
            if day not in days:
                print('\nsorry!, The day entered is not valid.Please enter the day between monday to sunday\n')
                continue
            else:
                break
        except ValueError as d:
            print("Exception occurred: {}".format(d))
    
    
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

    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
      
    # filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month :',common_month)


    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week: ',common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station:',df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station:',common_end_station)
    
    # TO DO: display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_statistics(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    # display max travel time
    max_travel = df['Trip Duration'].max()
    print("Max travel time :", max_travel)

    print("Travel time for each user type:\n")
    
    # display the total trip duration for each user type
    group_by_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_trip):
        print("  {}: {}".format(group_by_trip.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_statistics(df):
    """ Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of user types:\n")
    user_counts = df['User Type'].value_counts()
    
    #print out the total numbers of user types 
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    
    print()

    if 'Gender' in df.columns:
        stats_gender(df)

    if 'Birth Year' in df.columns:
        stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    


def stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # iteratively print out the total numbers of genders 
    for index,gender_count in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))
    
    print()
    
    

def stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # To Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # calculating the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # calculating the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # calculating most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)

def table_statistics(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating Dataset Statistics...\n')
    
    # counts the number of missing values in the entire dataset
    missing_values = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city,missing_values))
    print('-'*40)

def display_user_data(df):
    """To Display the raw bikeshare data."""
    length_of_row = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for n in range(0, length_of_row, 5):
        
        ans = input('\nWould you like to explore a particular user trip data? choose \'yes\' or \'no\'\n ')
        if ans.lower() != 'yes':
            break
        
        # retrieve and convert data to json format and split each json row data 
        user_data = df.iloc[n: n + 5].to_json(orient='records', lines=True).split('\n')
        for row in user_data:
            #print each user data
            parse_row = json.loads(row)
            json_row = json.dumps(parse_row, indent=2)
            print(json_row)
    print('-'*40)


#main function the starting of the code

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
            
        time_statistics(df)
        station_statistics(df)
        trip_duration_statistics(df)
        user_statistics(df)
        table_statistics(df, city)
        display_user_data(df)
        #To restart the analysis
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
