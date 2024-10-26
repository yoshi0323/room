import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

def log(message):
    print(message)
    with open('C:\\Users\\RakauRoom\\RakutenRoom\\debug\\debug_log.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def take_screenshot(driver, filename):
    screenshot_path = os.path.join('C:\\Users\\RakauRoom\\RakutenRoom\\debug\\screenshots', filename)
    driver.save_screenshot(screenshot_path)
    log(f"スクリーンショットを保存しました: {screenshot_path}")

def manual_login(driver):
    log("楽天ルームのトップページにアクセスします。")
    driver.get('https://room.rakuten.co.jp/all/items')
    time.sleep(2)

    log("ログインボタンをクリックしてください。")
    input("ログイン後、Enterキーを押してください。")
    log(f"現在のURL: {driver.current_url}")

def manual_navigation(driver):
    log("マイページに進むための操作を行ってください。")
    input("マイページに移動したらEnterキーを押してください。")
    log(f"現在のURL: {driver.current_url}")

def main():
    load_dotenv()

    chrome_options = Options()
    service = Service('C:\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        manual_login(driver)
        manual_navigation(driver)
    except Exception as e:
        log(f"エラーが発生しました: {e}")
        take_screenshot(driver, 'error_screenshot.png')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
