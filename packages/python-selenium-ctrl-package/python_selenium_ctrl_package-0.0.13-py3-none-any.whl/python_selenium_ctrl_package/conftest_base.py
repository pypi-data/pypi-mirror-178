import pandas as pd
import pytest
from .drivers.browsers import browser_os_name_conf


@pytest.fixture
def testname(request):
    "pytest fixture for testname"
    try:
        name_of_test = request.node.name
        name_of_test = name_of_test.split('[')[0]

        return name_of_test

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def test_run_id(request):
    "pytest fixture for test run id"
    try:
        return request.config.getoption("--test_run_id")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def cases(request):
    name = request.config.getoption("--xlsx")
    testID = request.node.own_markers[0].args[1][0][1]
    sheet = "Context"
    df = pd.read_excel("././conf/web/" + request.node.funcargs.get('product') + '/' + name, sheet_name=sheet, dtype=str,
                       usecols=lambda x: 'Remark' not in x)
    df = df.fillna('')
    row = df.index[df['testID'] == testID].tolist()
    data = (df.loc[row[0]])
    return data


@pytest.fixture
def testrail_flag(request):
    "pytest fixture for test rail flag"
    try:
        return request.config.getoption("--testrail_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def browser(request):
    """pytest fixture for browser, default browser set in here by config
    Originally default browser browser_os_name_conf when using pytest and logic set in conftest.py pytest_generate_tests() hook
    However pytest-bdd is not working with that hook, therefore comments that hook"""
    name = browser_os_name_conf.default_browser
    try:
        if len(request.config.getoption("--browser")) != 0:
            name = request.config.getoption("--browser")[0].lower()
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))
    return name

