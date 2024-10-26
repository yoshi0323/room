import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Serviceクラスをインポート
from dotenv import load_dotenv
import openai
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoPost:
    def __init__(self, log_area):
        load_dotenv()
        self.log_area = log_area
        self.running = True
        self.driver = None
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.rakuten_api_key = os.getenv('RAKUTEN_API_KEY')
        openai.api_key = self.openai_api_key

    def log(self, message):
        self.log_area.append(message)
        print(message)  # コンソールにも表示

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()

    def get_items(self, genre_id):
        url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
        params = {
            'applicationId': self.rakuten_api_key,
            'genreId': genre_id,
            'hits': 30,
            'sort': '-reviewCount',
            'format': 'json'
        }
        response = requests.get(url, params=params)
        items = response.json()['Items']
        return items

    def generate_description(self, item):
        prompt = f"""
以下の商品について、魅力的な紹介文を書いてください。

商品名: {item['itemName']}
商品説明: {item['itemCaption']}

#商品ページの解説からどんな商品か把握してください
#把握した内容から、ユーザーが興味を引くように文章を考えてください
#堅苦しくなく、自然で優しい言葉遣いで、絵文字なども使い心を惹かれる内容にしてください
#文末に必ずハッシュタグを3つつけてください

紹介文:
"""
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        description = response.choices[0].text.strip()
        return description

    def run(self):
        # ChromeDriverの設定
        chrome_options = Options()
        service = Service('C:\\chromedriver-win64\\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # 楽天ルームトップページにアクセス
        self.driver.get('https://room.rakuten.co.jp/all/items')
        time.sleep(2)  # ページが読み込まれるのを待つ
        self.log(f"現在のURL: {self.driver.current_url}")

        # ログインボタンをクリックするために待機
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="feed_wrapper"]/div[1]/div/div/a[2]'))
        )
        login_button.click()
        time.sleep(2)  # ログイン画面が表示されるのを待つ
        self.log(f"現在のURL: {self.driver.current_url}")

        # ログイン処理を呼び出す
        login_to_rakuten_room(self.driver)

        # マイページへの遷移を行う
        self.log("マイページに進むための操作を行います。")
        my_room_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ng-app"]/body/div[2]/div/div[1]/header/ul/li[4]/a'))
        )
        my_room_button.click()
        time.sleep(2)  # マイページが表示されるのを待つ
        self.log(f"現在のURL: {self.driver.current_url}")

        # ここから以降の自動操作を追加
        genre_ids = ['100371', '215783', '558929']  # 各ジャンルのIDを設定

        post_count = 0
        max_posts_per_day = 100

        while self.running and post_count < max_posts_per_day:
            genre_id = random.choice(genre_ids)
            items = self.get_items(genre_id)
            for item_wrapper in items:
                if not self.running or post_count >= max_posts_per_day:
                    break
                item = item_wrapper['Item']
                item_url = item['itemUrl']
                description = self.generate_description(item)
                self.post_item(item_url, description)
                post_count += 1
                self.log(f"{post_count}件目の投稿を行いました。")
                time.sleep(random.uniform(300, 600))  # ランダムな待機時間

        self.driver.quit()

    def post_item(self, item_url, description):
        try:
            # 楽天ルームの投稿ページにアクセス
            self.driver.get('https://room.rakuten.co.jp/myroom/collect')

            # 商品URLを入力
            item_url_field = self.driver.find_element(By.ID, 'collectItemUrl')
            item_url_field.clear()
            item_url_field.send_keys(item_url)

            # 「検索」ボタンをクリック
            search_button = self.driver.find_element(By.ID, 'collectSearchButton')
            search_button.click()

            time.sleep(3)

            # コメントを入力
            comment_field = self.driver.find_element(By.ID, 'collect-content')
            comment_field.clear()
            comment_field.send_keys(description)

            # 「コレ！」ボタンをクリック
            collect_button = self.driver.find_element(By.CLASS_NAME, 'collect-btn')
            collect_button.click()

            time.sleep(3)
        except Exception as e:
            self.log(f"投稿中にエラーが発生しました: {e}")
