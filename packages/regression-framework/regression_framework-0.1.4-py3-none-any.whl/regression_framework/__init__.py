from .bp import *
from .bp.regression_api import RegressionAPI
from .dmo import *
from .svc import *


def run_regression(test_case_location: str) -> None:
    RegressionAPI().process(test_case_location)
