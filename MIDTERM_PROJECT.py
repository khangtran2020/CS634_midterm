#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os 
import itertools


# # 1. Load Data

# In[2]:


print("Welcome to the simulation of the apriori algorithms.")
i = 0
csv = []
index = []
print("The available data is listed bellow, input the choice you want")
for file in os.listdir('data'):
    if ".csv" in file:
        csv.append(file)
        print(file, "- to choose this data input (" +str(i+1) +")")
        index.append(i+1)
        i += 1

while True:
    try:
        choice_of_data = int(input())
        if choice_of_data not in index:
            print("Input is not recognized, please input the number corresponding to the data")
        else:
            print('User chose', csv[choice_of_data-1], 'dataset')
            data = csv[choice_of_data-1]
            break
    except ValueError:
        print("Input is not recognized, please input the number corresponding to the data")
        
print("Loading and processing data ... ")


# In[3]:


filepath = 'data'
file = os.path.join(filepath, data)
df = pd.read_csv(file)
df.head()


# In[4]:


list_of_items = []
for tran in df[df.columns[-1]]:
    for item in str(tran).replace(u'\xa0', u'').split(', '):
        list_of_items.append(item)
list_of_items = set(list_of_items)
items = {}
i = 1
for item in list_of_items:
    items[item] = i
    i += 1
items


# In[5]:


for item in items:
    arr = np.zeros(df.shape[0]).astype(int)
    i = 0
    for tran in df[df.columns[1]]:
        if item in str(tran).replace(u'\xa0', u'').split(', '):
            arr[i] = 1
        i += 1
    df[item] = arr
df.head()


# # 2. Input Support & Confidence

# In[6]:


print("Done processing the data!")
print("Please choose the support rate (>= 0 & <= 1)")
while True:
    try:
        support_rate = float(input())
        if (support_rate < 0 or support_rate > 1):
            print("input is not in range (0,1)")
            continue
        break
    except ValueError:
        print("input is not float, please input in range (0,1)")
print("User chose support rate: %f" % support_rate)


# In[7]:


print("Please choose the confidence rate (>= 0 & <= 1)")
while True:
    try:
        confidence_rate = float(input())
        if (confidence_rate < 0 or confidence_rate > 1):
            print("input is not in range (0,1)")
            continue
        break
    except ValueError:
        print("input is not float, please input in range (0,1)")
print("User chose confidence rate: %f" % confidence_rate)


# In[8]:


min_support = support_rate*df.shape[0]


# # 3. Apriori Algorithms

# In[9]:


count_dict = {} 
for item in list_of_items:
    if np.sum(df[item]) >= min_support:
        count_dict[item] = np.sum(df[item])
set(count_dict.keys())


# In[10]:


list_frequent = []
for i in range(2, len(count_dict) + 1):
    ls = list(itertools.combinations(count_dict.keys(), i))
    for per in ls:
        if (np.sum(np.sum(df[list(per)], axis = 1) == i) >= int(min_support)):
            list_frequent.append(per)
#             print(len(list_frequent), list_frequent, per)


# In[11]:


print("Procesing ...")
print("Result: ")
for fred in list_frequent:
#     print("For frequent list,", fred, "we have rules:")
    sp2 = np.sum(np.sum(df[list(fred)], axis = 1) == len(list(fred)))
#     print("Support: ",sp2)
    ls = list(itertools.permutations(fred, len(fred)))
    for per in ls: 
        passed = False
        sp1 = np.sum(np.sum(df[list(per)[:-1]], axis = 1) == len(list(list(per)[:-1])))
        if (sp2/sp1 >= confidence_rate):
            passed = True
        if(passed): 
            print(" * ",list(per)[:-1], "=>",'"'+str(list(per)[-1])+'""',"with confidence:", sp2/sp1)

