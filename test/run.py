import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options


# ---------------------------
# pytest fixture: 建 driver
# ---------------------------
@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"
    options.app_package = "com.android.chrome"
    options.app_activity = "com.google.android.apps.chrome.Main"

    options.set_capability("appium:chromedriverAutodownload", True)
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:ensureWebviewsHavePages", True)

    drv = appium_webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options
    )

    yield drv   # 提供給測試使用
    drv.quit()  # 測試完自動 quit


# ---------------------------
# scroll function
# ---------------------------
def scroll_down(driver, count=2):
    for _ in range(count):
        driver.execute_script("mobile: swipeGesture", {
            "left": 100,
            "top": 300,
            "width": 800,
            "height": 1400,
            "direction": "up",
            "percent": 0.85
        })


# ---------------------------
# 主測試案例（pytest）
# ---------------------------
def test_google_search(driver):

    wait = WebDriverWait(driver, 10)

    # Step 1: open Twitch
    driver.get("https://www.twitch.tv")

    # cookie popup
    try:
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
        )
        btn.click()
    except:
        pass

    # Step 2: click Browse
    MAX_RETRY = 10
    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"第 {attempt} 次找 Browse")
            browse = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@text="Browse"]'))
            )
            browse.click()
            break
        except TimeoutException:
            print("找不到 Browse")
            if attempt == MAX_RETRY:
                raise

    # Step 3: 找搜尋輸入框
    for attempt in range(1, MAX_RETRY + 1):
        try:
            search_input = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//android.view.View[@resource-id="twilight-sticky-header-root"]/android.view.View/android.widget.EditText'
                    )
                )
            )
            break
        except TimeoutException:
            print("找不到搜尋框")
            if attempt == MAX_RETRY:
                raise

    search_input.click()

    # 使用剪貼簿貼上 "StarCraft II"
    driver.set_clipboard_text("StarCraft II")
    driver.press_keycode(279)
    driver.press_keycode(66)

    # 等搜尋結果
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//android.widget.TextView[@text="View All Channel Search Results"]')
        )
    )

    # scroll
    scroll_down(driver, 1)
    time.sleep(1)
    scroll_down(driver, 1)

    # Step 4: 點第一個實況主
    for attempt in range(1, MAX_RETRY + 1):
        try:
            streamer = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//android.view.View[@resource-id="page-main-content-wrapper"]/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.Button'
                    )
                )
            )
            streamer.click()
            break
        except TimeoutException:
            print("找不到 streamer")
            if attempt == MAX_RETRY:
                raise

    # Step 5: 等 Follow → 截圖
    for attempt in range(1, MAX_RETRY + 1):
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//android.widget.Button[@text="Follow"]')
                )
            )
            time.sleep(5)
            driver.save_screenshot("pic/streamer_page.gif")
            print("Screenshot saved → streamer_page.gif")
            break
        except TimeoutException:
            print("找不到 Follow")
            if attempt == MAX_RETRY:
                raise
