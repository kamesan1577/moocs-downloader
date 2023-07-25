import sys
import time
import json
import glob
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) < 2:
    print("引数が足りません")
    sys.exit()
# FIXME 相対パスだとバグる？
SRC_DIR = str(sys.argv[1])
if not os.path.exists(SRC_DIR):
    print("フォルダが存在しません")
    sys.exit()
if len(sys.argv) == 3:
    DST_DIR = str(sys.argv[2])
else:
    DST_DIR = "~/Downloads"
print("src: " + SRC_DIR)
print("dst: " + DST_DIR)


chrome_options = Options()
appState = {
    "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "pageSize": "A4",
}
chrome_options.add_experimental_option(
    "prefs",
    {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        "savefile.default_directory": DST_DIR,
    },
)
chrome_options.add_argument("--kiosk-printing")

driver = webdriver.Chrome(options=chrome_options)

# ファイルかフォルダかを判定
if os.path.isfile(SRC_DIR):
    file_list = [SRC_DIR]
else:
    file_list = glob.glob(SRC_DIR + "/*.html")
print(file_list)

wait = WebDriverWait(driver, 15)
for file in file_list:
    driver.get(file)
    wait.until(EC.presence_of_all_elements_located)

    driver.execute_script("window.print();")

    time.sleep(1)
print("終了")

driver.quit()
