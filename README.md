# Subsuke-Notification-Server(アーカイブ済み)

静岡大学の学生３人でやっているプロジェクト「SUBSUKE」の通知用サーバーのリポジトリ。（**アーカイブ済み**）
開発は[このリポジトリ](https://github.com/ushmz/subsuke)で継続中。

## 開発環境 (2020/3/5時点)
- Mac
- Python
- Flask
- heroku

## ディレクトリ構成
```
subsuke-notification-server
┣ _test_  # テスト用
┣ venv    # 実行用venv環境
┃
┣ .gitignore
┣ NotificationScheduler.py    # プッシュ通知を定期実行するためのモジュール
┣ Procfile                    # heroku上での起動コマンドを示すファイル
┣ SQLRepository.py            # O/Rマッパーもどき
┣ Service.py                  # ロジック部分をまとめたモジュール
┣ SinigletonScheduler.py      # プッシュ通知を管理するモジュール
┣ requirements.txt            # herokuで実行する場合に必要なパッケージ情報
┗ run.py                      # 起動スクリプト
```

## 関数orメソッドorクラス名 引数 戻り値 機能 使用箇所 など

class SQLRepository　清水さん作
- 機能：各種プッシュ通知をDBに保存し、支払い周期のデータを適宜更新

def getConnecton(self):
- 引数:self 
- 機能:データベースとのコネクションを取得 host port user password database を二次元配列から取得？　 iniファイルに何か書いてあるっぽい。後で確認。
- 

os.environ
- 環境変数の操作を行う
- .get("文字列")で(多分中身が辞書型に近い記述)文字列の値を取得出来る。

def registorUserToken(self, token, name=None):
- プッシュ通知トークンをDBに保存するメソッド

psql
- psycopg2モジュールの中で定義されている?
- PostgreSQLでサーバにアクセスする操作らしい
- .connect()に引数はデータベースのURLを送るとなにか返ってくる


def schedulePushNotification(self, rowid, token, message, cycle, date):
- プッシュ通知をDBに保存するメソッド．
- Expoプッシュトークン　通知本文　支払い周期　次回通知予定日 を扱う
- 

def collectAllonSchedule(self):
- 一日一回，その日に送信する通知を返却する．返却とは？
- 
- 

def updateSchedule(self, pendingId, token):
- 支払い周期に応じて次回通知日を更新する．
- selfで渡されたものをごちゃごちゃすると支払い周期("週", "月","年")の文字列が取得されてそれを条件分岐でupdateの頻度を変えている。
- 

def cancelScheduling(self, rowid, token):
- POSTされたIDの通知スケジュールを削除する．
- 多分アプリで削除した時に呼び出される
- deleteのSQLを送る
