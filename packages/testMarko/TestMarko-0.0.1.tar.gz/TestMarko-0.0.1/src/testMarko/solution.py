import copy
from math import e, inf
import math

class Solution:

    math_error_count = 0
    fit_calls = 0
    fit_fails = 0

    @classmethod
    def clearStats(cls):
        cls.math_error_count=0
        cls.fit_fails = 0
        cls.fit_calls=0

    def __init__(self, factors, complexity_penalty):
        # factors are basically subexpressions that enter linear combination, e.g. 2*x+3y*sin(x*y) --> factors = [2x, 3y*sin(x*y)]
        self.factors =  copy.deepcopy(factors)
        self.complexity_penalty = complexity_penalty

    def __str__(self) -> str:
        return "+".join([str(x) for x in self.factors])
