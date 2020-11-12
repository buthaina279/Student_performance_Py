#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as st
from statsmodels.formula.api import ols 
from statsmodels.stats.multicomp import (pairwise_tukeyhsd,
                                         MultiComparison)
# %%
#read the data set
students = pd.read_csv("data/StudentsPerformance.csv")

#%%
# and because there is spaces in column's name 
# we are going to replace it with "_"
students.columns = students.columns.str.replace(' ', '_')

#%%
#explore the data set
students.head()

# %%
#show column's name 
students.columns

#%%
#EDA
#%%
# show the relashionship between all Continuous features
sns.pairplot(students, vars = ["math_score", "reading_score", "writing_score"])

# %%
# correlations between the continouse features 
students[["math_score", "reading_score", "writing_score"]].corr()
# %%
# show correlations between the continouse features 
sns.heatmap(students[["math_score", "reading_score", "writing_score"]].corr(), annot=True, cmap = 'Reds')

# %%
#compare the scores for each subject based in the gender
sns.boxplot(students_t.sbj_name, students_t.scores, hue = students_t.gender)

# %%
#adding index column to the data set 
# in order to melt using this identifier for each row 
students = students.reset_index() 


#%%
#rename index column
students =  students.rename(columns = {"index": "ID"})
students
#%%
# create tidy data set 
# and create one column for subjects' name 
# and one for its scores
students_t = students.melt(id_vars= ['ID', 
                                        'gender', 
                                        'race/ethnicity',
                                        'parental_level_of_education',
                                        'lunch', 
                                        'test_preparation_course'], 
                                value_vars=['math_score', 
                                            'reading_score', 
                                            'writing_score'],
                                var_name='sbj_name',
                                value_name='scores')

students_t
# %%
#test if the melting worked well
students_t.loc[students_t['index'] == 3]


#%%
# Descriptive statistics 
students_t.groupby(['gender','sbj_name'])['scores'].describe()

#%%
#set a theme for the plots 
sns.set_theme(style="ticks", color_codes=True)
# %%
#Infrential statistics 
# Normal distribution for the three subjects
sns.displot(students_t, x = "scores" ,
col = "sbj_name", 
kind = "hist")


#%%
# central limit theorem 
#%%
# Create a list
sampled_means = []
#create a list contain subject's name
subjects = ["math_score", "reading_score", "writing_score"]

#iterate this for loop for each subject 
# and print the central limit theorem
# For 1000  times
for i in subjects:
    for ii in range(0,1000):
        sampled_means.append(students[i].sample(n=100).mean())
    pd.Series(sampled_means).hist(bins=50)

#%%

#The data is normally distributed in math, reading,
#  and writing score in both population 
# and sample means
#the sample mean x¯ is an unbiased estimator 
# for the underlying population mean μ
#the sample means x¯ are centered on 
# the population mean μ
# %%
# 95% CI for each subject 
#creat a list 
CI = []
for i in subjects:
    CI.append(st.t.interval(alpha=0.95, df=len(students[i])-1, loc=np.mean(students[i]), scale=st.sem(students[i])))
#%%
# print 95% for math
math_CI = CI[0]
math_CI
#There is a 95% chance that interval 
# [65.14806, 67.02994] covers the true population 
# parameter μ (66.089)
#%%
#print the CI for reading
reading_CI = CI[1]
reading_CI
#There is a 95% chance that interval 
# [68.26299, 70.07501] covers the true population
#  parameter μ (69.169)
#%%
#print the CI for writing
writing_CI = CI[2]
writing_CI
#There is a 95% chance that interval 
# [67.11104, 68.99696] covers the true population
#  parameter μ (68.054)
#%%
#Linear regression  
# between math score and reading score
sns.regplot(x="math_score", y="reading_score", data = students)

#%%
#t-test
st.ttest_ind(students['math_score'],
                students['reading_score'])
#Reject the null hypothesis There is a relashion
#  between math score and reading score
#%%
#Linear regression  
# between math score and writing score
sns.regplot(x="math_score", y="writing_score", data = students)
#Reject the null hypothesis

#%%
#t-test
st.ttest_ind(students['math_score'],
                students['writing_score'])
#%%
# 1-way ANOVA
model = ols("parental_level_of_education ~ math_score", students)
results = model.fit()
aov_table = sm.stats.anova_lm(results, typ=2)
aov_table
#The lowest scores illustrates that the students whose parent have high school education
#%%
#tucky test 

tuky_students = pairwise_tukeyhsd(students_t['parental_level_of_education'], chicken_weights['math_score'])
print("full tukey")
print(tuky_students)
# %%
