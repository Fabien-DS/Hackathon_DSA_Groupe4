
#Temps et fichiers
import os
import warnings
import time
from datetime import timedelta

#Manipulation de données
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
from functools import partial


#Visualisation
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots





def plot_obs_pred(df, feature, weight, observed, predicted, y_label=None,
                  title_train_test=None, ax=None, fill_legend=False, output_df=False):
    """Plot observed and predicted - aggregated per feature level.

    Parameters
    ----------
    df : DataFrame
        input data
    feature: str
        a column name of df for the feature to be plotted
    weight : str
        column name of df with the values of weights or exposure
    observed : str
        a column name of df with the observed target
    predicted : DataFrame
        a dataframe, with the same index as df, with the predicted target
    fill_legend : bool, default=False
        whether to show fill_between legend
    """
    # aggregate observed and predicted variables by feature level
    df_ = df.loc[:, [feature, weight]].copy()
    df_["observed"] = df[observed] * df[weight]
    df_["predicted"] = predicted * df[weight]
    df_ = (
        df_.groupby([feature])[[weight, "observed", "predicted"]]
        .sum()
        .assign(observed=lambda x: x["observed"] / x[weight])
        .assign(predicted=lambda x: x["predicted"] / x[weight])
    )
    df_=df_.reset_index()

  
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
#        px.bar(x=df_[feature],y=df_[weight]),
        go.Bar(x=df_[feature], y=df_[weight], name="exposure"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_[feature], y=df_["observed"], mode='lines', name="observed"),
        secondary_y=True,
    )
    
    fig.add_trace(
        go.Scatter(x=df_[feature], y=df_["predicted"], mode='lines', name="predicted"),
        secondary_y=True,
    )
    

    # Add figure title
    fig.update_layout(
        title_text="Valeurs observées vs prédites par "+feature + " sur " + title_train_test
    )

    # Set x-axis title
    fig.update_xaxes(title_text=feature)

    # Set y-axes titles
    fig.update_yaxes(title_text="exposure", secondary_y=False)
    fig.update_yaxes(title_text="value", secondary_y=True)

    fig.show()
    
    if output_df:
        return df_
    


def plot_obs_pred_2(df, feature, weight, observed, use_predicted=True, predicted='', y_label=None,
                  title_train_test=None, ax=None, fill_legend=False, output_df=False):
    """Plot observed and predicted - aggregated per feature level.

    Parameters
    ----------
    df : DataFrame
        input data
    feature: str
        a column name of df for the feature to be plotted
    weight : str
        column name of df with the values of weights or exposure
    observed : str
        a column name of df with the observed target
    predicted : DataFrame
        a dataframe, with the same index as df, with the predicted target
    fill_legend : bool, default=False
        whether to show fill_between legend
    """
    # aggregate observed and predicted variables by feature level
    df_ = df.loc[:, [feature, weight]].copy()
    df_["observed"] = df[observed] * df[weight]
    if use_predicted:
        df_["predicted"] = predicted * df[weight]
        df_ = (
            df_.groupby([feature])[[weight, "observed", "predicted"]]
            .sum()
            .assign(observed=lambda x: x["observed"] / x[weight])
            .assign(predicted=lambda x: x["predicted"] / x[weight])
        )
    else:
        df_ = (
            df_.groupby([feature])[[weight, "observed"]]
            .sum()
            .assign(observed=lambda x: x["observed"] / x[weight])
        )
    df_=df_.reset_index()

  
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
#        px.bar(x=df_[feature],y=df_[weight]),
        go.Bar(x=df_[feature], y=df_[weight], name="exposure"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_[feature], y=df_["observed"], mode='lines', name="observed"),
        secondary_y=True,
    )
    
    if use_predicted:
        fig.add_trace(
            go.Scatter(x=df_[feature], y=df_["predicted"], mode='lines', name="predicted"),
            secondary_y=True,
        )
    

    # Add figure title
    fig.update_layout(
        title_text="Valeurs observées vs prédites par "+feature + " sur " + title_train_test
    )

    # Set x-axis title
    fig.update_xaxes(title_text=feature)

    # Set y-axes titles
    fig.update_yaxes(title_text="exposure", secondary_y=False)
    fig.update_yaxes(title_text="value", secondary_y=True)

    fig.show()
    
    if output_df:
        return df_
    
    
def plot_obs_pred_3(
                    df, 
                    feature, 
                    weight, 
                    observed, 
                    use_predicted=True, predicted='', 
                    use_year=False, year_field='', 
                    y_label=None,
                    title_train_test=None, 
                    ax=None, 
                    fill_legend=False, 
                    output_df=False):
    
    """Plot observed and predicted - aggregated per feature level.

    Parameters
    ----------
    df : DataFrame
        input data
    feature: str
        a column name of df for the feature to be plotted
    weight : str
        column name of df with the values of weights or exposure
    observed : str
        a column name of df with the observed target
    predicted : DataFrame
        a dataframe, with the same index as df, with the predicted target
    fill_legend : bool, default=False
        whether to show fill_between legend
    """
    # aggregate observed and predicted variables by feature level
    
    if use_year:
        df_ = df.loc[:, [year_field, feature, weight]].copy()
    else:
        df_ = df.loc[:, [feature, weight]].copy()
    
    df_["observed"] = df[observed] * df[weight]
    if use_predicted:
        df_["predicted"] = predicted * df[weight]
        if use_year:
            df_ = (
                df_.groupby([feature, year_field])[[weight, "observed", "predicted"]]
                .sum()
                .assign(observed=lambda x: x["observed"] / x[weight])
                .assign(predicted=lambda x: x["predicted"] / x[weight])
            )
        else :
            df_ = (
                df_.groupby([feature])[[weight, "observed", "predicted"]]
                .sum()
                .assign(observed=lambda x: x["observed"] / x[weight])
                .assign(predicted=lambda x: x["predicted"] / x[weight])
            )
    else:
        if use_year:
            df_ = (
                df_.groupby([feature,year_field])[[weight, "observed"]]
                .sum()
                .assign(observed=lambda x: x["observed"] / x[weight])
            )
        else:
            df_ = (
                df_.groupby([feature])[[weight, "observed"]]
                .sum()
                .assign(observed=lambda x: x["observed"] / x[weight])
            )
    df_=df_.reset_index()

  
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if use_year:
        for year in list(set(df_[year_field])):
            fig.add_trace(
                go.Bar(x=df_[feature][df_[year_field]==year], y=df_[weight][df_[year_field]==year], name="exposure_"+str(year)),
                secondary_y=False,
            )
    else:
        fig.add_trace(
            go.Bar(x=df_[feature], y=df_[weight], name="exposure"),
            secondary_y=False,
        )

    if use_year:
        for year in list(set(df_[year_field])):
            fig.add_trace(
                go.Scatter(x=df_[feature][df_[year_field]==year], y=df_["observed"][df_[year_field]==year], mode='lines', name="observed_"+str(year)),
                secondary_y=True,
            )
    else:
        fig.add_trace(
            go.Scatter(x=df_[feature], y=df_["observed"], mode='lines', name="observed"),
            secondary_y=True,
        )
    
    if use_predicted:
        if use_year:
            for year in list(set(df_[year_field])):
                fig.add_trace(
                    go.Scatter(x=df_[feature][df_[year_field]==year], y=df_["predicted"][df_[year_field]==year], mode='lines', name="predicted_"+str(year)),
                    secondary_y=True,
                )
        else:
            fig.add_trace(
                go.Scatter(x=df_[feature], y=df_["predicted"], mode='lines', name="predicted"),
                secondary_y=True,
            )
    

    # Add figure title
    fig.update_layout(
        title_text="Valeurs observées vs prédites par "+feature + " sur " + title_train_test
    )

    # Set x-axis title
    fig.update_xaxes(title_text=feature)

    # Set y-axes titles
    fig.update_yaxes(title_text="exposure", secondary_y=False)
    fig.update_yaxes(title_text="value", secondary_y=True)

    fig.show()
    
    if output_df:
        return df_
    
    
       