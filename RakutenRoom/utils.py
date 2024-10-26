import os
import time
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

def login_to_rakuten_room(driver):
    load_dotenv()
    username = os.getenv('RAKUTEN_LOGIN_ID')
    password = os.getenv('RAKUTEN_PASSWORD')

    # ログインページにアクセス
    login_url = 'https://grp01.id.rakuten.co.jp/rms/nid/login'
    driver.get(login_url)
    time.sleep(2)

    # ユーザー名とパスワードを入力
    driver.find_element(By.ID, 'loginInner_u').send_keys(username)
    driver.find_element(By.ID, 'loginInner_p').send_keys(password)

    # ログインボタンをクリック
    driver.find_element(By.CLASS_NAME, 'loginButton').click()
    time.sleep(5)
