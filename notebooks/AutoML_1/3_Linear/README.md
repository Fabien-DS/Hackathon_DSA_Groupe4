# Summary of 3_Linear

[<< Go back](../README.md)


## Linear Regression (Linear)
- **n_jobs**: -1
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True

## Optimized metric
rmse

## Training time

3.0 seconds

### Metric details:
| Metric   |     Score |
|:---------|----------:|
| MAE      |  3.43952  |
| MSE      | 25.4665   |
| RMSE     |  5.04643  |
| R2       |  0.683816 |
| MAPE     |  0.169812 |



## Learning curves
![Learning curves](learning_curves.png)

## Coefficients
| feature   |   Learner_1 |
|:----------|------------:|
| RM        |  0.351415   |
| RAD       |  0.247805   |
| B         |  0.106781   |
| ZN        |  0.0963366  |
| CHAS      |  0.0860307  |
| INDUS     |  0.0529975  |
| intercept | -0.00545265 |
| AGE       | -0.00607618 |
| CRIM      | -0.117524   |
| NOX       | -0.126194   |
| PTRATIO   | -0.190825   |
| TAX       | -0.224165   |
| DIS       | -0.297743   |
| LSTAT     | -0.448304   |


## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)
## True vs Predicted

![True vs Predicted](true_vs_predicted.png)


## Predicted vs Residuals

![Predicted vs Residuals](predicted_vs_residuals.png)



## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence (Fold 1)
![SHAP Dependence from Fold 1](learner_fold_0_shap_dependence.png)

## SHAP Decision plots

### Top-10 Worst decisions (Fold 1)
![SHAP worst decisions from fold 1](learner_fold_0_shap_worst_decisions.png)
### Top-10 Best decisions (Fold 1)
![SHAP best decisions from fold 1](learner_fold_0_shap_best_decisions.png)

[<< Go back](../README.md)
