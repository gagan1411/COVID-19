# COVID-19

This project was made by me to track the total number of cases at the end of each day and the new cases reported on each day.

This script uses a COVID19-India API which is an open source and crowdsourced database of COVID-19 cases of India. Information for each day is retrieved through the API in json file and processed in the Python script. The links to the API page and the json file has been provided at the end of this file.

The data from the json file is stored locally in SQLite database for future reference.

Data was cleaned and handled using the Pandas library. Dates were converted from strings to datetime format using the datetime library.
Graphs were plotted using matplotlib library and additional functionality has been added to the graphs.

In the figure for total cases for each day(figure 1), clicking on the figure tells us total number of cases at the end of the corresponding day depending on the position of cursor at the time of click.

In the figure for new cases reported each day(figure 2), clicking on the figure tells us the total number of new cases that were reported for the given day depending on the position of cursor at the time of click.

LINKS

COVID19-India API : https://api.covid19india.org/

json file for daily data : https://api.covid19india.org/data.json
