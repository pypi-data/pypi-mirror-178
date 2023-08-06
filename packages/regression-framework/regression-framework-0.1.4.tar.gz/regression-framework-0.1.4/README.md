# Regression Framework
This microservice creates a framework for running regression tests

## Sample Test Case
The header specifies the `runner` and the `comparator`.

The `runner` is the name of the function that will be used to create the *actual results*.

The `comparator` is the name of the function that will be used to compare the *actual results* to the *expected results*.

Each test file can contain multiple test cases.

By convention, each test file should correspond to an issue in GitHub.

Each test file should test a single aspect or function of the system, using as many variations in input as are necessary to ensure the design is functional.

```yaml
engine:
  runner: "mutato"
  comparator: "mutato"
  loglevel: ERROR
  ontologies:
    - unitest

## ---------------------------------------------------------- ##
## Purpose:     Testing Swap for "Doctoral Degree"
## Reference:   https://github.com/craigtrim/owl-parse/issues/6
## ---------------------------------------------------------- ##

cases:
  - id: 06-01
    ## ---------------------------------------------------------- ##
    ##  Purpose:    Span 'doctoral degree'
    ## ---------------------------------------------------------- ##
    input: regression/inputs/tokens-0001.json
    output:
      - normal: "doctoral_degree"
```

## Driver Tutorial
Each project that implements this service will need to create a *driver*.

The driver is responsible for calling `regression-framework\regression_framework\bp\regression_api.py` with the correct parameters, as well as implementing the runner(s) and comparator(s).

### Driver
A simple but functional driver looks like this:
```python
import os
from typing import Callable
from baseblock import FileIO
from baseblock import BaseObject
from regression_framework.bp import RegressionAPI

class RegressionDriver(BaseObject):

    def __init__(self):
        BaseObject.__init__(self, __name__)

    def find_runner(self,
                    d_test_case: dict) -> Callable:

        runner_name = d_test_case['engine']['runner']

        if runner_name == "mutato":
            return self.runner

        raise NotImplementedError(runner_name)

    def find_comparator(self,
                        d_test_case: dict) -> Callable:

        runner_name = d_test_case['engine']['runner']

        if runner_name == "mutato":
            return self.comparator

        raise NotImplementedError(runner_name)

    def run(self):

        api = RegressionAPI(find_runner=self.find_runner,
                            find_comparator=self.find_comparator)

        api.process(FileIO.join_cwd("regression/cases"))
```
Note that the driver must implement a finder method for the runner and comparator.

The regression framework supports the notion of multiple runners and multiple comparators and each corresponds to this aspect of the test file:
```yaml
engine:
  runner: "mutato"
  comparator: "mutato"
```

### Runner
The runner (in this case) looks like this:
```python
def runner(self,
            ontologies: list,
            input_text: str) -> str:

    from owl_parse import owl_parse

    def get_content() -> list:
        if FileIO.exists(input_text):
            return FileIO.read_json(input_text)
        raise NotImplementedError(input_text)

    absolute_path = FileIO.join_cwd('resources/testing')

    return owl_parse(tokens=get_content(),
                        ontology_name=ontologies[0],
                        absolute_path=absolute_path)
```
It is a simple invocation of a known method, with the correct parameters, and the results are returned.

### Comparator
The comparator looks like this:
```python
def comparator(self,
                actual_results: object,
                expected_results: object) -> bool:

    def compare_normal_attribute(expected_value: str) -> bool:
        for actual_result in actual_results:
            if 'normal' in actual_result:
                if actual_result['normal'] == expected_value:
                    return True
        return False

    for expected_result in expected_results:
        if 'normal' in expected_result:
            if not compare_normal_attribute(expected_result['normal']):
                return False

    return True
```
The actual results are searched and if the expected value(s) are found, the function will return a truth value.

The full implementation is here:
https://github.com/craigtrim/regression-framework/issues/2
