# -*- coding: utf-8 -*-
"""
This program fetches continous futures data for Index and stock futures in NSE
using NSEpy package
It will create an excel file with the current and near month futures Close and
Last traded price. To know more how to use it check the below link

https://zerodha.com/varsity/chapter/calendar-spreads/

https://www.linkedin.com/pulse/download-continuous-index-stocks-futures-data-nse-using-arun-kamath/

@author: arun kamath
"""
######################################################
# Import section
import pandas as pd
from datetime import date, timedelta
from nsepy import get_history
from nsepy.derivatives import get_expiry_date

def fetch_data(sym,expiry,start_date):
    df_next_temp = pd.DataFrame()
    df_curr_temp = pd.DataFrame()
    df_combined_temp = pd.DataFrame()

    if sym == "NIFTY" or sym == "BANKNIFTY": #add OR cond. for additional index
        index_bool = True
    else:
        index_bool = False

    curr_fut_data = get_history(symbol=sym,
                        start=start_date,
                        end=expiry,
                        index=index_bool,
                        futures=True,
                        expiry_date=expiry)

    if expiry.month == 12:
        next_expiry = get_expiry_date(expiry.year+1,1)
    else:
        next_expiry = get_expiry_date(expiry.year,expiry.month+1)
    #bug in nse site fetching wrong expiry for march, 2018
    if next_expiry == date(2018,3,29):
        next_expiry = date(2018,3,28)

    next_fut_data = get_history(symbol=sym,
                        start=start_date,
                        end=expiry,
                        index=index_bool,
                        futures=True,
                        expiry_date=next_expiry)

    df_curr_temp = curr_fut_data[["Last","Close"]].copy()
    df_next_temp = next_fut_data[["Last","Close"]].copy()

    df_curr_temp.reset_index(drop=False, inplace=True)
    df_curr_temp['Date']= pd.to_datetime(df_curr_temp['Date'])
    df_curr_temp.set_index('Date', inplace=True)

    df_next_temp.reset_index(drop=False, inplace=True)
    df_next_temp['Date']= pd.to_datetime(df_next_temp['Date'])
    df_next_temp.set_index('Date',inplace=True)
    
    #you can add/remove columns here
    df_combined_temp["Curr Close"] = df_curr_temp["Close"]
    df_combined_temp["Curr Last"]  = df_curr_temp["Last"]
    df_combined_temp["Next Close"] = df_next_temp["Close"]
    df_combined_temp["Next Last"]  = df_next_temp["Last"]

    return df_combined_temp


def get_data():
    #try to keep the number of contracts less than 8 for optimal performance
    symbols = ["NIFTY","BANKNIFTY","SUNTV", "TATASTEEL","RELIANCE", "INFY"]
    month = [1,2,3,4,5,6,7,8,9,10,11,12]

    #add year at new year. Check in console whether old data is still fetched
    #if not fetched remove it and make suitable logic changes in line 95
    year = [2016, 2017, 2018]

    #if you have already run this program before,change the filename below to
    # avoid overwriting
    filename = "calendar_spread1.xlsx"

    now_d = date.today()
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    for sym in symbols:
        df_combined = pd.DataFrame()
        for yy in year:
            for mm in month:
                expiry = get_expiry_date(year=yy, month=mm)

                if expiry == date(2016,1,28):
                    start_date = expiry + timedelta(days=1)

                else:
                    #bug in nse site resulting in wrong expiry for march, 2018
                    #can be removed if fixed by nse
                    # run get_expiry_date(2018, 3) in console to verify
                    if expiry == date(2018,3,29):
                        expiry = date(2018,3,28)
                    df_combined = df_combined.append(fetch_data(sym,expiry,
                                                                start_date))
                    start_date = expiry + timedelta(days=1)
                    if start_date > now_d:
                        df_combined.to_excel(writer,sym)
                        break
    writer.save()

def main():

    get_data()

if __name__ == '__main__':

    main()
