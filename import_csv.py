#import_csv.py  → CSVをDBに取り込む
#==============================
# 必要なライブラリをインポートする
#==============================
import csv
from utils.logger import SimpleLogger
from database import SessionLocal
from db_tables import Bank, Branch

#loggerのセットアップ
logger_setup = SimpleLogger()
logger = logger_setup.get_logger()

#==============================
# 1つ目のフロー
# CSVファイルを開いて読み込む
# → data/zengin.csv を1行ずつ読み込む
#==============================
CSV_FILE_PATH = "data/zengin.csv"

with open(CSV_FILE_PATH, mode="r", newline="", encoding="utf-8-sig") as csn_file:
    # 1行目のヘッダーをキーとして辞書形式で読み込む
    # DictReader で読み込むとこうなる→{"銀行コード": "0001", "銀行名（漢字）": "みずほ", "支店コード": "001", ...}
    reader = csv.DictReader(csn_file)
    logger.info("CSVファイルを開きました: {CSV_FILE_PATH}")
    
    
    #==============================
    # 2つ目のフロー
    # DBのセッションを開始する
    # → database.py で作った SessionLocal を使う
    #==============================
    # SessionLocal() を呼び出して新しいセッション（作業単位）を開始する
    # インスタンス作成
    #database.py で作った SessionLocal を呼び出してセッションのインスタンスを作成。これでDBへの読み書きができる状態になる
    session = SessionLocal()
    logger.info("DBのセッションを開始しました")

    #==============================
    # 3つ目のフロー
    # 1行ずつ銀行テーブル・支店テーブルに振り分ける
    # → 銀行コードが初登場なら banks に追加
    # → 支店情報は毎行 branches に追加
    #==============================
    # setクラスのインスタンスを作成（重複を自動で除外する組み込みクラス）
    # 「追加済みの銀行コード一覧」を管理する → 同じ銀行コードの重複追加を防ぐ
    added_bank_codes = set()

    # 1つ目のフローで読み取ったCSVを1行ずつ辞書として取得する
    # row = {"銀行コード": "0001", "銀行名（漢字）": "みずほ", ...}
    for row in reader:
        
        #銀行コードを取得して変数に入れる
        bank_code = row["銀行コード"]
        
        #銀行コードが初登場の時だけbanksテーブルに追加する
        if bank_code not in added_bank_codes:
            
            #Bankクラスのインスタンスを作成(カラム名=値で渡す)
            bank = Bank(
                bank_code = bank_code, 
                bank_name_kanji = row["銀行名（漢字）"],
                bank_name_kana = row["銀行名（カタカナ）"]
            )
            
            #セッションの追加(まだDBに追加されない)
            session.add(bank)
            
            #追加済みとして記録
            added_bank_codes.add(bank_code)
            
        #支店情報は全ての行をbranchesテーブルに追加する
        branch = Branch(
            branch_code=row["支店コード"],
            bank_code=bank_code,
            branch_name_kanji=row["支店名（漢字）"],
            branch_name_kana=row["支店名（カタカナ）"]
        )
        
        #セッションの追加(まだDBに追加されない)
        session.add(branch)
    logger.info(f"CSVの読み込みが完了しました：{len(added_bank_codes)}銀行")
    



#==============================
# 4つ目のフロー
# DBに保存する
# → commit() で確定・session を閉じる
#==============================
