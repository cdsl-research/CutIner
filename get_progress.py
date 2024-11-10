import gspread
from google.oauth2.service_account import Credentials

def get_progress():
    # ===========================認証周りの設定===============================
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        "./c0a21030-oauth2-d53a178680eb.json",
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    # ===========================認証周りの設定===============================

    score_per_head = {"要追加（同日3時限に再チェック）":2, "要修正（同日3時限に再チェック）":1, "OK":0, "その他（コメントに記入）":"-"}

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HuNIOcT_lS4TC6zZMQDFkxB2o3-lEZdWI2ooGTHoEgk/edit?gid=0#gid=0"

    spreadsheet = gc.open_by_url(spreadsheet_url)
    result = spreadsheet.sheet1.get_all_values()
    print(result)

    progress_score = {}
    for row in result:
        print(f"{row[0]}:{score_per_head[row[1]]}")
        progress_score[row[0]] = score_per_head[row[1]]
        
    return progress_score