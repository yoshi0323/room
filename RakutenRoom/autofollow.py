import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Serviceクラスをインポート
from dotenv import load_dotenv
from utils import login_to_rakuten_room

class AutoFollow:
    def __init__(self, log_area):
        load_dotenv()
        self.log_area = log_area
        self.running = True
        self.driver = None

    def log(self, message):
        self.log_area.append(message)

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()

    def run(self):
        # ChromeDriverの設定
        chrome_options = Options()
        service = Service('C:\\chromedriver-win64\\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # ログイン
        login_to_rakuten_room(self.driver)

        max_follows_per_hour = 40
        follow_count = 0

        # フォローするユーザーのページにアクセス
        self.driver.get('https://room.rakuten.co.jp/recommended/users')

        while self.running and follow_count < max_follows_per_hour:
            users = self.driver.find_elements(By.CSS_SELECTOR, 'div.userCard')
            for user in users:
                if not self.running or follow_count >= max_follows_per_hour:
                    break
                try:
                    follow_button = user.find_element(By.CLASS_NAME, 'rui-button-positive')
                    follow_button.click()
                    follow_count += 1
                    self.log(f"{follow_count}人目のユーザーをフォローしました。")
                    # ランダムな待機時間（1〜2分）
                    time.sleep(random.uniform(60, 120))
                except Exception as e:
                    self.log(f"フォロー中にエラーが発生しました: {e}")
            # 次のページがあれば進む
            try:
                next_button = self.driver.find_element(By.LINK_TEXT, '次へ')
                next_button.click()
                time.sleep(3)
            except:
                break

        self.driver.quit()
