# zengin-api

銀行名と支店を調べるAPI

## 技術スタック

- Python
- FastAPI
- SQLite
- SQLAlchemy

## ER図

```
[banks]                    [branches]
─────────────────          ──────────────────────
bank_code      PK ───┐    branch_code   PK
bank_name_kanji      └──→ bank_code     FK + PK
bank_name_kana             branch_name_kanji
                           branch_name_kana
```

## テーブル定義

### banks（銀行テーブル）

| カラム名 | 型 | 制約 | 説明 |
|---|---|---|---|
| bank_code | String | PK | 銀行コード |
| bank_name_kanji | String | NOT NULL | 銀行名（漢字） |
| bank_name_kana | String | NOT NULL | 銀行名（カタカナ） |

### branches（支店テーブル）

| カラム名 | 型 | 制約 | 説明 |
|---|---|---|---|
| branch_code | String | PK | 支店コード |
| bank_code | String | FK + PK | 銀行コード |
| branch_name_kanji | String | NOT NULL | 支店名（漢字） |
| branch_name_kana | String | NOT NULL | 支店名（カタカナ） |

## セットアップ

```bash
# 仮想環境の作成・有効化
python3 -m venv venv
source venv/bin/activate

# パッケージインストール
pip install -r requirements.txt
```
