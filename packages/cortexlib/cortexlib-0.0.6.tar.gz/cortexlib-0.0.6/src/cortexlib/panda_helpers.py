import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

def add_blank_column(dataframe,column_name):
    dataframe[f'{column_name}'] = ''
    return dataframe

def add_5(num):
    return num + 5