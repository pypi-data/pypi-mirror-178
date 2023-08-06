from scipy import stats
from xgboost import XGBRegressor
import numpy as np
import pandas as pd


def verify_ml_dataset(dataset, target):
    # check for null values in pandas dataframe
    DATA_IMBALANCE_THRESHOLD = 0.1
    TOO_MANY_ZEROES_THRESHOLD = 0.1
    FEATURE_IMPORTANCE_THRESHOLD = 0.01
    dict_main = {}
    dict = {"null_values":[],  "string_features":[], "too_many_zeros":[], "outliers":[], "data_imbalance":[], "data_normalization":[]}
    dict_main["errors"]=dict
    dict_main["warnings"]=dict
    dict_main["success"]=dict  

       
    for column in dataset.columms:

        # check for null values in pandas dataframe
        if dataset[column].isnull().values.any():
            dict_main["errors"]["null_values"].append(column)
        else:
            dict_main["success"]["null_values"].append(column)

        # check for string columns in pandas dataframe
        if (dataset[column].dtypes == object).sum() > 0:
            dict_main["errors"]["string_features"].append(column)
        else:
            dict_main["success"]["string_features"].append(column)

        # check for too many zeroes in pandas dataframe
        count = 0
        column_name = dataset[column]
        count += (column_name == 0).sum()
        if count > len(dataset[column]) * TOO_MANY_ZEROES_THRESHOLD:
            dict_main["warnings"]["too_many_zeros"].append(column)
            break

        # Check for outliers
        if column in dict_main["success"]["string_features"]:
            z_scores = stats.zscore(dataset[column])
            abs_z_scores = np.abs(z_scores)
            # Select data points with a z-scores above or below 3
            filtered_entries = (abs_z_scores < 3).all(axis=1)
            if len(filtered_entries) > 0:
                dict_main["warnings"]["outliers"].append(column)
            else:
                dict_main["success"]["outliers"].append(column)

        # Check for data imbalance
        # try:
        #     values = Y.value_counts()
        #     if (
        #         values[0] * DATA_IMBALANCE_THRESHOLD > values[1]
        #         or values[1] * DATA_IMBALANCE_THRESHOLD > values[0]
        #     ):
        #         dict_main[column]["warnings"].append("data_imbalance")
        #     else:
        #         dict_main[column]["success"].append("data_imbalance")
        # except:
        #     labels = []
        #     for column_name in Y.columns:
        #         if "label" in column_name:
        #             labels.append(dataset[column_name][1])
        #     labels.sort()
        #     if (
        #         labels[0] * DATA_IMBALANCE_THRESHOLD > labels[-1]
        #         or labels[-1] * DATA_IMBALANCE_THRESHOLD > labels[0]
        #     ):
        #         dict_main[column]["warnings"].append("data_imbalance")
        #     else:
        #         dict_main[column]["success"].append("data_imbalance")

        # # check for feature importance
        # if "string_features" in dict_main[column]["success"]:
        #     xgb = XGBRegressor()
        #     xgb.fit(dataset, Y)
        #     importance = xgb.feature_importances_
        #     for score in importance:
        #         if score < FEATURE_IMPORTANCE_THRESHOLD:
        #             dict["warnings"].append("low_importance_features")
        #             break
        #     else:
        #         dict["success"].append("low_importance_features")

        # Data normalization
        if column in dict_main["success"]["string_features"]:        
            for val in dataset[column].min():
                if val < -1:
                    dict_main["warnings"]["data_normalization"].append(column)
                    break
            else:
                dict_main["success"]["data_normalization"].append(column)
            for val in dataset[column].max():
                if val > 1:
                    dict_main["warnings"]["data_normalization"].append(column)
                    break
            else:
                dict_main["success"]["data_normalization"].append(column)

    
    values = dataset[target].value_counts()
    if (
        values[0] * DATA_IMBALANCE_THRESHOLD > values[1]
        or values[1] * DATA_IMBALANCE_THRESHOLD > values[0]
    ):
        dict["warnings"]["data_imbalance"].append("data_imbalance")
    else:
        dict["success"]["data_imbalance"].append("data_imbalance")
    

    return dict_main
