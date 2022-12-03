# This is the testbench folder for the project.
## Linting
- Linting is done using pylint.
- Currently, it checks all .py files in the "sorting_battle_gym" folder.
- To run the linter locally, run `python tests/lint.py` from the root of the project.
    - You need to have pylint installed for this to work. (use `pip install pylint`)
    - check the output of the linter to get a higher score.
- The linter will run on the GitHub Actions CI as well. If you get a socre of more than 7/10, you can proceed to unit testing.
## Unit tests
- Unit tests are done using pytest.
- To add new tests, add a .py file in the "tests" folder, make sure to name it `test_<module name>.py`.
- the class name should be `Test<module name>`.
- the test functions should be named `test_<function name>_case<X>`. (X is the test case number, starting from 1. If there is only one test case, you can omit the `_case<X>`)
- use `assert` to check the output of the function.
- To run the tests locally, run `python -m pytest` from the root of the project.
    - You need to have pytest installed for this to work. (use `pip install pytest`)
- The tests will run on the GitHub Actions CI as well. You are good to merge if all tests pass.