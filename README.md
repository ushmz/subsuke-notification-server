# Subsuke-Notification-Server

静岡大学の学生３人でやっているプロジェクト「SUBSUKE」の通知用サーバーのリポジトリ。

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
