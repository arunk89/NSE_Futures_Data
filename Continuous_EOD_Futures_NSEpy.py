# Import section
import pandas as pd
from datetime import date, timedelta
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
import sys

def fetch_data(contract, expiry, start_date):
    
    df_futures = pd.DataFrame()
    
    #add OR cond. for additional index    
    if contract == "NIFTY" or contract == "BANKNIFTY":
        index_bool = True
    else:
        index_bool = False
    
    curr_fut_data = get_history(symbol=contract,
                        start=start_date,
                        end=expiry,
                        index=index_bool,
                        futures=True,
                        expiry_date=expiry)
    
    df_futures = curr_fut_data[:].copy() 
    
    df_futures.reset_index(drop=False, inplace=True)
    df_futures['Date']= pd.to_datetime(df_futures['Date'])
    df_futures.set_index('Date', inplace=True)
    
    return df_futures
        
    
def get_data(contract):
    df_combined = pd.DataFrame()
    month = [1,2,3,4,5,6,7,8,9,10,11,12]

    #add year at new year. Check in console whether old data is still fetched
    #if not fetched remove it and make suitable logic changes in line 59
    year = [2016, 2017, 2018]

    #if you have already run this program before,change the filename below to
    # avoid overwriting
    filename = "_calendar_spread.xlsx"
    filename = contract+filename

    now_d = date.today()
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
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
                df_combined = df_combined.append(fetch_data(contract,expiry,
                                                        start_date))
                start_date = expiry + timedelta(days=1)
                if start_date > now_d:
                    df_combined.to_excel(writer,contract)
                    break
    writer.save()
            
        
def main():
    if len(sys.argv) < 2:
        print ("execute in cmd like 'python continous_data.py NIFTY'")
        sys.exit(1)    
    contract = sys.argv[1]
    
#    contract = 'NIFTY'
    get_data(contract.upper())

if __name__ == '__main__':

    main()
