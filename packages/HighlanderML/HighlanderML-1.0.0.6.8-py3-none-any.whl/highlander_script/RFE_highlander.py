### Library used in python:
import pandas as pd
import numpy as np
import multiprocessing




###Import specific function needed
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from concurrent.futures import ThreadPoolExecutor


# create a target dataframe for multiprocessing
def create_RFE_df_multi(seed_val, df, list_col, target_val, test_size=0.1):

    # split data set
    x_train, x_test, y_train, y_test = train_test_split( df[list_col], df[target_val],
                                                        test_size=(1-test_size), random_state=seed_val)



    return(x_train, y_train, list_col)

# get RFE model
def get_models_multi(i):
    models = dict()

    # set RFE  parameter
    rfe = RFE(estimator=DecisionTreeRegressor(random_state=0), n_features_to_select=1)

    # choose model
    model = GradientBoostingRegressor(random_state=0)

    # obtain model
    models[str(i)] = Pipeline(steps=[('s',rfe),('m',model)])
    return models

#obtain the RFE rank
def obtain_rank_df_multi(models, X, y,index,list_col):

    # define RFE
    rfe = models[str(index)]['s']

    # fit the RFE model
    rfe.fit(X, y)

    # obtain for each value the rank
    c_0=[]
    c_1=[]
    c_2=[]

    for i in range(X.shape[1]):
        c_0.append(list_col[i])
        c_1.append(rfe.support_[i])
        c_2.append(rfe.ranking_[i])

    #put the value in a dataframe
    data = {'Column':c_0, 'Selected':c_1, 'Rank_'+str(index):c_2}

    # Create DataFrame
    rfe_df = pd.DataFrame(data)

    return(rfe_df)

# devide work on processor
def multi_pro(y):

    # attribuzione delle varaibili
    test_size=y[0][0]
    df_clima=y[0][1]
    list_col=y[0][2]
    target_val=y[0][3]

    # attribuzioni degli intervalli di esecuzione
    start=y[1]
    end=y[2]

    result=[]

    #  loop for definition dataframe
    for  j in range (start,end,1):
        # define dataset
        X, y, list_col=create_RFE_df_multi(j, df_clima, list_col,  target_val, test_size)

        # get the models to evaluate
        models = get_models_multi(j)

        #input String
        string_name = "rfe_df"+str(j)

        #taking input variable name as a string
        result.append(obtain_rank_df_multi(models, X, y,j,list_col))

    return(result)


# define the job of each processor
def  sub_pro(var, n_pro, n_operation):

    # confrim operation number is lower than processor
    if n_operation<n_pro:
        n_pro=n_operation

    # build the value vector for signle processor
    vector_pro=[]
    gap=(n_operation-1)//(n_pro-1)

    for i in range (0,n_operation,gap):

        x=[]
        x.append(var); x.append(i); x.append(i+gap)
        vector_pro.append(x)

    # last job
    vector_pro[-1][2]=(n_operation)

    # se il passo è un numero pari a 1.x si fanno troppi sotto processi, si accorpano tutti i processi in un processo finale più lungo.
    if len(vector_pro)>n_pro:
        lim=vector_pro[-1][2]
        vector_pro=vector_pro[0:n_pro]
        vector_pro[-1][2]=lim

    return(vector_pro)


def RFE_highlander(test_size,mat_prod_250,list_col_clim,target_val,n_cros_fold=10,n_thread=4):

    var_multi=[test_size, mat_prod_250, list_col_clim, target_val]


    #pool = multiprocessing.Pool()
    #pool = multiprocessing.Pool(processes=n_thread)



    # create an array of value to use for multi processing
    inputs = sub_pro(var_multi, n_thread, n_cros_fold)


    with ThreadPoolExecutor(max_workers=n_thread) as pool:
        pool.submit(multi_pro,inputs)

        outputs = pool.map(multi_pro,inputs)


    rfe_df_group = {'Column': list_col_clim}
    rfe_df_group = pd.DataFrame(rfe_df_group)

    for i in outputs:
        for j in i:
            rfe_df_group[j.columns[2]]=j[j.columns[2]]



    return(rfe_df_group)
