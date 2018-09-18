import pandas as pd
import os,sys
from pandas import ExcelWriter

a = pd.read_excel(open('E:\ExcelTool\TEST\CTE.xlsx','rb'))

b = a[['Course']]
c = a[['DCCCD']]

b = b.dropna()
b['length'] = b['Course'].apply(lambda x : len(x))

# length = b['length'].unique()

d = b[(b.length <10)]

d = d[['Course']]

# d = d['Course'].apply(lambda x: x.split(' '))
# d['SUBJECT_ID'] = d.apply(lambda x: x[0])
# d['COURSE_NUMBER'] = d.apply(lambda x: x[1])

# # 
# v = d['Course'][0]
# print(v[5:9])
# sp = v[4]
# d = pd.DataFrame(d.Course.str.split(v).tolist())

# d = d['Course'].apply(lambda x: x.split(' '))
d['SUBJECT_ID'] = d['Course'].astype(str).str[0:4]
d['COURSE_NUMBER'] = d['Course'].astype(str).str[5:9]
# print(d)

os.chdir('E:\ExcelTool\TEST')
writer = ExcelWriter('PythonExport.xlsx')
d.to_excel(writer,'Sheet1', index = False)
writer.save()

