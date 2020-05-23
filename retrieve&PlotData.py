# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:34:29 2020

@author: HP USER
"""


import urllib.request, urllib.error, urllib.parse
import json
import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

#retrieve json file and decode it
jsonFile = urllib.request.urlopen('https://api.covid19india.org/data.json').read()
data = json.loads(jsonFile)

conn = sqlite3.connect('Covid19Data.sqlite')
cur = conn.cursor()

#create a table in database if the table does not exists
cur.executescript('''
            CREATE TABLE IF NOT EXISTS dailyCases(
                dailyConfirmed INTEGER NOT NULL, 
                dailyDeceased INTEGER NOT NULL, 
                dailyRecovered INTEGER NOT NULL,
                date TEXT NOT NULL UNIQUE,
                totalConfirmed INTEGER NOT NULL,
                totalDeceased INTEGER NOT NULL,
                totalRecovered INTEGER NOT NULL
            );''')

#%%

#update the data in database for each date
for daily in data['cases_time_series']:
    dailyData = list(daily.values())
    cur.execute('''SELECT * FROM dailyCases WHERE date=?''', (dailyData[3], ))
    result = cur.fetchone()
    if result is None:
        cur.execute('''
                INSERT INTO dailyCases (dailyConfirmed, dailyDeceased, dailyRecovered, date,
                totalConfirmed, totalDeceased, totalRecovered) VALUES ( ?, ?, ?, ?, ?, ?, ?)''', 
                (int(dailyData[0]), int(dailyData[1]), int(dailyData[2]), dailyData[3],
                 int(dailyData[4]), int(dailyData[5]), int(dailyData[6])))
    elif result[4] < int(dailyData[4]):
        cur.execute('''
                    UPDATE dailyCases
                    SET totalConfirmed=?
                    WHERE date=?''',
                    (int(dailyData[4]), dailyData[3]))
    conn.commit()


#%%
total = pd.read_sql('SELECT * FROM dailyCases', conn)

#convert date to python datetime type object
def fun(x):
    return datetime.strptime(x+str((datetime.today().year)), '%d %B %Y')
total['date'] = total['date'].apply(fun)

#plot figure for total cases for each day
fig = plt.figure()

plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b'))
plt.plot(total['date'], total['totalConfirmed'], '-o', ms=1)
plt.title('Total cases in India for each day')
plt.xlabel('Dates', fontsize=12)
plt.ylabel('Total cases', labelpad=0.1, fontsize=12)

def slide(event):
    date = int(event.xdata)
    print(event.xdata)
    dateIndex = date - dateLoc[0]+2
    date = total['date'].iloc[dateIndex]
    strDate = date.strftime('%d %b')
    #text for displaying the total cases for each day
    str = 'Total cases on {} were {}'.format(strDate, total['totalConfirmed'].iloc[dateIndex])
    plt.cla()
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b'))
    plt.plot(total['date'], total['totalConfirmed'], '-o', ms=1)
    plt.text(x=dateLoc[0], y=50000, s=str)
    plt.title('Total cases in India for each day')
    plt.xlabel('Dates', fontsize=12)
    plt.ylabel('Total cases', labelpad=0.1, fontsize=12)
    plt.draw()

dateLoc = (plt.gca().xaxis.get_majorticklocs())
dateLoc = dateLoc.astype(np.int64)
fig.canvas.mpl_connect('button_press_event', slide)

#plot the figure for new cases reported for each day
fig2 = plt.figure()
fig2.set_figheight(9)
fig2.set_figwidth(16)
fig2.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b'))
plt.bar(total['date'], total['dailyConfirmed'], width=0.8, alpha=0.8)
plt.plot(total['date'], total['dailyConfirmed'], c='red', alpha=0.8)
plt.title('New cases reported in India for each day')
plt.xlabel('Dates', fontsize=12)
plt.ylabel('New cases reported', labelpad=10, fontsize=12)

def slide2(event):
    date = int(round(event.xdata))
    print(event.xdata)
    dateIndex = date - dateLoc[0]+2
    date = total['date'].iloc[dateIndex]
    strDate = date.strftime('%d %b')
#    print(plt.gcf().texts())
    str = 'Total cases reported on {} were {}'.format(strDate, total['dailyConfirmed'].iloc[dateIndex])
    plt.cla()
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b'))
    plt.bar(total['date'], total['dailyConfirmed'], alpha=0.8)
    plt.plot(total['date'], total['dailyConfirmed'], c='red', alpha=0.8)
    plt.annotate(xy=(event.xdata, total['dailyConfirmed'].iloc[dateIndex]),
                     xytext=(dateLoc[0], 4000), s=str,
                     arrowprops={'arrowstyle':'->'})
    plt.title('New cases reported in India for each day')
    plt.xlabel('Dates', fontsize=12)
    plt.ylabel('New cases reported', fontsize=12, labelpad=10)
    plt.draw()

fig2.canvas.mpl_connect('button_press_event', slide2)

plt.show()
conn.close()
