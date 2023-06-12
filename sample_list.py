import pandas as pd 
data = pd.read_csv("/gpfs/data/user/aditya/PED_files/test.csv")
data['eid'] = data['eid'].apply(int)
a = list(data['eid'])
d = ()
n = '_'
a = data ['eid']
for x in a: 
  for r in a:
    if x == r: 
      c = ('%d' + '_' + '%d') % (x, r)
      file2.write (c + '\n')
      print(c)
