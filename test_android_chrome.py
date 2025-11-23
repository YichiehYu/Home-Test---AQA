from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.common.exceptions import TimeoutException

from appium import webdriver
from appium.options.android import UiAutomator2Options
# cmd
#下載nodejs安裝好path sdk tool等
# appium --address 0.0.0.0 --port 4723 --relaxed-security

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.wait import WebDriverWait


def create_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"
    # options.browser_name = "Chrome"
    options.app_package = "com.android.chrome"
    options.app_activity = "com.google.android.apps.chrome.Main"

    # ⭐ 正確開啟自動下載（注意 key 名稱 & appium: 前綴）
    options.set_capability("appium:chromedriverAutodownload", True)

    # ===== 建議新增（讓 Chrome 不會重新初始化） =====
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:ensureWebviewsHavePages", True)

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options
    )
    return driver


def test_google_search():
    driver = create_driver()

    # ====== SETUP ======


    # ====== Step 1: go to Twitch ======
    driver.get("https://www.twitch.tv")

    # 移除 cookie popup（如果有）
    try:
        accept_btn =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]")))
        accept_btn.click()
    except:
        pass



    # ====== Step 2: click search icon ======
    # search_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Browse']")))

    MAX_RETRY = 10

    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"第 {attempt} 次嘗試找 Browse 按鈕")
            search_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@text="Browse"]')))
            search_icon.click()
            break
        except TimeoutException:
            print(f" 第 {attempt} 次找不到 Browse")
            if attempt == MAX_RETRY:
                raise






    # ====== Step 3: input "StarCraft II" ======

    MAX_RETRY = 10

    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"第 {attempt} 次嘗試找 Browse 按鈕")
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                           '//android.view.View[@resource-id="twilight-sticky-header-root"]/android.view.View/android.widget.EditText')))
            break
        except TimeoutException:
            print(f" 第 {attempt} 次找不到 Browse")
            if attempt == MAX_RETRY:
                raise

    print(search_input.get_attribute("class"))
    print(search_input.get_attribute("focusable"))
    print(search_input.get_attribute("clickable"))
    print(search_input.get_attribute("text"))
    print(search_input.get_attribute("content-desc"))
    # 點一下輸入框（讓光標出現）
    search_input.click()

    driver.set_clipboard_text("StarCraft II")
    driver.press_keycode(279)
    driver.press_keycode(66)




    View_All = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                   '//android.widget.TextView[@text="View All Channel Search Results"]')))

    # ====== Step 4: scroll down ======

    def scroll_down(driver, count=2):
        for i in range(count):
            driver.execute_script("mobile: swipeGesture", {
                "left": 100,
                "top": 300,
                "width": 800,
                "height": 1400,
                "direction": "up",
                "percent": 0.85
            })

    # 用法
    scroll_down(driver, 1)
    time.sleep(2)

    scroll_down(driver, 1)

    MAX_RETRY = 10

    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"第 {attempt} 次嘗試找 Browse 按鈕")
            # 選第一個實況主（Streamer）
            streamer = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//android.view.View[@resource-id="page-main-content-wrapper"]/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.Button'))
            )
            streamer.click()
            break
        except TimeoutException:
            print(f" 第 {attempt} 次找不到 Browse")
            if attempt == MAX_RETRY:
                raise


    MAX_RETRY = 10

    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"第 {attempt} 次嘗試找 Browse 按鈕")
            #  等 Streamer Page 影片載入 → 截圖
            follow = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="Follow"]')))
            time.sleep(5)

            driver.save_screenshot("streamer_page.png")
            print("Screenshot saved → streamer_page.png")
            break
        except TimeoutException:
            print(f" 第 {attempt} 次找不到 Browse")
            if attempt == MAX_RETRY:
                raise


    driver.quit()


if __name__ == "__main__":
    test_google_search()
