#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## Local Government Area Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average maths score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing maths score (50 or greater)
# 
# * Calculate the percentage of students with a passing reading score (50 or greater)
# 
# * Calculate the percentage of students who passed maths **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[2]:


# identify the unique records for 'School ID'
unique_schools = school_data['School ID'].unique()

# determine how many items are in the unique_schools array                                              
total_schools = len(unique_schools)


# In[3]:


# identify the unique records for 'Student ID'
unique_studets = student_data['Student ID'].unique()

# determine how many items are in the unique_students array                                              
total_students = len(unique_studets)

# format the variable to add the thousand separator
formatted_total_students = f'{len(unique_studets):,}'


# In[4]:


# sum column 'budget' from school_data to determine the total budget
total_budget = school_data['budget'].sum()

# format the variable to add the '$' signal and present 2 decimal places
formatted_total_budget = f'${total_budget:,.2f}'


# In[5]:


# find the average of the maths_score column using the mean function
average_maths = round(student_data['maths_score'].mean(),2)


# In[6]:


# find the average of the reading_score column using the mean function
average_reading = round(student_data['reading_score'].mean(),2)


# In[7]:


# filter data containing only Maths Scores equal or greater than 50
maths_passing = student_data.loc[(student_data['maths_score'] >= 50) ]


# In[8]:


# filter data containing only Reading Scores equal or greater than 50
reading_passing = student_data.loc[(student_data['reading_score'] >= 50) ]


# In[9]:


# use loc function to filter the students with score >= 50 in reading_score AND maths_score
overall_passing = student_data.loc[(student_data['reading_score'] >= 50) & (student_data['maths_score'] >= 50) ]


# In[10]:


# count how many students are in the 'maths_score >=50' list filtered and convert that into percentage in relation to the total students
percentage_maths_passing = round(len(maths_passing) / total_students * 100,2)


# In[11]:


# count how many students are in the 'reading_score >=50' list filtered and convert that into percentage in relation to the total students
percentage_reading_passing = round(len(reading_passing) / total_students * 100,2)


# In[12]:


# count how many students are in the 'maths AND reading >=50' list filtered and convert that into percentage in relation to the total students
percentage_overall_passing = round(len(overall_passing) / total_students * 100,2)


# In[13]:


# create a Dataframe with the results found
lga_summary = pd.DataFrame({'Total Schools':[total_schools],
             'Total Students':formatted_total_students,
             'Total Budget':formatted_total_budget,
             'Average Maths Score':average_maths,
             'Average Reading Score':average_reading,
             '% Passing Maths':percentage_maths_passing,
             '% Passing Reading':percentage_reading_passing,
             '% Overall Passing':percentage_overall_passing,
             })
# display the dataframe
lga_summary


# ## School Summary

# * Create an overview table that summarises key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Maths Score
#   * Average Reading Score
#   * % Passing Maths
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed maths **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[14]:


# create a second dataframe with the relevant columns from the school_data, to manipulate the data
school_data2 = school_data[['school_name','type','size','budget']]


# In[15]:


# calculate the budget per student
per_student_budget = school_data2['budget'] / school_data2['size']

# add the calculation as a new column into the dataframe
school_data2['Per Student Budget'] = per_student_budget


# In[16]:


# sort data by 'school_name'
sorted_by_school_df = school_data2.sort_values('school_name')

# set the 'school_name' as the index of the dataframe
sorted_by_school_df.set_index('school_name', inplace = True)


# In[17]:


# format the school budget to add the '$' signal and present 2 decimal places
school_budget = sorted_by_school_df['budget'].map('${:,.2f}'.format)


# In[18]:


# format the budget per student data to add the '$' signal and present 2 decimal places
formatted_per_student_budget = sorted_by_school_df['Per Student Budget'].map('${:,.2f}'.format)


# In[19]:


# group student data by school_name to consolidate information and allow calculating averages per school
grouped_student_df = student_data.groupby(["school_name"])


# In[20]:


# store the average maths scores in a variable
school_avg_maths = round(grouped_student_df['maths_score'].mean(),2)


# In[21]:


# store the average reading scores in a variable
school_avg_reading = round(grouped_student_df['reading_score'].mean(),2)


# In[22]:


# identify how many students are above the pass grade for maths per school
maths_passing_per_school = maths_passing['school_name'].value_counts()

# calculate the percentage of students above the pass grade per school
pct_maths_passing_per_school = round(maths_passing_per_school / sorted_by_school_df['size'] * 100,2)


# In[23]:


# identify how many students are above the pass grade for reading per school
reading_passing_per_school = reading_passing['school_name'].value_counts()

# calculate the percentage of students above the pass grade per school
pct_reading_passing_per_school = round(reading_passing_per_school / sorted_by_school_df['size'] * 100,2)


# In[24]:


# identify how many students are above the pass grade for reading AND maths per school
overall_passing_per_school = overall_passing['school_name'].value_counts()

# calculate the percentage of students above the pass grade for reading AND maths per school
pct_overall_passing_per_school = round(overall_passing_per_school / sorted_by_school_df['size'] * 100,2)


# In[25]:


# create a Dataframe with the results found
school_summary = pd.DataFrame({'School Type':sorted_by_school_df['type'],
                              'Total Students':sorted_by_school_df['size'],
                              'Total School Budget':school_budget,
                              'Per Student Budget':formatted_per_student_budget,
                              'Average Maths Score':school_avg_maths,
                              'Average Reading Score':school_avg_reading,
                              '% Passing Maths':pct_maths_passing_per_school,
                              '% Passing Reading':pct_reading_passing_per_school,
                              '% Overall Passing':pct_overall_passing_per_school,
                              })
# display the dataframe
school_summary


# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[26]:


# sort the the dataframe from the greatest to the lowest percentage overall passing.
top_schools = school_summary.sort_values('% Overall Passing', ascending = False)
# display the top 5 results
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[27]:


# sort the the dataframe from the lowest to the greatest percentage overall passing.
bottom_schools = school_summary.sort_values('% Overall Passing')
# display the top 5 results of the list
bottom_schools.head(5)


# ## Maths Scores by Year

# * Create a table that lists the average maths score for students of each year level (9, 10, 11, 12) at each school.
# 
#   * Create a pandas series for each year. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[28]:


# filter the dataframe with only year 9 students
year9_df = student_data.loc[(student_data['year'] == 9),:]

# group the filtered data by School Name
grouped_y9_df = year9_df.groupby(['school_name']) 

# calculate the mean of year 9 students maths score
y9_maths_avg = round(grouped_y9_df['maths_score'].mean(),1)
# calculate the mean of year 9 students reading score
y9_reading_avg = round(grouped_y9_df['reading_score'].mean(),1)


# In[29]:


# filter the dataframe with only year 10 students
year10_df = student_data.loc[(student_data['year'] == 10),:]

# group the filtered data by School Name
grouped_y10_df = year10_df.groupby(['school_name']) 

# calculate the mean of year 10 students maths score
y10_maths_avg = round(grouped_y10_df['maths_score'].mean(),1)
# calculate the mean of year 10 students reading score
y10_reading_avg = round(grouped_y10_df['reading_score'].mean(),1)


# In[30]:


# filter the dataframe with only year 11 students
year11_df = student_data.loc[(student_data['year'] == 11),:]

# group the filtered data by School Name
grouped_y11_df = year11_df.groupby(['school_name']) 

# calculate the mean of year 11 students maths score
y11_maths_avg = round(grouped_y11_df['maths_score'].mean(),1)
# calculate the mean of year 11 students reading score
y11_reading_avg = round(grouped_y11_df['reading_score'].mean(),1)


# In[31]:


# filter the dataframe with only year 12 students
year12_df = student_data.loc[(student_data['year'] == 12),:]

# group the filtered data by School Name
grouped_y12_df = year12_df.groupby(['school_name']) 

# calculate the mean of year 12 students maths score
y12_maths_avg = round(grouped_y12_df['maths_score'].mean(),1)

# calculate the mean of year 12 students reading score
y12_reading_avg = round(grouped_y12_df['reading_score'].mean(),1)


# In[32]:


# create a Dataframe with the results found for maths
maths_scores_by_year_df = pd.DataFrame({'Year 9':y9_maths_avg,
                                       'Year 10':y10_maths_avg,
                                       'Year 11':y11_maths_avg,
                                       'Year 12':y12_maths_avg,
                                       })

# display the dataframe
maths_scores_by_year_df


# ## Reading Score by Year

# * Perform the same operations as above for reading scores

# In[33]:


# create a Dataframe with the results found for reading
reading_scores_by_year_df = pd.DataFrame({'Year 9':y9_reading_avg,
                                       'Year 10':y10_reading_avg,
                                       'Year 11':y11_reading_avg,
                                       'Year 12':y12_reading_avg,
                                       })
# display the dataframe
reading_scores_by_year_df


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Maths Score
#   * Average Reading Score
#   * % Passing Maths
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[34]:


# create a copy of the dataframe to manipulate the data without interfering in the original one, already used for other calculations
school_summary2 = school_summary.copy()
# check the datatypes of the dataframe
school_summary.dtypes


# In[35]:


# present a snippet of the dataframe to check how data is presented
school_summary2.head(2)


# In[36]:


# remove the '$' symbol from Per Student Budget and change the datatype to float, so we can make calculations using the column
school_summary2['Per Student Budget'] = school_summary2['Per Student Budget'].str.replace('$','').astype('float')


# In[37]:


# create bins and labels based on the budget per student
bins = [0, 585, 630, 645, 680]
labels = ['<\$585','\$585-$630','\$630-$645','\$645-$680']

# add the labels to the dataframe
school_summary2['Spending Ranges (per student)'] = pd.cut(school_summary2['Per Student Budget'], bins, labels = labels, include_lowest = True)


# In[38]:


# group the data into the created bins
spending_maths_scores = round(school_summary2.groupby(['Spending Ranges (per student)'])['Average Maths Score'].mean(),2)
spending_reading_scores = round(school_summary2.groupby(['Spending Ranges (per student)'])['Average Reading Score'].mean(),2)
spending_passing_maths_scores = round(school_summary2.groupby(['Spending Ranges (per student)'])['% Passing Maths'].mean(),2)
spending_passing_reading_scores = round(school_summary2.groupby(['Spending Ranges (per student)'])['% Passing Reading'].mean(),2)
overall_passing_spending_scores = round(school_summary2.groupby(['Spending Ranges (per student)'])['% Overall Passing'].mean(),2)


# In[39]:


# create a dataframe with the results
spending_summary = pd.DataFrame({'Average Maths Score':spending_maths_scores,
                                'Average Reading Score':spending_reading_scores,
                                '% Passing Maths':spending_passing_maths_scores,
                                '% Passing Reading':spending_passing_reading_scores,
                                '% Overall Passing':overall_passing_spending_scores,
                                })
#display the dataframe
spending_summary


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[40]:


# create bins and labels based on the school size
bins2 = [0, 1000, 2000, 5000]
labels2 = ['Small(<1000)','Medium(1000-2000)','Large(2000-5000)']

# add the labels to the dataframe
school_summary2['School Size Bins'] = pd.cut(school_summary2['Total Students'], bins2, labels = labels2, include_lowest = True)


# In[41]:


# group the data into the created bins
spending_maths_scores2 = round(school_summary2.groupby(['School Size Bins'])['Average Maths Score'].mean(),2)
spending_reading_scores2 = round(school_summary2.groupby(['School Size Bins'])['Average Reading Score'].mean(),2)
spending_passing_maths_scores2 = round(school_summary2.groupby(['School Size Bins'])['% Passing Maths'].mean(),2)
spending_passing_reading_scores2 = round(school_summary2.groupby(['School Size Bins'])['% Passing Reading'].mean(),2)
overall_passing_spending_scores2 = round(school_summary2.groupby(['School Size Bins'])['% Overall Passing'].mean(),2)


# In[42]:


# create a dataframe with the results
size_summary = pd.DataFrame({'Average Maths Score':spending_maths_scores2,
                                'Average Reading Score':spending_reading_scores2,
                                '% Passing Maths':spending_passing_maths_scores2,
                                '% Passing Reading':spending_passing_reading_scores2,
                                '% Overall Passing':overall_passing_spending_scores2,
                                })
# display the dataframe
size_summary


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[43]:


# group the data by school type (information already in the dataset)
spending_maths_scores3 = round(school_summary2.groupby(['School Type'])['Average Maths Score'].mean(),2)
spending_reading_scores3 = round(school_summary2.groupby(['School Type'])['Average Reading Score'].mean(),2)
spending_passing_maths_scores3 = round(school_summary2.groupby(['School Type'])['% Passing Maths'].mean(),2)
spending_passing_reading_scores3 = round(school_summary2.groupby(['School Type'])['% Passing Reading'].mean(),2)
overall_passing_spending_scores3 = round(school_summary2.groupby(['School Type'])['% Overall Passing'].mean(),2)


# In[44]:


# create a dataframe with the results
type_summary = pd.DataFrame({'Average Maths Score':spending_maths_scores3,
                                'Average Reading Score':spending_reading_scores3,
                                '% Passing Maths':spending_passing_maths_scores3,
                                '% Passing Reading':spending_passing_reading_scores3,
                                '% Overall Passing':overall_passing_spending_scores3,
                                })
# display the dataframe
type_summary


# In[ ]:




