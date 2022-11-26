import create_test_data
import pandas as pd
import numpy as np
from opmatch.main import match
# import opmatch

df = create_test_data.get_test_data(True, 7,pcase=.1, random_state=101)
df['matched'] = 0
df['case'] = df.y
test_data = np.array([
    [1, .8],
    [1, .4],
    [0, .3],
    [0, .5],
    [0, .4],
    [0, .1],
    [0, .2]
])
df_test = pd.DataFrame(columns=['case', 'ps'], 
            data = test_data)
print('case', len(df[df.case==1]))
print('constant')
dic_const = match(df=df_test, matching_ratio=2,metric='PS',
        matching_type='const')
print(dic_const)
print('variable')
dic_const = match(df=df_test, min_mr=1,max_mr=3, n_controls=3,metric='PS',
        matching_type='var')
print(dic_const)

print('entire_number')
dic_const = match(df=df_test,metric='PS',
        matching_type='entire_number')
print(dic_const)
