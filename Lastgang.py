# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import datetime


def combinedatetime(series):
    return datetime.datetime.combine(series[0], series[1])

os.chdir('/Users/ulfschnabel/Dropbox/Kurt')

excelfile = pd.read_excel('testlauf.xlsx')

lastgang = pd.DataFrame(excelfile.iloc[1:, 5])

lastgang.index = excelfile.iloc[1:, 3:5].apply(combinedatetime, axis = 1)
lastgang.loc[:, 1] = lastgang.index 
lastgang.loc[:, 2] = lastgang.loc[:, 1].dt.dayofweek
