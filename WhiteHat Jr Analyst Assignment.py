#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing libraries for data manipulation
import pandas as pd
import numpy as np


# In[2]:


# read in the Hourly Distribution Data
raw = pd.read_csv(r"C:\Users\HomeLaptop\Desktop\placementsxxx (1)\WhitehatJr\WhiteHat Assignment.csv")
raw.head()


# 1.	Based on the hourly distribution data, find out the surge hours on the platform (demand is high) and also explain the logic chosen to calculate at the surge slots.

# In[9]:


# Creating New Columns of total number of bookings and total number of completions
raw["total_bookings"] = raw["Paid_Bookings"] + raw["Total_Trial_Bookings"]
raw["total_completions"] = raw["Total_Trial_Completions"] + raw["Total_Paid_Completions"]
raw.head()


# In[27]:


# Grouping values of total_bookings by dayhour variable
# Computing the (mean+std deviation) as a threshold for surge hours
x = raw.groupby(["dayhour"])["total_bookings"].sum().sort_values(ascending = False).reset_index()
y = x["total_bookings"].mean()
z = x["total_bookings"].std()
print(y,z)
x["surge_hour"] = x["total_bookings"] > y+z
x


# Explanation: In the above cell,rows having 'True' value for surge_hours Flag are based on the whether the number of 
#     total bookings in that dayhour is greater than mean+std deviation of total_bookings.

# 2.	Based on the hourly distribution data, find out the hours where we need to increase teacher slots and explain the logic chosen to arrive at the same.

# In[22]:


# creating a column open slots which is the difference between total teachers slots and total completions
raw["open_slots"] = raw["Total_Teacher_Slots"] - raw["total_completions"]
raw.head()


# In[33]:


# Grouping by dayhour
# creating a column open_slots_ratio
x = raw.groupby(["dayhour"])[["Total_Teacher_Slots","open_slots"]].sum().reset_index()
x["open_slots_ratio"] = x["open_slots"]/x["Total_Teacher_Slots"]
# creating a flag for increase teacher slots when ever open_slots_ratio is negative
x["increase_teacher_slots"] = x["open_slots_ratio"] < 0
# sorting the values based on open_slots_ratio decreasing
x = x.sort_values(by="open_slots_ratio")
x


# Explantion: All the rows having flag increase_slots as True is based on difference between number of total teacher slots 
#     and total completions. The bigger the difference as a fraction of total teacher slots, more number of slots are 
#     required in the given dayhour.    

# 3.	Write a python script to plot a bar graph of the hourly distribution of paid and trial classes and completion segmented based on weekdays and weekends.

# In[3]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[6]:


raw.head() 


# In[30]:


raw_graph = raw.drop(['Total_Teacher_Slots'], axis=1)
raw_graph.head()


# In[25]:


sns.catplot(x="dayhour", y="Paid_Bookings", 
            hue="weektype", kind="bar", data=raw_graph)
sns.catplot(x="dayhour", y="Total_Trial_Bookings", 
            hue="weektype", kind="bar", data=raw_graph)
sns.catplot(x="dayhour", y="Total_Trial_Completions", 
            hue="weektype", kind="bar", data=raw_graph)
sns.catplot(x="dayhour", y="Total_Paid_Completions", 
            hue="weektype", kind="bar", data=raw_graph)


# In[35]:


dat = pd.read_csv(r"C:\Users\HomeLaptop\Desktop\placementsxxx (1)\WhitehatJr\WhiteHat Jr. Analyst Assignment.csv")
dat.head()


# Determine the best teachers (teachers with highest trial conversion%) in each level in the month of april and may

# In[37]:


dat["trial_conversion%"] = dat["Conversion"]*100/dat["TrialsCompleted"]
dat.head()


# In[65]:


dat["rank"] = dat.groupby(["Level", "TrialMonth"])["trial_conversion%"].rank("dense", ascending=False)
best_teachers = dat.loc[(dat['rank'] == 1) & (dat['TrialMonth'].isin([4,5]))]
print(best_teachers)


# Determine the monthly avg trial conversion at each level

# In[70]:


mnth_avg_tc = dat.groupby(["Level","TrialMonth"])["trial_conversion%"].mean()
print(mnth_avg_tc)


# Determine the avg. performance(trial conversion %) of new joinees in their month of joining

# In[99]:


from datetime import datetime, timedelta


# In[116]:


dat['date1'] = pd.to_datetime(dat['JoiningDate'], format="%Y-%m-%d")
dat['join_month'] = pd.DatetimeIndex(dat['JoiningDate']).month
dat.head()


# In[105]:


new_join_data = dat[dat.TrialMonth == dat.join_month]
new_join_data.head()


# In[112]:


new_join_month_avg_tc = new_join_data.groupby(["TrialMonth"])["trial_conversion%"].mean()
print(new_join_month_avg_tc)


# Determine the avg performance (trial conversion %)of new joinees in their 2nd month in the system

# In[110]:


new_join_data2 = dat[dat.TrialMonth == (dat.join_month + 1)]
new_join_data2.head()


# In[114]:


new_join_month2_avg_tc = new_join_data2.groupby(["TrialMonth"])["trial_conversion%"].mean()
print(new_join_month2_avg_tc)


# Determine the avg performance (trial conversion %) of teachers in May at each level based on their month of joining

# In[118]:


may_dat = dat[dat["TrialMonth"] == 5]
may_dat.head()


# In[121]:


may_avg_tc = may_dat.groupby(["Level","join_month"])["trial_conversion%"].mean()
print(may_avg_tc)

