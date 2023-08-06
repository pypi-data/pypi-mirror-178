# Highlander Project

This repository contains all the information for the Machine learning data analyses used in the Highlander project

## Dependencies

The following dependencies are required to perform the analysis in Python:

```
pandas>=1.3.4 
numpy>=1.21.2
scikit-learn>=1.0
h2o>=3.38.0.1
```
The main functions are grouped into two files:

```
RFE_module.py
H2O_module.py
```

## Modules and functions

Two modules are required to perform the analyses in the highlander_script/ directory. The RFE_module.py perform a Recursive Feature Elimination reducing the input variables. The user can define the number of features to maintain. The discarded features are the most uninformative and redundant in the dataset. Consequently, this step can reduce the variables, allowing a more precise and quick analysis using the Machine Learning algorithms. It can be considered a feature selection before analyzing the data. The function name is: "RFE_highlander()".
The H2O_module.py contains several functions to perform the Machine Learning analyses. In detail:

<ul>
<li> It searches for the best algorithm to perform the prediction; the best algorithm is chosen using a set of different models (best_model)</li>
<li> Once the best model is selected, the best hyper-parameters are tuned using a grid search approach (grid_search_gbm)</li>
<li> The relative importance of all the variables in the prediction is then evaluated (varimp)</li> 
<li> The model is then trained and tested, and the accuracy is evaluated using the Mean Absolute Error metric (mae_nf)</li>
<li> The subset of the most important variables is identified. This step an be considered a feature selection after the data analysis (varimp)</li>
<li> The SHAP algorithm is then used to evaluate the contribution and the explanation of each feature to the classification (shap)</li>
<li> The explaination of the model is useful to evaluate the contribution of the feature to the model (explain_model)</li>
</ul>

## Tutorial

The whole pipeline to perform and end-to-end data analysis is reported as a Python notebook file ("Highlander_ML_notebook.ipynb") in the "Notebook" directory. 
