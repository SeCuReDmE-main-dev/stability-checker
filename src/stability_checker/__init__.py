"""stability-checker: which travel insurance stability clauses does a traveller meet?"""
from .checker import CHANGES, CONDITIONS, Result, check, coverage, load_plans

__all__ = ["CHANGES", "CONDITIONS", "Result", "check", "coverage", "load_plans"]
__version__ = "0.3.0"
