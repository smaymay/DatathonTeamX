import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import csv

__author__ = 'S. May'

clusterfile = sys.argv[1]

clusters = open(clusterfile).read().split('\n')

results = open('clusters.csv', 'w+')
results_writer = csv.writer(results)

for row in clusters:
	if len(row) >1: 
		if 'CLUSTER' in row: 
			results_row = [row]
		else:
			regions = row.split()
			for region in regions:
				r_list = region.split('_')
				rate = r_list[len(r_list)-1]
				results_row.append(rate)
			results_writer.writerow(results_row)




