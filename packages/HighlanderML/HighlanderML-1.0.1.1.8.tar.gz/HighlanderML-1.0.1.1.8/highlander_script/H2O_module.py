# h2o module
import h2o
import pandas as pd

#Import specific function needed
from sklearn.model_selection import train_test_split
from numpy import mean
from numpy import std
from sklearn.pipeline import Pipeline
from h2o.automl import H2OAutoML
from collections import Counter
from h2o.grid.grid_search import H2OGridSearch
from sklearn.metrics import mean_absolute_error as mae

# find the best algorithm
def best_model(df, target_val, run_time=60, seed=1, max_mem_size=4, A_train=0.5, A_test=0.2):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # create H2O df
    df_h2o=h2o.H2OFrame(df)

    # split the dataset in train, test and validation set
    A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train, A_test])

    # Remove from the target value the variable
    y = target_val
    x = df_h2o.columns
    x.remove(y)

    # train different model
    aml = H2OAutoML(max_runtime_secs = run_time, seed = seed, exclude_algos = ["StackedEnsemble"], verbosity="info")
    aml.train(x = x, y = y, training_frame = A_train, validation_frame=A_valid)

    # best model information
    lb = aml.leaderboard
    data_as_df = lb.as_data_frame()

    # shutdown H2O
    h2o.shutdown()

    return(data_as_df)


# Grid search
def grid_search(df, target_val, max_mem_size=4, A_train=0.5, A_test=0.2,

                mod = 'H2OGradientBoostingEstimator',

                mod_params2 = {'learn_rate': [0.1], 'max_depth': [*range(10,100,10)],
                'sample_rate': [0.2,0.5,1.0], 'col_sample_rate': [0.2, 0.5, 1.0], 'ntrees': [*range(10,100,10)]},

                search_criteria = {'strategy': 'RandomDiscrete', 'seed': 1, 'max_runtime_secs': 60,
                   'stopping_tolerance': 0.001, 'stopping_rounds': 10, 'stopping_metric': "MAE"}):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # module to import, if defaul import H2OGradientBoostingEstimator
    exec('from h2o.estimators.gbm import ' + mod + ' as model_h2o_search', globals())



    # create H2O df
    df_h2o=h2o.H2OFrame(df)


    # split the dataset in train, test and validation set
    A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train, A_test])

    # create target dataset and target value
    y = target_val
    x = df_h2o.columns
    x.remove(y)


    # set grid search parameter
    grid_test = H2OGridSearch(model=model_h2o_search,
                              grid_id='gbm_grid',
                              hyper_params=mod_params2,
                              search_criteria=search_criteria )
    # train the grid search
    grid_test.train(x=x, y=y,
                    training_frame=A_train,
                    validation_frame=A_valid,
                    seed=1)

    # Get the grid results, sorted by validation AUC
    gbm_gridperf3 = grid_test.get_grid(sort_by='MAE', decreasing=False)

    # shutdown H2O
    h2o.shutdown()

    # delete the global variable:
    del globals()['model_h2o_search']

    return(gbm_gridperf3)


# find the variable importance
def varimp(df, target_val,
            mod = 'H2OGradientBoostingEstimator',
            nfolds=5, ntrees=10, col_sample_rate=0.1, learn_rate=0.1, max_depth=3, sample_rate=0.1, seed=1,
            max_mem_size=4, A_train=0.5, A_test=0.2):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # module to import, if defaul import H2OGradientBoostingEstimator
    exec('from h2o.estimators.gbm import ' + mod + ' as model_h2o_search', globals())

    # create the model with the best value from the gris search
    select_model =  model_h2o_search(nfolds=nfolds, ntrees=ntrees, col_sample_rate=col_sample_rate, learn_rate=learn_rate,
                                            max_depth=max_depth, sample_rate=sample_rate, seed=seed, keep_cross_validation_predictions = True)

    # create H2O df
    df_h2o=h2o.H2OFrame(df)

    # split the dataset in train, test and validation set
    A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train, A_test])

    # create target dataset and target value
    y = target_val
    x = df_h2o.columns
    x.remove(y)

    # train the model
    select_model.train(x=x, y=y, training_frame=A_train)

    # obtain the variable importance
    varimp = select_model.varimp(use_pandas=True)

    # shutdown H2O
    h2o.shutdown()

    # delete the global variable:
    del globals()['model_h2o_search']

    return(varimp)

# explain model
def explain_model(df, target_val,
                    mod = 'H2OGradientBoostingEstimator',
                    nfolds=5, ntrees=10, col_sample_rate=0.1, learn_rate=0.1, max_depth=3, sample_rate=0.1, seed=1,
                    max_mem_size=4, A_train=0.5, A_test=0.2):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # module to import, if defaul import H2OGradientBoostingEstimator
    exec('from h2o.estimators.gbm import ' + mod + ' as model_h2o_search', globals())

    # create the model with the best value from the gris search
    select_model =  model_h2o_search(nfolds=nfolds, ntrees=ntrees, col_sample_rate=col_sample_rate, learn_rate=learn_rate,
                                            max_depth=max_depth, sample_rate=sample_rate, seed=seed, keep_cross_validation_predictions = True)

    # create H2O df
    df_h2o=h2o.H2OFrame(df)

    # split the dataset in train, test and validation set
    A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train, A_test])

    # create target dataset and target value
    y = target_val
    x = df_h2o.columns
    x.remove(y)

    # train the model
    select_model.train(x=x, y=y, training_frame=A_train)

    # obtain the variable importance
    print(select_model.explain(A_test))

    # shutdown H2O
    h2o.shutdown()

    # delete the global variable:
    del globals()['model_h2o_search']



# print the shap  of the model
def shap(df, target_val,
            mod = 'H2OGradientBoostingEstimator',
            nfolds=5, ntrees=10, col_sample_rate=0.1, learn_rate=0.1, max_depth=3, sample_rate=0.1, seed=1,
            n_features=5, max_mem_size=4, A_train=0.5, A_test=0.2):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # module to import, if defaul import H2OGradientBoostingEstimator
    exec('from h2o.estimators.gbm import ' + mod + ' as model_h2o_search', globals())

    # create the model with the best value from the gris search
    select_model =  model_h2o_search(nfolds=nfolds, ntrees=ntrees, col_sample_rate=col_sample_rate, learn_rate=learn_rate,
                                            max_depth=max_depth, sample_rate=sample_rate, seed=seed, keep_cross_validation_predictions = True)

    # create H2O df
    df_h2o=h2o.H2OFrame(df)

    # split the dataset in train, test and validation set
    A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train, A_test])

    # create target dataset and target value
    y = target_val
    x = df_h2o.columns
    x.remove(y)

    # train the model
    select_model.train(x=x, y=y, training_frame=A_train)

    # obtain the variable importance
    print(select_model.shap_summary_plot(A_test, top_n_features=n_features))

    # shutdown H2O
    h2o.shutdown()

    # delete the global variable:
    del globals()['model_h2o_search']

# mae development base on the number of feature
def mae_nf(df, target_val, varimp, n_feature_start=2, n_feature_end=0,
           mod = 'H2OGradientBoostingEstimator',
           nfolds=5, ntrees=10, col_sample_rate=0.1, learn_rate=0.1, max_depth=3, sample_rate=0.1, seed=1,
           step=1, max_mem_size=4, A_train_value=0.5, A_test_value=0.2):

    # define mem size:
    max_mem_size= str(int(max_mem_size))+"g"

    # start H2O
    h2o.init(max_mem_size = max_mem_size)

    # module to import, if defaul import H2OGradientBoostingEstimator
    exec('from h2o.estimators.gbm import ' + mod + ' as model_h2o_search', globals())

    # empy vector to store MAE
    vector_mae=[]

    # define_the maximum number of feature:
    if n_feature_end==0:
        n_feature_end=varimp.shape[0]

    for i in range(n_feature_start,n_feature_end,step):
        # create a list of feature to analys
        col_mae=varimp["variable"].to_list()[0:i]
        # append the target feature
        col_mae.append(target_val)

        # create H2O mae df
        df_mae=df[col_mae]

        # create H2O df
        df_h2o=h2o.H2OFrame(df_mae)

        # set the best algorim value
        algoritm_mae =  model_h2o_search(nfolds=nfolds, ntrees=ntrees, col_sample_rate=col_sample_rate, learn_rate=learn_rate,
                                            max_depth=max_depth, sample_rate=sample_rate, seed=seed, keep_cross_validation_predictions = True)

        # split the dataset in train, test and validation set
        A_train,A_test,A_valid = df_h2o.split_frame(ratios=[A_train_value, A_test_value])

        # create target dataset and target value
        y = target_val
        x = df_h2o.columns
        x.remove(y)

        # train algoritm
        algoritm_mae.train(x=x, y=y, training_frame=A_train, validation_frame=A_valid)


        # create df for prediction
        y_test = [target_val] ### validatore del risultato
        x_test = A_test
        x_test=x_test.drop(y_test, axis=1)

        # algoritm prediction
        pred=algoritm_mae.predict(x_test)

        #calculate MAE
        mae_test=mae(A_test.as_data_frame()[target_val].tolist(),pred.as_data_frame()["predict"].tolist())
        # store MAE
        vector_mae.append(mae_test)


    # intialise data of lists.
    data = {'mae':vector_mae,
            'number_of_feature':[*range(2,n_feature_end,step)]}


    # Create DataFrame with all the mae
    df_mae_complete = pd.DataFrame(data)

    # shutdown H2O
    h2o.shutdown()

    # delete the global variable:
    del globals()['model_h2o_search']

    return(df_mae_complete)



# end
