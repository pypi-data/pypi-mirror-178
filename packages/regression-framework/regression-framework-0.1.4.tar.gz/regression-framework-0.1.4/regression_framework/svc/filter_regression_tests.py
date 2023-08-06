#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Filter Selected Regression Tests based on User-Supplied Criteria """


from baseblock import BaseObject, EnvIO, Stopwatch


class FilterRegressionTests(BaseObject):
    """ Filter Selected Regression Tests based on User-Supplied Criteria """

    def __init__(self):
        """ Change Log

        Created:
            6-Jun-2022
            craigtrim@gmail.com
        Updated:
            13-Sept-2022
            craigtrim@gmail.com
            *   migrated to regression-framework repo
        """
        BaseObject.__init__(self, __name__)

    def _process(self,
                 d_test_cases: dict) -> list:

        filter_on = EnvIO.str_or_default('REGRESSION_FILENAME', '*')
        if filter_on == "*":
            return d_test_cases

        # return [x for x in test_cases if filter_on in x]
        return {k: d_test_cases[k] for k in d_test_cases if filter_on in k}

    def process(self,
                d_test_cases: dict) -> dict:

        sw = Stopwatch()

        d_test_cases = self._process(d_test_cases)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Filtered Test Cases",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Files: {len(d_test_cases)}"]))

        return d_test_cases
