import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import csv
import argparse

from scipy.stats.stats import pearsonr

__author__ = 'S. May'

"""Preps livability data to run K-Means cluster analysis by making
two files: livability.vecs and livability.labels, which will be 
arguments to cluster.py.

If the argument corr==True, also computes correlations
between each factor and diabetes rates, and saves in 
correlations.csv
"""

def get_filelist(f):
    with open(f, 'r+') as f_open:
        f_reader = csv.reader(f_open)
        return list(f_reader)

def get_factor_indices(headers, factors):
    factor_indices = []
    for factor in factors:
        factor_indices.append(headers.index(factor))
    return factor_indices

def write_output(f_list, headers, corr):
    
    factor_indices = get_factor_indices(headers, args.factors)
    label_index = headers.index('City')
    diabetes_index = headers.index('2012 percent')
    
    len_valid_row = len(headers)
    
    if corr == True:
        factor_vectors = [[] for factor in factors]
        diab_vector = []
    
    vec_output = open('livability.vecs', 'w+')
    label_output = open('livability.labels', 'w+')
    fac_output = open('factors.txt', 'w+')
    
    # write file containing list of factors used in this iteration
    fac_output.write(' '.join(factors))
    
    for row in f_list:
        if len(row) == len_valid_row:
            w = True
            vector = [row[i] for i in factor_indices]
        
        # check to make sure row is completely full
        for item in vector:
            if item == '' or item == ' ':
                w = False
        
        if w == True:
            current_label = '_'.join(row[label_index].split()) + '_' + row[diabetes_index]
            label_output.write(current_label + '\n')
            vec_output.write(' '.join(vector) + '\n')
            
            if corr == True: 
                for i in xrange(len(factor_indices)): 
                    factor_vectors[i].append(float(row[factor_indices[i]]))
                diab_vector.append(float(row[diabetes_index]))
        
    
    if corr == True:
        return diab_vector, factor_vectors

def get_correlations(diab_vector, factor_vectors):
    corr_file = open('correlations.csv', 'w+')
    c_writer = csv.writer(corr_file)
    for i in xrange(len(factor_indices)):
        pearson = pearsonr(diab_vector, factor_vectors[1])
        c_writer.writerow([factors[i]] + [pearson[0]] + [pearson[1]])


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', type=str)
    parser.add_argument('factors', type=list)
    parser.add_argument('corr', type=bool)
    
    args = parser.parse_args()
    
    f_list = get_filelist(args.datafile)

    # check to make sure it loaded
    # len(f_list)

    headers = f_list[0]
    del f_list[0]
    
    if args.corr == True:
        diab_vector, factor_vectors = write_output(f_list, headers, args.corr)
        get_correlations(diab_vector, factor_vectors)
    else:
        write_output(f_list, headers, args.corr)

    
if __name__ == '__main__': 
    main() 
    
    
    
    
        