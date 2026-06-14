#DB のテーブル構造を定義（銀行テーブル・支店テーブル）

# SQLAlchemyからテーブル定義に必要なクラス・関数をインポート
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

#==============================
# １つ目のフロー
# SQLAlchemyを使って「テーブルの設計図」を定義する
#==============================
class Base(DeclarativeBase): # ← SQLAlchemyに「テーブル管理の基地」を作る
    pass
    
#==============================
# ２つ目のフロー：銀行テーブル（banks）を定義する
# - 銀行コード（例: 0001）
# - 銀行名・漢字（例: みずほ）
# - 銀行名・カタカナ（例: ミズホ）
#==============================
#銀行テーブルの定義
class Bank(Base): # ← Baseを継承 → SQLAlchemyがテーブルとして認識
    __tablename__ = "banks" # SQLite上のテーブル名
    
    #Column クラスからインスタンスを作成して bank_code という変数に代入
    bank_code = Column(String, primary_key=True) #銀行コード(主キー)
    bank_name_kanji = Column(String, nullable=False) #銀行名(漢字):NULL禁止
    bank_name_kana = Column(String,nullable=False) #銀行名(カタカナ):NULL禁止
    
    #Branchクラスと１対多の関係を定義（１つの銀行→複数支店）
    branches = relationship("Branch", back_populates="bank")
    
    
#==============================
# 3つ目のフロー： 支店テーブル（branches）を定義する
# - 支店コード（例: 001）
# - 支店名・漢字（例: 東京営業部）
# - 支店名・カタカナ（例: トウキヨウ）
# - 銀行コード（どの銀行の支店か紐付けるため）
#==============================
#支店テーブルの定義
class Branch(Base):  ## ← Baseを継承 → SQLAlchemyがテーブルとして認識
    __tablename__ = "branches" ## SQLite上のテーブル名
    
    #支店コードと銀行名の組み合わせで主キーを構成（複合主キー）
    branch_code = Column(String, primary_key=True)
    bank_code = Column(String, ForeignKey("banks.bank_code"),primary_key=True) #銀行テーブルと紐づける外部キー
    
    #支店名の漢字:NULL禁止
    branch_name_kanji = Column(String,nullable=False)
    #支店名のカタカナ:NULL禁止
    branch_name_kana = Column(String,nullable=False)
    
    #Bankクラスと紐づけ(branch.bankで銀行用にアクセスできるようにしている)
    bank = relationship("Bank", back_populates="branches")