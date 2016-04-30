import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import csv

__author__ = 'S. May'

# name / path to file containing livability data
liv_file = sys.argv[1]
# name / path to file containing diabetes data
diab_file = sys.argv[2]

with open(liv_file, 'r') as f:
	f_reader = csv.reader(f)
	liv_list = list(f_reader)

with open(diab_file, 'r') as f:
	f_reader = csv.reader(f)
	diab_list = list(f_reader)

liv_headers = liv_list[0]
del liv_list[0]

diab_headers = diab_list[0]
del diab_list[0]

county_index_liv = liv_headers.index('County')
county_index_diab = diab_headers.index('County')

new_csv = open('mergedfile.csv', 'w+')
w_csv = csv.writer(new_csv)

w_csv.writerow(liv_headers + diab_headers)

for liv_row in liv_list: 
	county = liv_row[county_index_liv].lower()
	i = 0
	while county not in diab_list[i][county_index_diab].lower() and i < len(diab_list)-1:
		i += 1
	if county in diab_list[i][county_index_diab].lower():
		w_csv.writerow(liv_row + diab_list[i])




