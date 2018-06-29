# -*- coding: utf-8 -*-
"""
This program checks which day of the week is most profitable in order to do 
weekly SIP.

Works for NSE only

It assumes we buy 1 stock or 1 Index on close of the day everyday.

We fetch data from 1/1/2000 using nsepy. Am not sure whether the stock data we
receive is adjusted for splits and bonuses.

@author: arkamath
"""
# Import section
import pandas as pd
from datetime import date
from nsepy import get_history
import sys
import matplotlib.pyplot as plt
 
def draw_graph(df_returns):
    
    #Drop Saturday and Sunday trades value(Probably Mahurat trading)
    df_returns.drop(df_returns.index[5],inplace=True)
    df_returns.drop(df_returns.index[5],inplace=True)  
    df_returns.reset_index(drop=True, inplace=True)
    df_returns.set_index('Weekday', inplace=True)
    #Normalise values
    df_returns = (df_returns - df_returns.mean())/df_returns.std()
              
    ax = df_returns[['Units Purchased']].plot(kind='bar', 
                   title ="Units purchased", 
                   figsize=(15, 10), legend=True, fontsize=12,color='#C0FF44')
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Quantity/No of trades", fontsize=12)
    plt.show()
  
    ax = df_returns[['Total Investment']].plot(kind='bar', 
                   title ='Total Investment', 
                   figsize=(15, 10), legend=True, fontsize=12,color='#FF4455')
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Total investment till date", fontsize=12)    
    plt.show()
    
    ax = df_returns[['Profit Today']].plot(kind='bar', 
                   title ="Profit Today", 
                   figsize=(15, 10), legend=True, fontsize=12,color='#C0FF44')
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Profit as of today", fontsize=12)    
    plt.show()
    
    ax = df_returns[['Profit %']].plot(kind='bar', 
                   title ="Profit %", 
                   figsize=(15, 10), legend=True, fontsize=12,color='#AA44FF')
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Profit % as of today", fontsize=12)    
    plt.show()
    
    ax = df_returns[['Cost per Unit']].plot(kind='bar', 
                   title ="Cost per Unit", 
                   figsize=(15, 10), legend=True, fontsize=12,color='#FF44A1')
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Per unit cost", fontsize=12)    
    plt.show()  
    
    ax = df_returns[['Profit per Unit']].plot(kind='bar', 
                   title ="Profit per Unit", 
                   figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Day of the Week", fontsize=12)
    ax.set_ylabel("Per unit profit", fontsize=12)    
    plt.show()  
    
def calculate_returns(df_returns,symbol):
    df_returns = get_data(symbol.upper())
    df_aggregate = pd.DataFrame()

    df_aggregate = df_returns.groupby('Wday').count()
    df_aggregate.rename(columns={'Close':'Units Purchased'},inplace=True) 
    df_aggregate['Total Investment'] = df_returns.groupby('Wday').sum()
    
    current_value = df_returns.Close.iat[-1]
    df_aggregate['Profit Today'] = (df_aggregate['Units Purchased'] * \
    current_value) - df_aggregate['Total Investment']
    
    df_aggregate['Profit %'] = ((df_aggregate['Profit Today'] - \
    df_aggregate['Total Investment'])/ df_aggregate['Total Investment'] )*100
    
    df_aggregate['Cost per Unit'] = df_aggregate['Total Investment']/ \
    df_aggregate['Units Purchased']    
        
    df_aggregate['Profit per Unit'] = df_aggregate['Profit Today']/ \
    df_aggregate['Units Purchased']
    
    days = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
    df_aggregate.reset_index(drop=False, inplace=True)
    df_aggregate['Weekday'] = df_aggregate['Wday'].apply(lambda x: days[x])
    df_aggregate.set_index('Wday', inplace=True)
    
    
    return df_aggregate
    
def get_data(symbol):
    df_data = pd.DataFrame()
    
    if "NIFTY" not in symbol and "ETF" not in symbol:
        index_bool = False
    else:
        index_bool = True   
    
    historic_data = get_history(symbol=symbol,
                            start=date(2000,1,1),
                            end=date(2018,6,29),
                            index=index_bool)
    
    if historic_data.empty:
        print("Data not fetched from NSE. Try after some time")
        exit(2)
    df_data = historic_data[:].copy() 
    
    df_data.reset_index(drop=False, inplace=True)
    df_data['Date']= pd.to_datetime(df_data['Date'])
    df_data.set_index('Date', inplace=True)
    
    df_data['Wday'] = df_data.index.weekday
    df_data.reset_index(drop=False, inplace=True)
    df_data = df_data.drop(columns = ['Date','Open', 'High','Low', 'Volume', 
                                      'Turnover'])
    if index_bool == False:
        df_data = df_data.drop(columns = ['Symbol','Series', 'Prev Close',
                                          'Last', 'VWAP','Trades',
                                          '%Deliverble',
                                          'Deliverable Volume',
                                      ])
    return df_data
    
def main():
    if len(sys.argv) < 2:
        print ("execute in cmd like 'python weedayreturns.py NIFTY'")
        exit(1)    
    symbol = sys.argv[1]    
#    symbol = 'NIFTY'
    df_returns = pd.DataFrame()
        
    df_returns = calculate_returns(df_returns,symbol)
    draw_graph(df_returns)
    
if __name__ == '__main__':

    main()
