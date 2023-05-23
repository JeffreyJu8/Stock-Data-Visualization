# ITP 216 Homework 13
# Fall 2022
import statistics

import pandas as pd
import matplotlib.pyplot as plt


def main():
    # reading in the dataset
    df = pd.read_csv("csv_files/tesla.csv")

    # removing rows of data where the observed temp is null
    df = df[df["Open"].notnull()]
    # df = df[df['TMAX'].notnull()]
    # df = df[df['TMIN'].notnull()]

    # df['TMID'] = df['TMAX'] + df['TMIN']
    # df['TMID'] = df['TMAX'] + df['TMIN'].div(2)


    # making a column for year: allows us to easily get the last 10 years
    df["YEAR"] = df["Date"].str[0:4]
    years_list = df["YEAR"].unique()
    #print(len(years_list))
    # making a column for month: allows us to group by month
    df["MONTH_DAY"] = df["Date"].str[-5:]
    df = df[df['MONTH_DAY'] != '02-29']  # drop leap years
    month_days_list = list(df["MONTH_DAY"].unique())

    df.sort_values(inplace=True, by='MONTH_DAY')
    print(df[['Date', 'YEAR', 'MONTH_DAY', 'Open']])

    # list of months to label the x-axis of both graphs
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, ax = plt.subplots(2, 1)


    #graph 1

    # make the xtick list from a range from 0 to 365 and step by 31 days per month
    xtickList = list(range(0, 13, 1))
    # to avoid warnings, use axis.xaxis.set_xticks() and .set_ticklabels()
    ax[0].xaxis.set_ticks(xtickList)
    # you can use month_list aove for x labels
    ax[0].xaxis.set_ticklabels(years_list)
    ax[0].set(title="Most recent 10 years",
              xlabel="Month", ylabel="Open")
    #color_list = ["blue", "#FF00FF", "green", "orange", "pink"]
    grouped_years = df.groupby("YEAR")


    index = 0
    for year in years_list:
        df_group = grouped_years.get_group(year)
        ax[0].plot(df_group["Date"], df_group["Open"],
                   label=year)


    ax[0].grid(which='major', color='#999999', alpha=0.2)
    ax[0].legend()


    df = pd.read_csv("csv_files/AMZN.csv")

    # removing rows of data where the observed temp is null
    df = df[df["Open"].notnull()]
    # df = df[df['TMAX'].notnull()]
    # df = df[df['TMIN'].notnull()]

    # df['TMID'] = df['TMAX'] + df['TMIN']
    # df['TMID'] = df['TMAX'] + df['TMIN'].div(2)

    # making a column for year: allows us to easily get the last 10 years
    df["YEAR"] = df["Date"].str[0:4]
    years_list = df["YEAR"].unique()
    #print(len(years_list))
    # making a column for month: allows us to group by month
    df["MONTH_DAY"] = df["Date"].str[-5:]
    df = df[df['MONTH_DAY'] != '02-29']  # drop leap years
    month_days_list = list(df["MONTH_DAY"].unique())

    df.sort_values(inplace=True, by='MONTH_DAY')
    print(df[['Date', 'YEAR', 'MONTH_DAY', 'Open']])

    # list of months to label the x-axis of both graphs
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # year_list_recent = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]

    fig, ax = plt.subplots(2, 1)

    # graph 1

    # make the xtick list from a range from 0 to 365 and step by 31 days per month
    xtickList = list(range(0, 26, 1))
    # to avoid warnings, use axis.xaxis.set_xticks() and .set_ticklabels()
    ax[0].xaxis.set_ticks(xtickList)
    # use year_list aove for x labels
    ax[0].xaxis.set_ticklabels(years_list)

    ax[0].set(title="Most recent 10 years",
              xlabel="Year", ylabel="Open")
    # color_list = ["blue", "#FF00FF", "green", "orange", "pink"]
    grouped_years = df.groupby("YEAR")

    index = 0
    for year in years_list:
        df_group = grouped_years.get_group(year)
        ax[1].plot(df_group["Date"], df_group["Open"],
                   label=year)
        index += 1

    ax[1].grid(which='major', color='#999999', alpha=0.2)
    ax[1].legend()


    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
