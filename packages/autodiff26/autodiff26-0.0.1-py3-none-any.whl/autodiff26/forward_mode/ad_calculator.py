#!/usr/bin/env python3
# File       : ad_calculator.py
# Description: Forward mode calculation
# Copyright 2022 Harvard University. All Rights Reserved.
import numpy as np
import autodiff26.forward_mode.functions as ad

def autodiff(function, **kwargs):
    """Implements the calculator

    Parameters
    ----------
    function: Function
            Function to evaluate value and derivative.
            Takes any number of inputs.
    **kwargs: Arbitrary key word arguments
            Inputs to the function to evaluate

    Examples
    --------
    >>> x_1 = np.array([0.5,1,2])
    >>> x_2 = np.array([0.5,3,4])
    >>> f = lambda x_1,x_2: ad.sin(x_1*x_2) * ad.sin(0.5)
    >>> fn = autodiff(f, x_1=x_1, x_2=x_2)
    >>> print(fn.val)
    [0.11861178 0.06765654 0.47432361]
    >>> print(fn.der)
    [ 0.46452136 -1.89851074 -0.41853859]

    Returns
    -------
    any
        ad object with primal trace and tangent trace results
        can be accessed via obj.val and obj.der respectively

    """
    return function(*[ad.FunctionClass(kwargs[key]) for key in kwargs])
