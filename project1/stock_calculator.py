from pathlib import Path
import numpy as np
import pandas as pd

PATH_SOURCE = Path(__file__).parent
PATH_TRANS = PATH_SOURCE / 'invent_trans'
PATH_STOCK = PATH_SOURCE / 'stock'
PATH_OUTPUT = PATH_SOURCE / 'results'
PATH_OUTPUT.mkdir(parents=True, exist_ok=True)

def calculate_stocks(df: pd.DataFrame,date:np.datetime64):
    stocks_df = df[df['trans_date'] <=date]
    stocks_df = stocks_df.groupby(['item_id', 'location_id']).agg({
        'qty': 'sum',
        'cost_amount':'sum'
        }).reset_index()
    stocks_df['qty'] = stocks_df['qty'].round(0)
    stocks_df['cost_amount'] = stocks_df['cost_amount'].round(2)    
    stocks_df.insert(2,column='trans_date',value= date.strftime('%Y-%m-%d'))
    stocks_df.to_csv(PATH_OUTPUT / f"stock_{date.strftime('%Y_%m_%d')}.csv",sep=";",index=False)
    print(f"file with name: stock_{date.strftime('%Y_%m_%d')}.csv has been added to {PATH_OUTPUT}")
    return stocks_df      
   

def main(run_full_range:bool = False) -> None:
    stock_file = next(PATH_STOCK.glob("*.csv"),None)
    if stock_file is not None:
        stocks = pd.DataFrame(pd.read_csv(stock_file,sep=';'))
    else:
        print(f'Please, provide a stock file to {PATH_STOCK}')
        return
    dfs = []
    for file in PATH_TRANS.glob("*.csv"):
        dfs.append(pd.read_csv(file,sep=';'))
    if dfs != []:
        df = pd.concat(dfs,ignore_index=True)
        combined = pd.concat([stocks,df],ignore_index=True)
        combined['trans_date'] = pd.to_datetime(combined['trans_date'])
    else:
        print('There is no files provided')
        return

   
    
    if run_full_range:
        date_range = pd.date_range(start=combined['trans_date'].min(),end=combined['trans_date'].max())
        for date in date_range:
            stocks_day_csv = calculate_stocks(df=combined,date=date)
    else:
        target_date = pd.to_datetime('2025-07-31')
        calculate_stocks(df=combined,date=target_date)

if __name__ == "__main__" :
    try:
        main()
    except Exception as e:
        print(f'Oops... Something wrong with an exception:{e}')
