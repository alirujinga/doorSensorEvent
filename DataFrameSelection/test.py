from datetime import datetime as dt
import pandas as pd
import numpy as np
def transferStrToDate(df):
    line = df.shape[0]
    for i in range(0, line):
        Date = dt.strptime(df["date"][i], "%m/%d/%Y")
        df._set_value(i,'date',Date)
        print(type(df["date"][i]))
    return df


technologies = {
    'date':["1/23/2023","1/23/2023"],
    'Fee' :[20000,25000],
    'Duration':['30days','40days'],
    'Discount':[1000,2300],
    'Tutor':['Michel','Sam']
              }
df = pd.DataFrame(technologies)

df = transferStrToDate(df)
strtime = "1/23/2023 9:55:08"
times = dt.strptime(strtime, "%m/%d/%Y %H:%M:%S")
strtime = ''
time = dt.strptime('9:55:08',"%H:%M:%S")
print(time)

def shortEvent(df):
    line = df.shape[0]
    for i in range(0, line):
        event =df["Duration"][i]
        print(event)
        # df._set_value(i, 'date', Date)
    return df


def dropRow():
    df = pd.DataFrame(np.arange(12).reshape(3, 4),
                      columns=['A', 'B', 'C', 'D'])
    print(df)
    df = df.drop(df.index[1])
    print(df.iloc[1]["A"])
    print(type(df.iloc[1]["A"]))

shortEvent(df)
dropRow()
print(dt.now())
a = ''
print(len(a))

d = {'a': 1, 'b': 2, 'c': 3}
ser = pd.Series(data=d, index=['a', 'b', 'c'])
for i in ser.keys():
    print(i)
path = "//server3/Users/administrator.ARXTRON/Documents/Door Controller/events.csv"
a = pd.read_csv(path)
print(a)