"""
Linear regression module

ref:
https://www.kirenz.com/post/2021-11-14-linear-regression-diagnostics-in-python/linear-regression-diagnostics-in-python/
"""

import numpy as np
from pandas import DataFrame
from statsmodels.api import OLS
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.regression.linear_model import RegressionResults

from ostatslib.actions.utils import (ActionResult,
                                     reward_cap,
                                     interpretable_model,
                                     split_response_from_explanatory_variables)
from ostatslib.states import State


@reward_cap
@interpretable_model
def linear_regression(state: State,
                      data: DataFrame) -> ActionResult[RegressionResults]:
    """
    Fits data to a linear regression model.

    Args:
        state (State): current environment state
        data (DataFrame): data under analysis

    Returns:
        ActionResult[RegressionResults]: action result
    """
    if not __is_valid_state(state):
        return ActionResult(state, -1, "LinearRegression")

    response_var, explanatory_vars = split_response_from_explanatory_variables(state,
                                                                               data)
    try:
        regression = OLS(response_var, explanatory_vars).fit()
    except ValueError:
        return ActionResult(state, -1, "LinearRegression")

    regression = OLS(response_var, explanatory_vars).fit()
    reward = __calculate_reward(regression)
    state = __apply_state_updates(state, regression)
    return ActionResult(state, reward, regression)


def __is_valid_state(state: State) -> bool:
    if state.get("is_response_quantitative") <= 0:
        return False

    return True


def __calculate_reward(regression: RegressionResults) -> float:
    explanatory_vars: np.ndarray = regression.model.exog
    residuals: np.ndarray = regression.resid.values
    reward: float = 0

    reward += __reward_for_normally_distributed_errors(regression)
    reward += __reward_for_correlation_of_error_terms(residuals)
    reward += __reward_for_homoscedasticity(residuals, explanatory_vars)
    reward += __reward_for_model_r_squared(regression.rsquared)

    return reward


def __reward_for_normally_distributed_errors(regression: RegressionResults) -> float:
    jarque_bera_pvalue = jarque_bera(regression.wresid.values)[1]

    if jarque_bera_pvalue < .01:
        return -.2

    if jarque_bera_pvalue < .05:
        return -.1

    return .1


def __reward_for_correlation_of_error_terms(residuals: np.ndarray) -> float:
    dw_stat = durbin_watson(residuals)

    if 1 < dw_stat < 2:
        return .1

    return -.1


def __reward_for_homoscedasticity(residuals: np.ndarray,
                                  explanatory_vars: np.ndarray) -> float:
    f_stat_pvalue = het_breuschpagan(residuals, explanatory_vars)[3]

    if f_stat_pvalue < .01:
        return -.2

    if f_stat_pvalue < .05:
        return -.1

    return .1


def __reward_for_model_r_squared(rsquared: float) -> float:
    if rsquared <= .6:
        return - (1 - rsquared)

    return rsquared


def __apply_state_updates(state: State, regression: RegressionResults) -> State:
    state.set('score', regression.rsquared)
    return state
