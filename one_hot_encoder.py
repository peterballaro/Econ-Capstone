import pandas as pd 

def one_hot_ecoding(columns:list, df:pd.DataFrame, drop=False):
    for col in columns:
        vals = df[col].unique()
        for val in vals:
            df[f'{col}_{val}'] = df[col].apply(lambda x: 1 if x == val  else 0)
    if drop:    
        df = df.drop(columns, axis=1)
    
    return df