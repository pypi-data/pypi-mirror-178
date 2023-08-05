r"""Implements Function class object function methods"""

#!/usr/bin/env python3
# File       : functions.py
# Description: Define functions and override operators
# Copyright 2022 Harvard University. All Rights Reserved.

import numpy as np
_supported_types = (int, float)
_base = np.exp(1)

class FunctionClass:
    """Function class for overrriding numeric operations in dual number operations"""

    def __init__(self, val, der=1.0):
        """Initialize FunctionClass objects"""

        self.val = val
        self.der = der


    def __add__(self, other):
        """Function that implements addition

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: w + w
        >>> a = FunctionClass(5.0)
        >>> ans = g(a)
        >>> print(ans.val)
        10.0
        >>> print(ans.der)
        2.0

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object

        """

        if isinstance(other, FunctionClass):
            return FunctionClass(self.val + other.val, self.der + other.der)
        elif isinstance(other, _supported_types):
            return FunctionClass(self.val + other, self.der)
        else:
            raise TypeError(f"Type `{type(other)}` is not supported for addition")


    def __sub__(self, other):
        """Function that implements subtraction

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: w - 2.0
        >>> a = FunctionClass(5.0)
        >>> ans = g(a)
        >>> print(ans.val)
        3.0
        >>> print(ans.der)
        1.0

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object

        """

        if isinstance(other, FunctionClass):
            return FunctionClass(self.val - other.val, self.der - other.der)
        elif isinstance(other, _supported_types):
            return FunctionClass(self.val - other, self.der)
        else:
            raise TypeError(f"Type `{type(other)}` is not supported for subtraction")


    def __mul__(self, other):
        """Function that implements multiplication rules for primal and tangent trace

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: 2*w *w*w*w
        >>> a = FunctionClass(2.0)
        >>> ans = g(a)
        >>> print(ans.val)
        32.0
        >>> print(ans.der)
        64.0

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object

        """
        if isinstance(other, FunctionClass):
            dual_part = self.val * other.der
            dual_part += other.val * self.der
            real_part = self.val * other.val
            return FunctionClass(real_part, dual_part)

        # not int/scalar
        elif not isinstance(other, _supported_types):
            raise TypeError(
                f"Type `{type(other)}` is not supported for multiplication"
            )
        else:
            return FunctionClass(self.val*other, other*self.der)


    def __str__(self):
        """Formatted output of obj val"""

        return f"Value: {self.val}, Derivative: {self.der}"


    def __rmul__(self, other):
        """Implements reflected multiplication by call __mul__"""

        return self.__mul__(other)


    def __radd__(self, other):
        """Implements reflected addition by call __add__"""
        return self.__add__(other)


    def __rsub__(self, other):
        """Implements reflected subtraction"""
        if isinstance(other, _supported_types):
            return FunctionClass(other - self.val, -self.der)
        else:
            raise TypeError(f"Type `{type(other)}` is not supported for subtraction")


    def __truediv__(self, other):
        """Function that implements true division

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda v, w : v / w
        >>> a = FunctionClass(5.0)
        >>> b = FunctionClass(2.0)
        >>> ans = g(a, b)
        >>> print(ans.val)
        2.5
        >>> print(ans.der)
        -0.75

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object
        ZeroDivisionError
            If denominator is 0
        """

        if isinstance(other, FunctionClass):
            numerator = self * FunctionClass(other.val, -other.der)
            denominator = other.val**2
            if denominator == 0:
                raise ZeroDivisionError("You cannot divide by 0")
            return FunctionClass(numerator.val/denominator, numerator.der/denominator)
        elif isinstance(other, _supported_types):
            if other == 0:
                raise ZeroDivisionError("You cannot divide by 0")
            return FunctionClass(self.val/other, self.der/other)
        else:
            raise TypeError(f"Type `{type(other)}` is not supported for division")


    def __rtruediv__(self, other):
        """Implements reflected true division"""
        if self.val == 0:
            raise ZeroDivisionError("You cannot divide by 0")
        if isinstance(other, _supported_types):
            other_class = FunctionClass(other, 0)
            return other_class / self
        else:
            raise TypeError(f"Type `{type(other)}` is not supported for division")


    def __abs__(self):
        """Function that implements absolute operation
        Parameters
        ----------
        x: FunctionClass, int, float
            input to evaluate value and derivative
        Examples
        --------
        >>> g = lambda w: abs(w)
        >>> a = FunctionClass(2.0)
        >>> ans = g(a)
        >>> print(ans.val)
        2.0
        >>> print(ans.der)
        1.0

        Returns
        -------
        FunctionClass
                Returns updated function object with value and derivative
        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object
        ZeroDivision Error
            Derivative of absolute at 0

        """
        if isinstance(self, FunctionClass):
            if self.val == 0:
                raise ZeroDivisionError("Cannot divide by 0")
            self.der = self.der * (self.val/abs(self.val))
            if self.val < 0:
                self.val = abs(self.val)
            return FunctionClass(self.val, self.der)
        elif not isinstance(self, _supported_types):
            raise TypeError(
                f"Type `{type(FunctionClass)}` is not supported for absolute"
            )


    def __pow__(self, other):
        """Function that implements power

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: w**2
        >>> w = FunctionClass(1.0)
        >>> ans = g(w)
        >>> print(ans.val)
        1.0
        >>> print(ans.der)
        2.0

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object
        ZeroDivisionError
            if trying to take log of 0
        """
        #TODO
        # if isinstance(other, FunctionClass):
        #     if self.val == 0:
        #         raise ZeroDivisionError("Cannot take log of 0")
        #     val = self.val**other.val
        #     der = (self.val**(other.val - 1))*(self.der*other.val + self.val*other.der*np.log(self.val))
        #     return FunctionClass(val, der)

        if isinstance(other, _supported_types):
            if self.val == 0 and other <= 0:
                raise ZeroDivisionError("Cannot be raised to negative power")
            val = self.val**other
            der = other*(self.val**(other-1))*self.der
            return FunctionClass(val, der)

        else:
            raise TypeError(f"Type `{type(other)}` is not supported for power operations")


    def __rpow__(self, other):
        """Function that implements reflected power

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: w**2
        >>> w = FunctionClass(1.0)
        >>> ans = g(w)
        >>> print(ans.val)
        1.0
        >>> print(ans.der)
        2.0

        Returns
        -------
        FunctionClass
                    Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object
        ZeroDivisionError
            if trying to take log of 0
        """

        raise NotImplementedError


    def __neg__(self):
        """Function that implements the negation of the input

        Parameters
        ----------
        x: FunctionClass, int, float
                input to evaluate value and derivative

        Examples
        --------
        >>> g = lambda w: -w * -12
        >>> a = FunctionClass(1.0)
        >>> ans = g(a)
        >>> print(ans.val)
        12.0
        >>> print(ans.der)
        12.0

        Returns
        -------
        FunctionClass
                Returns updated function object with value and derivative

        Raises
        ------
        TypeError
            If input not a FunctionClass, int, float Object

        """
        if isinstance(self, FunctionClass):
            self.val = self.val * -1
            self.der = self.der * -1
            return FunctionClass(self.val, self.der)
        elif not isinstance(self, _supported_types):
            raise TypeError(
                f"Type `{type(FunctionClass)}` is not supported for negation"
            ) 


def sin(x):
    """Function that implements sin rules for primal and tangent trace

    Parameters
    ----------
    x: FunctionClass, int, float
            input to evaluate value and derivative

    Examples
    --------
    >>> g = lambda w: sin(w)
    >>> a = FunctionClass(0.0)
    >>> ans = g(a)
    >>> print(ans.val)
    0.0
    >>> print(ans.der)
    1.0

    Returns
    -------
    FunctionClass
                Returns updated function object with value and derivative

    Raises
    ------
    TypeError
        If input not a FunctionClass, int, float Object

    """

    if isinstance(x, FunctionClass):
        return FunctionClass(np.sin(x.val),np.cos(x.val)*x.der)

    elif not isinstance(x, _supported_types):
        raise TypeError(
                f"Type `{type(x)}` is not supported for sin operation"
            )
    else:
        return FunctionClass(np.sin(x), 0.0)


def cos(x):
     """Function that implements cos rules for primal and tangent trace

    Parameters
    ----------
    x: FunctionClass, int, float
            input to evaluate value and derivative

    Examples
    --------
    >>> g = lambda w: cos(w)
    >>> a = FunctionClass(1.0)
    >>> ans = g(a)
    >>> print(ans.val)
    0.5403023058681398
    >>> print(ans.der)
    -0.8414709848078965

    Returns
    -------
    FunctionClass
                Returns updated function object with value and derivative

    Raises
    ------
    TypeError
        If input not a FunctionClass, int, float Object

    """

     if isinstance (x, FunctionClass):
        return FunctionClass(np.cos(x.val), -np.sin(x.val)*x.der)
     elif not isinstance(x, _supported_types):
        raise TypeError(
                f"Type `{type(x)}` is not supported for cos operation"
            )
     else:
        return FunctionClass(np.cos(x), 0.0)


def tan(x):
    """Function that implements tan rules for primal and tangent trace

    Parameters
    ----------
    x: FunctionClass, int, float
            input to evaluate value and derivative

    Examples
    --------
    >>> g = lambda w: tan(w)
    >>> a = FunctionClass(0)
    >>> ans = g(a)
    >>> print(ans.val)
    0.0
    >>> print(ans.der)
    1.0

    Returns
    -------
    FunctionClass
                Returns updated function object with value and derivative

    Raises
    ------
    TypeError
        If input not a FunctionClass, int, float Object

    """

    if isinstance(x, FunctionClass):
        return FunctionClass(np.tan(x.val), (1/(pow(np.cos(x.val), 2))) * x.der)
    elif not isinstance(x, _supported_types):
        raise TypeError(
                f"Type `{type(x)}` is not supported for tan operation"
            )
    else:
        return FunctionClass(np.tan(x), 0.0)


def exp(x):
    """Function that implements exp rules for primal and tangent trace

    Parameters
    ----------
    x: FunctionClass, int, float
            input to evaluate value and derivative

    Examples
    --------
    >>> g = lambda w: exp(w)
    >>> a = FunctionClass(0)
    >>> ans = g(a)
    >>> print(ans.val)
    1.0
    >>> print(ans.der)
    1.0

    Returns
    -------
    FunctionClass
                Returns updated function object with value and derivative

    Raises
    ------
    TypeError
        If input not a FunctionClass, int, float Object

    """
    if isinstance(x, FunctionClass):
        return FunctionClass(np.exp(x.val), (np.exp(x.val))*x.der)
    elif not isinstance(x, _supported_types):
        raise TypeError(
                f"Type `{type(x)}` is not supported for exp operation"
            )
    else:
        return FunctionClass(np.exp(x), 0.0)


def log(x, base=_base):
    """Function that implements log rules for primal and tangent trace

    Parameters
    ----------
    x: FunctionClass, int, float
            input to evaluate value and derivative

    Examples
    --------
    >>> g = lambda w: log(w)
    >>> a = FunctionClass(1)
    >>> ans = g(a)
    >>> print(ans.val)
    0.0
    >>> print(ans.der)
    1.0

    Returns
    -------
    FunctionClass
                Returns updated function object with value and derivative

    Raises
    ------
    TypeError
        If input not a FunctionClass, int, float Object
    ValueError
        If trying to take the log of non positive number

    """

    if isinstance(x, FunctionClass):
        if x.val <= 0 or base == 1:
            raise ValueError("Cannot take log of non-positive values")
        return FunctionClass(np.log(x.val) / np.log(base), 
                             x.der / (x.val * np.log(base)))

    elif not isinstance(x, _supported_types):
        raise TypeError(
                f"Type `{type(x)}` is not supported for logarithm operation"
            )

    else:
        if x <= 0 or base == 1:
            raise ValueError("Cannot take the logarithm of non-positive values")
        return FunctionClass(np.log(x) / np.log(base), 0.0)
