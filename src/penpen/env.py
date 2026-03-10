"""
環境設定モジュール
"""

import os

# データベースパス
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.getcwd(), ".env.Don't_touch_the_AI.db"))