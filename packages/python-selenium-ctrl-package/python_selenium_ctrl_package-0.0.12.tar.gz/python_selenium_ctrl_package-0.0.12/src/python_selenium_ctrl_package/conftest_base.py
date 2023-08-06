import pandas as pd
import pytest


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
