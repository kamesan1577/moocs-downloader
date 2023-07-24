from time import sleep
import os
import sys
import subprocess
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


INIAD_ID = os.environ.get("INIAD_ID") 
INIAD_PW = os.environ.get("INIAD_PW")
INIAD_CHROME_PROFILE = os.environ.get("INIAD_CHROME_PROFILE") # Chromeのプロフィール名
CHROME_USER_DATA_PATH = os.environ.get("CHROME_USER_DATA_PATH") # profileフォルダがあるフォルダ
base_url = "https://moocs.iniad.org"
chrome_options = Options()

chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_PATH}")
chrome_options.add_argument(f"--profile-directory={INIAD_CHROME_PROFILE}")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


print("stop_all_chrome_prcess")
cmd = "taskkill /im chrome.exe /f"
returncode = subprocess.call(cmd)
print(returncode)

driver = webdriver.Chrome(options=chrome_options)
driver.get(base_url)


def search_course(search_word):
    courses = driver.find_elements(By.CLASS_NAME, "media")
    for course in courses:
        course_title = course.find_element(By.CLASS_NAME, "media-heading")
        course_button = course.find_element(By.CLASS_NAME, "btn-primary")
        course_url = course_button.get_attribute("href")

        if search_word in course_title.text:
            print(course_title.text)
            return course_url

        elif search_word in f"{base_url}{course_url}":
            print(course_title.text)
            return course_url
    print("該当するコースが見つかりませんでした")
    return None


def get_lecture_list():
    table_of_contents = driver.find_elements(By.CLASS_NAME, "treeview")
    lectures = []
    for content in table_of_contents:
        for lecture in content.find_elements(By.TAG_NAME, "li"):
            lectures.append(
                lecture.find_element(By.TAG_NAME, "a").get_attribute("href")
            )
    return lectures


def get_page_list_of_lecture():
    page_list = [driver.current_url]
    for page in driver.find_elements(By.CLASS_NAME, "pagination"):
        for page_li in page.find_elements(By.TAG_NAME, "li"):
            if not "#" in page_li.find_element(By.TAG_NAME, "a").get_attribute("href"):
                page_list.append(
                    page_li.find_element(By.TAG_NAME, "a").get_attribute("href")
                )
    page_list = list(set(page_list))
    return page_list


# INIADdedが入ってないと使えない
def download_slide():
    # FIXME 映像があるとバグる

    if len(driver.find_elements(By.CLASS_NAME, "embed-responsive")) > 0:
        slide = driver.find_element(By.CLASS_NAME, "embed-responsive")

        # FIXME クリックはできるけど全然スライドのURLを叩いてくれない
        # 映像がある場合はスライド切り替えボタンを押す
        nav_tabs = driver.find_elements(By.CLASS_NAME, "nav-tabs")
        if len(nav_tabs) > 0:
            print("映像があるのでスライド切り替えボタンを押します")
            nav_tabs[0].find_elements(By.TAG_NAME, "li")[1].click()

        slide_url = slide.find_element(By.TAG_NAME, "iframe").get_attribute("src")
        driver.get(slide_url + "&download=true")


# ログイン
if driver.current_url == f"{base_url}/signin":
    go_to_auth_button = driver.find_element(
        By.XPATH, "/html/body/div/div/div/div[2]/p[2]/a"
    )
    go_to_auth_button.click()
    sleep(1)
    user_name = driver.find_element(By.ID, "username")
    user_name.send_keys(f"{INIAD_ID}")
    password = driver.find_element(By.ID, "password")
    password.send_keys(f"{INIAD_PW}")

    login_button = driver.find_element(By.ID, "kc-login")
    login_button.click()

if driver.current_url == f"{base_url}/courses":
    print("ログイン成功")
    search_word = sys.argv[1] if len(sys.argv) > 1 else "ネットワーク"
    course_url = search_course(search_word)
    driver.get(course_url)
    lectures = get_lecture_list()
    for lecture in lectures:
        print(lecture)
        driver.get(lecture)
        pages = get_page_list_of_lecture()
        print("ページ一覧: " + str(pages))
        for page in pages:
            print("現在のページ: " + page)
            driver.get(page)
            download_slide()
print("終了")
sleep(5)
driver.quit()
