#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Execute Regression Tests """


import logging
from typing import Callable

from baseblock import BaseObject, Stopwatch

from regression_framework.dmo import (RegressionExecuteComparator,
                                      RegressionExecuteRunner)


class RunRegressionTests(BaseObject):
    """ Execute Regression Tests """

    def __init__(self,
                 find_runner: Callable,
                 find_comparator: Callable):
        """ Change Log

        Created:
            6-Jun-2022
            craigtrim@gmail.com
        Updated:
            13-Sept-2022
            craigtrim@gmail.com
            *   migrated to regression-framework repo

        Args:
            find_runner (Callable): Find the appropriate regression test runner on a per test-case level
            find_comparator (Callable): Find the appropriate regression test comparator on a per test-case level
        """
        BaseObject.__init__(self, __name__)
        self._find_runner = find_runner
        self._find_comparator = find_comparator
        self._execute_test_case = RegressionExecuteRunner().process
        self._validate_output = RegressionExecuteComparator().process

    @staticmethod
    def _set_log_level(d_test_file: dict) -> None:

        if 'loglevel' not in d_test_file['engine']:
            return None

        log_level = str(d_test_file['engine']['loglevel'])

        def get_log_level():
            if log_level.upper() == 'ERROR':
                return logging.ERROR
            elif log_level.upper() == 'WARNING':
                return logging.WARNING
            if log_level.upper() == 'INFO':
                return logging.INFO
            return logging.DEBUG

        for component in ['owl-query', 'deepnlu']:
            logging.getLogger(component).setLevel(get_log_level())

    def process(self,
                d_test_cases: dict) -> None:

        sw = Stopwatch()

        errors = 0
        total_test_cases = 0

        for test_case_name in d_test_cases:
            test_case_name_only = test_case_name.split("\\")[-1]

            # retrieve the test file
            d_test_file = d_test_cases[test_case_name]
            self._set_log_level(d_test_file)

            # a test file defines a single runner and comparator
            runner = self._find_runner(d_test_file)
            comparator = self._find_comparator(d_test_file)

            # a test file defines 1..* ontologies to test with
            ontologies = d_test_file['engine']['ontologies']

            # a test file defines zero-or-more test cases
            test_cases = d_test_file['cases']
            total_test_cases += len(test_cases)

            for d_test_case in test_cases:

                expected_results = d_test_case['output']

                svcresult = self._execute_test_case(
                    runner=runner,
                    ontologies=ontologies,
                    d_test_case=d_test_case)

                is_valid = self._validate_output(
                    comparator=comparator,
                    actual_results=svcresult,
                    expected_results=expected_results)

                if not is_valid:
                    errors += 1
                    self.logger.error('\n'.join([
                        "\n" + "!"*100,
                        f"!! Failed {test_case_name_only} @ {d_test_case['id']}",
                        "!"*100 + "\n"]))

                else:
                    self.logger.debug('\n'.join([
                        "\n" + "-"*100,
                        f"-- Passed {test_case_name_only} @ {d_test_case['id']}",
                        "-"*100 + "\n"]))

        if errors:
            self.logger.error('\n'.join([
                "Regression Failure",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Errors: {errors} - {total_test_cases}"]))

        elif self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Regression Successful",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Cases: {total_test_cases}"]))
