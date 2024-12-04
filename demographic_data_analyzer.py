import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(['race'])['race'].count().sort_values(ascending=False).values

    # What is the average age of men?
    average_age_men = round(df.groupby(['sex'])['age'].mean().Male, 1)

    # What is the percentage of people who have a Bachelor's degree?
    dfBCount = (df.groupby(['education'])['education'].count())['Bachelors']
    dfTCount = len(df.education)
    percentage_bachelors = round((dfBCount/dfTCount) * 100.0, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    dfedu = df.groupby(['education', 'salary']).size()
    df50kM = dfedu['Bachelors']['>50K'] + dfedu['Masters']['>50K'] + dfedu['Doctorate']['>50K']
    dftotal = dfedu['Bachelors'] + dfedu['Masters'] + dfedu['Doctorate']
    dft = dftotal['>50K'] + dftotal['<=50K']

    df49K = df.loc[(~(df['education'].isin(['Bachelors', 'Masters', 'Doctorate']))) & (df['salary'] == '>50K'), 'salary'].count()
    df49Ktotal = df.loc[~(df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])), 'salary'].count()

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round((df50kM/dft * 100), 1)
    lower_education = round(df49K/df49Ktotal * 100, 1)

    # percentage with salary >50K
    higher_education_rich = higher_education
    lower_education_rich = lower_education

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = (df['hours-per-week'].min())

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    K50 = df.loc[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K'), 'salary'].count()
    tot = df.loc[df['hours-per-week'] == min_work_hours, 'salary'].count()

    num_min_workers = round((K50/tot * 100),1)

    rich_percentage = num_min_workers

    # What country has the highest percentage of people that earn >50K?
    dfcountry = (df.loc[df['salary'] == '>50K']['native-country'].value_counts()/ df['native-country'].value_counts() * 100).sort_values(ascending=False).fillna(0).index[0]

    dfcountryearnings = df.loc[(df['native-country'] == dfcountry) & (df['salary'] == '>50K'), 'salary'].count() / df.loc[(df['native-country'] == dfcountry), 'salary'].count()
    highest_earning_country = dfcountry
    highest_earning_country_percentage = round(dfcountryearnings * 100, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df.loc[(df['salary'] == '>50K') & (df['native-country'] == 'India') , 'occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
