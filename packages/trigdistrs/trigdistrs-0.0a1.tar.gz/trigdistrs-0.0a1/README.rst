trigdistrs - Trigonometric Probability Distributions
----------------------------------------------------

This package presents new probability 
distributions produced by skewing regular
distribution using trigonometric functions.    
It uses symbolic computing with ```sympy.stats```
to make things easier.

See Souza 2016: NEW TRIGONOMETRIC CLASSES
OF PROBABILISTIC DISTRIBUTIONS, PhD Thesis
from Pernambuco Federal Rural University (UFRPE-Brazil),
available at <http://goo.gl/Z6nbJz>, for the origin
of the concepts.

Probability distributions are elements of 
measure theory and general statistics,
providing standardized formulas to compute
odds of events happening. These are closely
related to activaction functions in neural
networks, kernel smoothers and discriminant
functions in artificial intelligence, machine
learning and big data.

References:
* `Full Thesis <http://goo.gl/Z6nbJz>`_;
* `CosW R Package <https://cran.r-project.org/web/packages/CosW/index.html>`_;
* `SecKW R Package <https://cran.r-project.org/web/packages/SecKW/index.html>`_;
* `SinIW R Package <https://cran.r-project.org/web/packages/SinIW/index.html>`_;
* `TanB R Package <https://cran.r-project.org/web/packages/TanB/index.html>`_.
* Uses sympy;

Currently, the only thing to do is::

    >>> from trigdistrs import SecKW
    >>> # SecKW creates a random variable
    >>> # (sympy.stats.rv.RandomSymbol in
    >>> # sympy parlance)
    >>> from sympy.abc import x
    >>> Z = SecKW(x, 1, 1, 1, 1)
    >>> type(Z)
    >>> density(Z)(x)
    >>> E(Z) # This will take a very long time.
    >>> # Try also
    >>> Z = CosW(x, 1, 1)
    >>> Z = SinIW(x, 1, 1)
    >>> Z = TanB(x, 1, 1, 1)