<h1><center>Opmatch</center>
</h1>

<center>A lightweight package for optimal case-control matching.</center>

<h3 align="center">
    <a href="#getting_started">Getting Started</a>&bull;
    <a href="#-Introduction">Introduction</a> &bull;
    <a href="#-quick-tour">Quick Tour</a>
</h3>

## ⚡️ Getting Started
-------------------------

```bash
pip install opmatch
```
or
```bash
conda install -c conda-forge opmatch
```

## 📚 Introduction 
-------------------------------

#### Optimal Matching
With this package, we provide a tool to perform optimal case-control/treated-untreated matching for observational studies. 
In optimal matching, the sum of all the pairwise case-control distances is minimized.
We can perform matching with constant and variable matching ratio using the assignment algorithm by constructing an appropriate distance matrix. If interested in details, please see Ming and Rosenbaum<sup>1</sup>. 

#### Why variable ratio matching? 
Optimal matching in its simplest form assigns one control to every case. However, if we have a large pool of controls it might be beneficial to have multiple cases matched to each control. This involves a bias-variance tradeoff. Higher matching ratio is associated with higher bias and a lower variance. We can also increase the power of an observational study by increasing the matching ratio. However, some cases might not have close controls, so increasing the overall matching ratio will result in bad matches for some cases. A more sophisticated procedure is matching with a variable ratio. Cases which have more controls closeby will have more matched controls<sup>2</sup>. Thus, a variable ratio match results in more closely matched sets and has the only downside of a slightly more involved statistical analysis of covariate balance<sup>3</sup>

#### Full Matching
A method superior to matching with a constant or variable ratio is full matching<sup>4</sup>. Full matching, in addition to having multiple controls per case, also allows to have multiple cases per control and thus includes other method as a special case. 

<sub><sup>[1] Ming, Kewei, and Paul R. Rosenbaum. "A note on optimal matching with variable controls using the assignment algorithm." Journal of Computational and Graphical Statistics 10.3 (2001): 455-463.</sub></sup><br>
<sub><sup>[2]Stuart, Elizabeth A. "Matching methods for causal inference: A review and a look forward." Statistical science: a review journal of the Institute of Mathematical Statistics 25.1 (2010): 1.</sub></sup><br>
<sub><sup>[3]Rosenbaum, Paul R., P. R. Rosenbaum, and Briskman. Design of observational studies. Vol. 10. New York: Springer, 2010.</sub></sup><br>
<sub><sup>[4]Cochran, William G., and S. Paul Chambers. "The planning of observational studies of human populations." Journal of the Royal Statistical Society. Series A (General) 128.2 (1965): 234-266.</sub></sup>

## 🚀 Quick Tour
----------------------------------

To obtain matches you can simply run:

```python
from opmatch.matcher import Matcher
case_control_dict = Matcher(
        df, matching_ratio, 
        min_mr, max_mr, n_controls, 
        metric, matching_type,
        case_col, var_cols,  ps_col,
        ).match()
```
>#### Parameters

* **matching_ratio** number of controls per case if matching ratio is constant

* **min_mr**: minimum number of controls per case
* **max_mr**: maximum number of controls per case
* **n_controls**: number of controls to match
* **metric**: PS or one of the metrics accepted by scipy.spatial.distances.cdist
* **matching_type**: constant or variable matching ratio
* **case_col**: boolean column where cases are 1s and controls 0s
* **var_cols**: columns containing relevatn patient variables
        if metric!=PS: var_cols used for matching
        if metric==PS but ps_col is not specified: var_cols used to compute PS using logistic regression
* **ps_col**: column containing the propensity score
* **case_col**: column name of case column, should contain 1s and 0s





### Generate Example Data


```python
from opmatch.tutorial import example_data, vis
import importlib
importlib.reload(example_data)
importlib.reload(vis)
import matplotlib.pyplot as plt

df = example_data.generate(100, 0.05)
vis.age_bmi_scatter_2d(df)
```


    
![png](README_files/README_8_0.png)
    


## Perform matching


```python
from opmatch.matcher import Matcher
cc_dic_const = Matcher(df=df, matching_ratio=5, metric='mahalanobis', 
            matching_type='const', var_cols=['age','bmi']).match()
cc_dic_variable = Matcher(df=df, min_mr=1, max_mr=5, n_controls=25, metric='mahalanobis', 
            matching_type='variable', var_cols=['age','bmi']).match()
cc_dic_ps = Matcher(df=df, min_mr=1, max_mr=5, n_controls=25, metric='PS', 
            matching_type='variable', var_cols=['age','bmi']).match()
```

    Number of cases: 6
    Size of the control pool: 94
    alpha=5, beta=5, M=94, m=30, n=6
    Number of cases: 6
    Size of the control pool: 94
    alpha=1, beta=5, M=94, m=25, n=6
    Number of cases: 6
    Size of the control pool: 94
    alpha=1, beta=5, M=94, m=25, n=6
    [0.06159769 0.04427071 0.08461961 0.06452836 0.06491768 0.06688619
     0.06508139 0.07153466 0.05064903 0.03763943 0.07143818 0.03605914
     0.06685975 0.05872672 0.07666819 0.07730829 0.06854143 0.0723814
     0.09116249 0.05966641 0.05853244 0.05921892 0.04612938 0.07016596
     0.05257855 0.04777556 0.07328428 0.06603252 0.06558964 0.07452406
     0.05370307 0.04376809 0.05240556 0.03574941 0.05951543 0.08727492
     0.06258391 0.07096218 0.0665969  0.0526835  0.04888883 0.06777055
     0.06553244 0.05392769 0.06234727 0.0523858  0.05408321 0.06216449
     0.07866163 0.04118135 0.04652342 0.05756416 0.05097115 0.04428986
     0.0589001  0.06799013 0.0388027  0.068023   0.05380009 0.05463769
     0.05222295 0.0424596  0.05481378 0.08421398 0.06112076 0.06250213
     0.05553318 0.05592791 0.07106023 0.05079039 0.07852998 0.04679658
     0.0474278  0.0522755  0.05178742 0.05670109 0.03675352 0.05056844
     0.06001288 0.04626556 0.05450453 0.0744184  0.08287265 0.04085123
     0.07578452 0.04498683 0.06383479 0.05028064 0.0615676  0.07677551
     0.08579241 0.09106993 0.05175926 0.07901101 0.04106486 0.07641788
     0.04914339 0.05860048 0.05484469 0.05060125]
    

    c:\Users\fjn197\PhD\projects\opmatch\opmatch\matcher.py:76: UserWarning: Propensity score column name not passed, and 'ps'/'PS' not found in df, perform logistic regression on var_cols, to compute ps
      warnings.warn("Propensity score column name not passed, and 'ps'/'PS' not found in df, perform logistic regression on var_cols, to compute ps")
    


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    File c:\Users\fjn197\Miniconda3\envs\opmatch\lib\site-packages\pandas\core\indexes\base.py:3803, in Index.get_loc(self, key, method, tolerance)
       3802 try:
    -> 3803     return self._engine.get_loc(casted_key)
       3804 except KeyError as err:
    

    File c:\Users\fjn197\Miniconda3\envs\opmatch\lib\site-packages\pandas\_libs\index.pyx:138, in pandas._libs.index.IndexEngine.get_loc()
    

    File c:\Users\fjn197\Miniconda3\envs\opmatch\lib\site-packages\pandas\_libs\index.pyx:165, in pandas._libs.index.IndexEngine.get_loc()
    

    File pandas\_libs\hashtable_class_helper.pxi:5745, in pandas._libs.hashtable.PyObjectHashTable.get_item()
    

    File pandas\_libs\hashtable_class_helper.pxi:5753, in pandas._libs.hashtable.PyObjectHashTable.get_item()
    

    KeyError: 'ps'

    
    The above exception was the direct cause of the following exception:
    

    KeyError                                  Traceback (most recent call last)

    Cell In [27], line 7
          2 cc_dic_const = Matcher(df=df, matching_ratio=5, metric='mahalanobis', 
          3             matching_type='const', var_cols=['age','bmi']).match()
          4 cc_dic_variable = Matcher(df=df, min_mr=1, max_mr=5, n_controls=25, metric='mahalanobis', 
          5             matching_type='variable', var_cols=['age','bmi']).match()
          6 cc_dic_ps = Matcher(df=df, min_mr=1, max_mr=5, n_controls=25, metric='ps', 
    ----> 7             matching_type='variable', var_cols=['age','bmi']).match()
    

    File c:\Users\fjn197\PhD\projects\opmatch\opmatch\matcher.py:79, in Matcher.match(self)
         77         self.compute_ps()
         78         self.ps_col = 'ps'
    ---> 79 X_case = self.df_case[self.ps_col].to_numpy().reshape(-1,1)
         80 X_control = self.df_control[self.ps_col].to_numpy().reshape(-1,1)
         81 dist_mat = cdist(X_case, X_control, metric='minkowski', p=1)
    

    File c:\Users\fjn197\Miniconda3\envs\opmatch\lib\site-packages\pandas\core\frame.py:3804, in DataFrame.__getitem__(self, key)
       3802 if self.columns.nlevels > 1:
       3803     return self._getitem_multilevel(key)
    -> 3804 indexer = self.columns.get_loc(key)
       3805 if is_integer(indexer):
       3806     indexer = [indexer]
    

    File c:\Users\fjn197\Miniconda3\envs\opmatch\lib\site-packages\pandas\core\indexes\base.py:3805, in Index.get_loc(self, key, method, tolerance)
       3803     return self._engine.get_loc(casted_key)
       3804 except KeyError as err:
    -> 3805     raise KeyError(key) from err
       3806 except TypeError:
       3807     # If we have a listlike key, _check_indexing_error will raise
       3808     #  InvalidIndexError. Otherwise we fall through and re-raise
       3809     #  the TypeError.
       3810     self._check_indexing_error(key)
    

    KeyError: 'ps'



```python
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig, axes = plt.subplots(1,2, figsize=(10,5))
for cc_dic, ax in zip([cc_dic_const, cc_dic_variable], axes):
    matched = []
    for color, (case, controls) in zip(colors, cc_dic.items()):
        matched.extend(controls)
        matched.append(case)
        ax.scatter(df.loc[case, 'age'], df.loc[case, 'bmi'], color = color, marker = 'x')
        ax.scatter(df.loc[controls, 'age'], df.loc[controls, 'bmi'], color = color, marker='o')
    unmatched = [i for i in df.index if i not in matched]
    ax.scatter(df.loc[unmatched, 'age'], df.loc[unmatched, 'bmi'], color = 'k', marker='.', alpha=.2)
# set shared label for x and y axis
fig.text(0.5, 0.04, 'age', ha='center', va='center')
fig.text(0.04, 0.5, 'bmi', ha='center', va='center', rotation='vertical')
axes[0].set_title('Constant matching ratio')
axes[1].set_title('Variable matching ratio')
```




    Text(0.5, 1.0, 'Variable matching ratio')




    
![png](README_files/README_11_1.png)
    



```python
fig, ax = plt.subplots()
# get colorwheel
#ax.scatter(df.loc[unmatched, 'ps'], df.loc[unmatched, 'ps'], color = 'k', marker='.', alpha=.2)
```


    
![png](README_files/README_12_0.png)
    

