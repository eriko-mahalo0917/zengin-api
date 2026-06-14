#SQLite への接続設定
#==============================
# 必要なライブラリをインポートする
#==============================
#エンジン（接続口）を作る関数
from sqlalchemy import create_engine
#セッション（窓口）を作る関数
from sqlalchemy.orm import sessionmaker
#logger
from utils.logger import SimpleLogger

#loggerのセットアップ
logger_setup = SimpleLogger()
logger = logger_setup.get_logger()

#==============================
# 1つ目のフロー
# SQLiteのDBファイルの場所を指定する
# → zengin.db というファイルをどこに作るか決める
#==============================
#DBファイルのパスを指定する（sqlite:/// の後にファイルパスを書く）
#お決まりなので sqlite:///./ファイル名.db
DATABASE_URL = "sqlite:///./zengin.db"

#==============================
# 2つ目のフロー
# エンジンを作る
# → PythonとSQLiteをつなぐ接続口を作る
#==============================
logger.info("DBエンジンを作成を開始します")

# インスタンスを作成
# 1つ目で指定した場所を渡す → SQLAlchemyが接続の準備をする 
zengin_db_engine = create_engine(DATABASE_URL)
logger.info("DBエンジンを作成しました")


#==============================
# 3つ目のフロー
# セッションを作る（DBへの読み書きの窓口）
# → APIにリクエストが来るたびに作り、レスポンスを返したら閉じる
#==============================
# sessionmakerクラスからインスタンスを作成（セッションの設定を定義する）
# bind: どのDBを使うか指定 / autocommit・autoflush: 誤操作防止のためFalse ※自動でDBに保存しない設定
# 「全部成功したら保存、1つでも失敗したら全部取り消す」という考え方をトランザクション
# セッション → DBへの「作業単位」（リクエストごとに作って使い終わったら閉じる）
SessionLocal = sessionmaker(bind=zengin_db_engine, autocommit=False, autoflush=False)
logger.info("セッションを作成しました")

#==============================
# 4つ目のフロー
# テーブルを実際にSQLiteに作成する
# → db_tables.py の設計図をもとにDBファイルにテーブルを生成する
#==============================

# db_tables.py の Base をインポート
from db_tables import Base

# zengin.db にテーブルを生成する（既に存在する場合はスキップ）
# Base には Bank と Branch の設計図が紐づいている
Base.metadata.create_all(zengin_db_engine)
logger.info("テーブルを作成しました")