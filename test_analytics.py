__author__ = 'Shridhar'

from ad_driver import ad_driver
from PyReport.Report import Report
import json

_browser = "chrome"
_testdata_file = "testdata/testdata.json"
_path_to_batch = "D:\\Softwares\\BrowserMob Proxy\\browsermob-proxy-2.0-beta-9\\bin\\browsermob-proxy.bat"

# Read test data from JSON file
test_data = json.load(open(_testdata_file, "r"))

# Initialize report object
report = Report()

# Initialize Ad driver
ad_driver = ad_driver(_path_to_batch, _browser)

# Execute tests and update results
for test in test_data.keys():
    requests = ad_driver.execute(test_data[test])
    report.update_result(test_data[test], requests)

# Generate report
report.create_report()

# Quit Ad driver
ad_driver.quit()

