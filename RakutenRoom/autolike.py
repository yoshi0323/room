import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Serviceクラスをインポート
from dotenv import load_dotenv
from utils import login_to_rakuten_room

class AutoLike:
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

        max_likes_per_hour = 50
        like_count = 0

        # アイテム一覧ページにアクセス
        self.driver.get('https://room.rakuten.co.jp/all/items')

        while self.running and like_count < max_likes_per_hour:
            items = self.driver.find_elements(By.CSS_SELECTOR, 'div.rn-itemCard')
            for item in items:
                if not self.running or like_count >= max_likes_per_hour:
                    break
                try:
                    like_button = item.find_element(By.CLASS_NAME, 'icon-like')
                    like_button.click()
                    like_count += 1
                    self.log(f"{like_count}件目のいいねを行いました。")
                    # ランダムな待機時間（30〜90秒）
                    time.sleep(random.uniform(30, 90))
                except Exception as e:
                    self.log(f"いいね中にエラーが発生しました: {e}")
            # 次のページがあれば進む
            try:
                next_button = self.driver.find_element(By.LINK_TEXT, '次へ')
                next_button.click()
                time.sleep(3)
            except:
                break

        self.driver.quit()
