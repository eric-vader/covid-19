# -*- coding: UTF-8 -*-
import os
import csv
import datetime
from collections import defaultdict
from collections import Counter

def csv_to_dicts(csv_name):
    with open(os.path.join("raw", "{}.csv".format(csv_name))) as csv_file:
        d_reader = csv.DictReader(csv_file)
        return list(d_reader)

continent_dict = {}
for r in csv_to_dicts("continent"):
    continent_dict[r['country']] = r['continent']

translate = {
    'Mainland China': 'China',
    'Hong Kong': 'Hong Kong, China',
    'Macau': 'Macau, China',
    'US': 'United States',
    'UK': 'United Kingdom',
    'Others': 'Cruise',
    'Iran (Islamic Republic of)': 'Iran',
    'Republic of Korea': 'South Korea',
    'Hong Kong SAR': 'Hong Kong, China',
    'Macao SAR': 'Macau, China',
    'Taipei and environs': 'Taiwan',
    'Viet Nam': 'Vietnam',
    'occupied Palestinian territory': 'Israel',
    'Republic of Moldova': 'Moldova',
    'Saint Martin': 'St. Martin',
    'Channel Islands': 'Bailiwick of Guernsey',
    'Holy See': 'Vatican City'
}

day_zero = datetime.datetime.strptime('01/22/2020', '%m/%d/%Y')
days = defaultdict(lambda: defaultdict(int))
for r in csv_to_dicts("covid_19_data"):

    last_update = None
    try:
        last_update = datetime.datetime.strptime(r['Last Update'], '%m/%d/%Y %H:%M')
    except ValueError as v:
        try:
            last_update = datetime.datetime.strptime(r['Last Update'], '%m/%d/%y %H:%M')
        except ValueError as v:
            last_update = datetime.datetime.strptime(r['Last Update'], '%Y-%m-%dT%H:%M:%S')

    c = r['Country/Region'].strip()
    c = translate[c] if c in translate else c
    
    delta_days = (last_update - day_zero).days
    
    confirmed = float(r['Confirmed'])
    deaths = float(r['Deaths'])
    recovered = float(r['Recovered'])

    days[delta_days][continent_dict[c]] += confirmed - deaths - recovered

with open('q4.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["days","Asia","Europe","Americas","Africa","Oceania"])
    writer.writeheader()

    for k, v in days.items():
        if 'Cruise' in v:
            del v['Cruise']
        d = {
            'days':k,
            **v
        }
        print(d)
        writer.writerow(d)