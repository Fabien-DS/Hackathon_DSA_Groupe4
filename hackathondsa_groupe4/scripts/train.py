# -*- coding: utf-8 -*-
"""
This module is for training models.

Examples:
    Example command line executable::

        $ python train.py config.yml
"""
import logging

import click

from hackathondsa_groupe4.util.config import parse_config
from hackathondsa_groupe4.util.logging import setup_logging_env

logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    "config_file", type=click.Path(exists=True), default="/mnt/configs/config.yml"
)
@setup_logging_env
def _main(config_file):
    """ Train CLI Entrypoint """
    main(config_file=config_file)


def main(config_file):
    """
    Main function that loads config, sets up logging, and runs training

    Args:
        config_file (str): path to config file (for logging)

    Returns:
        None
    """
    logger.info("Training")
    logger.info(f"Loading config {config_file}")
    config = parse_config(config_file)
    logger.info(f"Config: \n{config}")


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

#Modélisation
from sklearn.metrics import mean_absolute_error, mean_squared_error, auc

#Tracking d'expérience
import mlflow
import mlflow.sklearn

#Text
import re



def scores_to_dict(score_df):
    d = score_df['train'].to_dict()
    d1 = dict(zip([x+'_train_' for x in  list(d.keys())], list(d.values())))
    d = score_df['test'].to_dict()
    d2 = dict(zip([x+'_test' for x in  list(d.keys())], list(d.values())))
    d1.update(d2)
    return d1



def score_estimator(
    estimator, X_train, X_test, df_train, df_test, target, weights,
    tweedie_powers=None, use_weights=True
):
    """Evaluate an estimator on train and test sets with different metrics"""

    metrics = [
        ("D² explained", None),   # Use default scorer if it exists
        ("mean abs. error", mean_absolute_error),
        ("mean squared error", mean_squared_error),
    ]
    if tweedie_powers:
        metrics += [(
            "mean Tweedie dev p={:.4f}".format(power),
            partial(mean_tweedie_deviance, power=power)
        ) for power in tweedie_powers]

    res = []
    for subset_label, X, df in [
        ("train", X_train, df_train),
        ("test", X_test, df_test),
    ]:
        y = df[target]
        if use_weights:
            _weights =  df[weights]
        for score_label, metric in metrics:
            if isinstance(estimator, tuple) and len(estimator) == 2:
                # Score the model consisting of the product of frequency and
                # severity models.
                est_freq, est_sev = estimator
                y_pred = est_freq.predict(X) * est_sev.predict(X)
            else:
                y_pred = estimator.predict(X)

            if metric is None:
                if not hasattr(estimator, "score"):
                    continue
                if use_weights:
                    score = estimator.score(X, y, sample_weight=_weights)
                else:
                    score = estimator.score(X, y)
            else:
                if use_weights:
                    score = metric(y, y_pred, sample_weight=_weights)
                else:
                    score = metric(y, y_pred)

            res.append(
                {"subset": subset_label, "metric": score_label, "score": score}
            )

    res = (
        pd.DataFrame(res)
        .set_index(["metric", "subset"])
        .score.unstack(-1)
        .round(4)
        .loc[:, ['train', 'test']]
    )
    return res


def random_state_params(pipe, seed):
    """Crée un dictionnaire constitué de tous les paramètres 'random_state' d'un pipe et leur assigne une valeur unique"""
    rs = re.findall(r"[a-zA-Z\_]+_random_state", ' '.join(list(pipe.get_params().keys())))
    rs=dict.fromkeys(rs, seed)
    return rs




def trainPipelineMlFlow(mlf_XP, 
                        xp_name_iter, 
                        pipeline, 
                        X_train, y_train, X_test, y_test, 
                        target_col='Frequency', 
                        weight_col='exposure', 
                        use_weights=False, 
                        fixed_params={}, 
                        opti=False, iterable_params={}):
    """
    Fonction générique permettant d'entrainer et d'optimiser un pipeline sklearn
    Les paramètres et résultats sont stockés dans MLFlow
    """
  
    mlflow.set_experiment(mlf_XP)

    with mlflow.start_run(run_name=xp_name_iter):
        
        start_time = time.monotonic()  
        
        warnings.filterwarnings("ignore")
        
        # fit pipeline
        pipeline.set_params(**fixed_params)
        if not opti:
            search = pipeline
        else:
            search = RandomizedSearchCV(pipeline, iterable_params)
        
        if use_weights:
            search.fit(X_train, y_train[target_col], sample_weight=X_train[weight_col])
        else:
            search.fit(X_train, y_train[target_col])
                
        # get params
        params_to_log = fixed_params #select initial params
        if opti:
            params_to_log.update(search.best_params_) #update for optimal solution
        mlflow.log_params(params_to_log)
        
        # Evaluate metrics
        y_pred=search.predict(X_test)
        score = score_estimator(estimator=search, 
                                         X_train=X_train, 
                                         X_test=X_test, 
                                         df_train=y_train, 
                                         df_test=y_test, 
                                         target=target_col, 
                                         weights=weight_col,
                                         use_weights=use_weights)
        
        # Print out metrics
        print(xp_name_iter)
        print("params:" % params_to_log)
        print(score)

        mlflow.log_metrics(scores_to_dict(score))
        mlflow.sklearn.log_model(pipeline, xp_name_iter)
        
        end_time = time.monotonic()
        elapsed_time = timedelta(seconds=end_time - start_time)
        print('elapsed time :', elapsed_time)
        mlflow.set_tag(key="elapsed_time", value=elapsed_time)   
        
    return search
        


if __name__ == "__main__":
    _main()
