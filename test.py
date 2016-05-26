# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:42:42 2016

@author: Saranya
"""

import pandas as pd
import json


df = pd.read_csv('data.csv')

# choose columns to keep, in the desired nested json hierarchical order
df = df[["category", "sub_category","sub_category_type", "count"]]

# order in the groupby here matters, it determines the json nesting
# the groupby call makes a pandas series by grouping "category", "sub_category" and"sub_category_type", 
#while summing the numerical column 'count'
df1 = df.groupby(["category", "sub_category","sub_category_type"])['count'].sum()
df1 = df1.reset_index()

print df1

d = dict()
d = {"name":"stock", "children": []}

for line in df1.values:
    category = line[0]
    sub_category = line[1]
    sub_category_type = line[2]
    count = line[3]

    # make a list of keys
    category_list = []
    for item in d['children']:
        category_list.append(item['name'])

    # if 'category' is NOT category_list, append it
    if not category in category_list:
        d['children'].append({"name":category, "children":[{"name":sub_category, "children":[{"name": sub_category_type, "count" : count}]}]})
    
    # if 'category' IS in category_list, add a new child to it
    else:
        sub_list = []        
        for item in d['children'][category_list.index(category)]['children']:
            sub_list.append(item['name'])
        print sub_list
        
        if not sub_category in sub_list:
            d['children'][category_list.index(category)]['children'].append({"name":sub_category, "children":[{"name": sub_category_type, "count" : count}]})
        else:
            d['children'][category_list.index(category)]['children'][sub_list.index(sub_category)]['children'].append({"name": sub_category_type, "count" : count})


print json.dumps(d)
