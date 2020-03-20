#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Jared Galloway
"""
import numpy as np
import pandas as pd
import argparse
import pdb
import sys

if __name__=='__main__':

    # Description
    parser = argparse.ArgumentParser(description='Take an ASV table \
        in the same format given by Kaye, and convert it to the format \
        needed for habitatcorrection software.')
   
    parser.add_argument('--threshold', dest='threshold', action='store',
        default=50,type=float, help= "This parameter should \
        specify the percentage of samples a single taxa should exist in, \
        otherwise it's filtered out")

    parser.add_argument('--ASV', dest='ASV', action='store',
        help="This should point to the asv table you would like \
        to format for running through the habitat correction.")

    parser.add_argument('--meta', dest='meta', action='store',
        help="This should point to the metadata table you would like \
        to format for running through the habitat correction.")

    parser.add_argument('--out_a', dest='out_a', action='store',
        help="This should point to where you want the formatted \
        asv table to end up")

    parser.add_argument('--out_m', dest='out_m', action='store',
        help="This should point to where you want the formatted \
        metadata table written to")
        
    parser.add_argument('--subset_ava', dest='subset_ava',action='store',default=None)

    args=parser.parse_args()
    
    # a data frame holding all the meta-data
    md = pd.read_csv(args.meta,sep=',',header=(0),dtype=str).replace(np.nan, 'Missing', regex=True)
    md.rename(columns={'Sample ID':'sample_name'}, inplace=True)
    md.set_index('sample_name', inplace=True)

    # a data frame holding all the the asv counts.
    df = pd.read_csv(args.ASV,sep='\t',header=(0)).replace(np.nan, '0.0', regex=True)

    if args.subset_ava != None:
        # Samples ids that exist in our df and belong to the subset ava
        indx = [sampleid for sampleid in md["AVA"][md["AVA"] == subset_ava].index if sampleid in self.df.columns]

        # Now all the ones we need to drop
        drop_c = [sampleid for sampleid in df.columns[8:] if sampleid not in indx]
        df=df.drop(drop_c,axis=1) 

    # this counts the number of columns that are not 0 for each row (remember that each row represents a species.)
    # Number of points a species must exist in to be considered
    # quick problem though, 
    vcounts=np.sum(df!=0,axis=1)

    # Make a list which ties together all the species. 
    # taxa_list=['-'.join(i[1].tolist()+[str(index)]) for index,i in enumerate(df[['Family.x','Genus.x','Species.x']].iterrows())]
    taxa_list=['-'.join(i[1].tolist()+[str(index)]) for index,i in enumerate(df[['Family.x','Genus.x']].iterrows())]

    # {i : family-genus-species}
    # this dictionary will be used to replace the index 
    # into the data frame
    c_name={}
    for i,v in enumerate(taxa_list):
        c_name[i]=v

    # here we do the re-naming. not actually sure why, but it's a nice way to format the data.
    df.rename(index=c_name,inplace=True)

    # Okay, now simply drop the species which are not included in at least {threshold} samples.
    # if you wanted to filter out the ones with less than 50% prevelence, you just need to 
    # set the threshold <- number of samples // 2. etc.
    drop_i=[c_name[i] for i,v in enumerate(vcounts) if v < args.threshold]
    df=df.drop(drop_i,axis=0)

    # simplit make a list of sample ids,  
    samples=[i.strip('\n') for i in  list(md.index) if i.strip('\n') in df]

    # drop the rows of meta data we got 
    missing_samples=[i for i in  list(md.index) if i.strip('\n') not in df]
    md=md.drop(missing_samples)

    # variable lists are simply the 
    print(df.shape)

    # keep a copy of the original dataframe. 
    # df_filtered = df.copy(deep=True)
    # transpose the data frame
    df=df[samples].T

 
    # write out the tables to the correct format
    md.replace(' ', '_', regex=True).to_csv(args.out_m, sep = '\t')
    df.to_csv(args.out_a, sep = '\t')



