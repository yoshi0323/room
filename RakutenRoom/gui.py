import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from threading import Thread
from autopost import AutoPost
from autofollow import AutoFollow
from autolike import AutoLike

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.auto_post = None
        self.auto_follow = None
        self.auto_like = None

    def initUI(self):
        # ボタンの作成
        self.post_start_btn = QPushButton('自動投稿スタート', self)
        self.post_stop_btn = QPushButton('自動投稿停止', self)
        self.follow_start_btn = QPushButton('自動フォロースタート', self)
        self.follow_stop_btn = QPushButton('自動フォロー停止', self)
        self.like_start_btn = QPushButton('自動いいねスタート', self)
        self.like_stop_btn = QPushButton('自動いいね停止', self)

        # ログ表示エリア
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)

        # レイアウト設定
        vbox = QVBoxLayout()
        vbox.addWidget(self.post_start_btn)
        vbox.addWidget(self.post_stop_btn)
        vbox.addWidget(self.follow_start_btn)
        vbox.addWidget(self.follow_stop_btn)
        vbox.addWidget(self.like_start_btn)
        vbox.addWidget(self.like_stop_btn)
        vbox.addWidget(QLabel('ログ：'))
        vbox.addWidget(self.log_area)

        self.setLayout(vbox)

        # ウィンドウ設定
        self.setWindowTitle('楽天ルーム自動化ツール')
        self.setGeometry(300, 300, 400, 500)
        self.show()

        # ボタンの動作を設定
        self.post_start_btn.clicked.connect(self.start_auto_post)
        self.post_stop_btn.clicked.connect(self.stop_auto_post)
        self.follow_start_btn.clicked.connect(self.start_auto_follow)
        self.follow_stop_btn.clicked.connect(self.stop_auto_follow)
        self.like_start_btn.clicked.connect(self.start_auto_like)
        self.like_stop_btn.clicked.connect(self.stop_auto_like)

    def start_auto_post(self):
        self.log_area.append('自動投稿を開始します。')
        self.auto_post = AutoPost(self.log_area)
        self.post_thread = Thread(target=self.auto_post.run)
        self.post_thread.start()

    def stop_auto_post(self):
        if self.auto_post:
            self.auto_post.stop()
            self.log_area.append('自動投稿を停止しました。')

    def start_auto_follow(self):
        self.log_area.append('自動フォローを開始します。')
        self.auto_follow = AutoFollow(self.log_area)
        self.follow_thread = Thread(target=self.auto_follow.run)
        self.follow_thread.start()

    def stop_auto_follow(self):
        if self.auto_follow:
            self.auto_follow.stop()
            self.log_area.append('自動フォローを停止しました。')

    def start_auto_like(self):
        self.log_area.append('自動いいねを開始します。')
        self.auto_like = AutoLike(self.log_area)
        self.like_thread = Thread(target=self.auto_like.run)
        self.like_thread.start()

    def stop_auto_like(self):
        if self.auto_like:
            self.auto_like.stop()
            self.log_area.append('自動いいねを停止しました。')
