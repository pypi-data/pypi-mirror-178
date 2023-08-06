import pandas as pd
import pytest
from .drivers.browsers import browser_os_name_conf
from .conf.rwd.Website import base_url_conf
from .utils import html_report_conf
from datetime import datetime
import os, pytest, sys, time


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


def addoption_base(parser):
    "Method to add the option to ini."
    try:
        parser.addini("rp_uuid", 'help', type="pathlist")
        parser.addini("rp_endpoint", 'help', type="pathlist")
        parser.addini("rp_project", 'help', type="pathlist")
        parser.addini("rp_launch", 'help', type="pathlist")

        parser.addoption("--browser",
                         dest="browser",
                         action="append",
                         default=[],
                         help="Browser. Valid options are ff, ie, chrome, opera, safari")
        parser.addoption("--app_url",
                         dest="url",
                         default=base_url_conf.base_url,
                         help="The url of the application")
        parser.addoption("--api_url",
                         dest="url",
                         default="http://35.167.62.251",
                         help="The url of the api")
        parser.addoption("--testrail_flag",
                         dest="testrail_flag",
                         default='N',
                         help="Y or N. 'Y' if you want to report to TestRail")
        parser.addoption("--test_run_id",
                         dest="test_run_id",
                         default=None,
                         help="The test run id in TestRail")
        parser.addoption("--remote_flag",
                         dest="remote_flag",
                         default="N",
                         help="Run the test in Browserstack/Sauce Lab: Y or N")
        parser.addoption("--os_version",
                         dest="os_version",
                         action="append",
                         help="The operating system: xp, 7",
                         default=[])
        parser.addoption("--ver",
                         dest="browser_version",
                         action="append",
                         help="The version of the browser: a whole number",
                         default=[])
        parser.addoption("--os_name",
                         dest="os_name",
                         action="append",
                         help="The operating system: Windows 7, Linux",
                         default=[])
        parser.addoption("--remote_project_name",
                         dest="remote_project_name",
                         help="The project name if its run in BrowserStack",
                         default=None)
        parser.addoption("--remote_build_name",
                         dest="remote_build_name",
                         help="The build name if its run in BrowserStack",
                         default=None)
        parser.addoption("--slack_flag",
                         dest="slack_flag",
                         default="N",
                         help="Post the test report on slack channel: Y or N")
        parser.addoption("--mobile_os_name",
                         dest="mobile_os_name",
                         help="Enter operating system of mobile. Ex: Android, iOS",
                         default="Android")
        parser.addoption("--mobile_os_version",
                         dest="mobile_os_version",
                         help="Enter version of operating system of mobile: 8.1.0",
                         default="8.0")
        parser.addoption("--device_name",
                         dest="device_name",
                         help="Enter device name. Ex: Emulator, physical device name")
        parser.addoption("--app_package",
                         dest="app_package",
                         help="Enter name of app package. Ex: com.qhms.eportal.clinicone")
        parser.addoption("--app_activity",
                         dest="app_activity",
                         help="Enter name of app activity. Ex: com.qhms.eportal.clinicone.Views.Splash.DeepLinkEntryActivity")
        parser.addoption("--device_flag",
                         dest="device_flag",
                         help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
                         default="Y")
        parser.addoption("--email_pytest_report",
                         dest="email_pytest_report",
                         help="Email pytest report: Y or N",
                         default="N")
        parser.addoption("--tesults",
                         dest="tesults_flag",
                         default='N',
                         help="Y or N. 'Y' if you want to report results with Tesults")
        parser.addoption("--app_name",
                         dest="app_name",
                         help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
                         default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
        parser.addoption("--ud_id",
                         dest="ud_id",
                         help="Enter your iOS device UDID which is required to run appium test in iOS device",
                         default=None)
        parser.addoption("--org_id",
                         dest="org_id",
                         help="Enter your iOS Team ID which is required to run appium test in iOS device",
                         default=None)
        parser.addoption("--signing_id",
                         dest="signing_id",
                         help="Enter your iOS app signing id which is required to run appium test in iOS device",
                         default="iPhone Developer")
        parser.addoption("--no_reset_flag",
                         dest="no_reset_flag",
                         help="Pass false if you want to reset app everytime you run app else false",
                         default="true")
        parser.addoption("--app_path",
                         dest="app_path",
                         help="Enter app path")
        parser.addoption("--appium_version",
                         dest="appium_version",
                         help="The appium version if its run in BrowserStack",
                         default="1.17.0")
        parser.addoption("--interactive_mode_flag",
                         dest="questionary",
                         default="n",
                         help="set the questionary flag")
        parser.addoption("--test_env",
                         dest="testenv",
                         default="",
                         help="Set testing environment. Eg. Prod, UAT",
                         required=True)
        parser.addoption("--screenshot",
                         dest="screenshot",
                         default='off',
                         help="Set on/off for screenshot feature. 3 mode can be set: 'all'/'failonly'/'off'. Default off")
        parser.addoption("--xlsx",
                         dest="xlsx",
                         default='',
                         help="Excel File name which need to get for config")
        parser.addoption("--case",
                         dest="case",
                         default="-1",
                         help="Number of case which need to run in Excel config. Do no use this option for running all cases. Input number > 0")
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


def configure(config):
    filename = 'report_' + datetime.now().strftime(
        "%Y%m%d_%H%M%S") + '_' + config.known_args_namespace.keyword + ".html"  # report_YYYYMMDD_HHMMSS_[target].html
    path = os.path.join(os.path.dirname(__file__), 'reports', filename)
    if html_report_conf.gen_report:
        config.option.htmlpath = path
