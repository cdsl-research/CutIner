import os
import re
import datetime

def get_PS_access(IPaddress, alert_time):
    """物理サーバの障害発生時刻の直前(アラート発生時刻の18分前から3分前の15分間)にVMが使用されていた時間の取得

    Args:
        IPaddress (str): アラートのinstance(障害発生箇所)のIPアドレス
        alert_time (str): アラート発生時刻(YYYY-MM-DD HH:MM:SS)
    
    Returns:
        used_VM_datas (dict): 物理サーバの障害発生時刻の直前にVMが使用されていた時間の辞書
            key:
                - vm_hostname (str): vmのホスト名
            value:
                - used_time (int): vmの使用時間(分)
        hostname (str): 物理サーバのホスト名
        before_time (int): 直前の時間範囲
    """
    ## ホスト名とIPアドレスの対応を保持した辞書
    hostnames = {"192.168.100.21":"plum",
                 "192.168.100.22":"jasmine",
                 "192.168.100.23":"rose",
                 "192.168.100.24":"lotus",
                 "192.168.100.25":"violet",
                 "192.168.100.26":"mint",
                 "192.168.100.27":"lily",
                 }
    
    hostname = hostnames[IPaddress] # 今回取得したい対象のIPaddress
    get_start_time = 18 # アラート発生時刻から何分前を取得開始時間とするのか
    get_end_time = 3 # アラート発生時刻から何分前を取得終了時間とするのか
    before_time = get_start_time - get_end_time
    data_location = f"/home/c0a21030/develop2/last_datas/{hostname.capitalize()}" # VMが使用されていた時間のデータが保存されたディレクトリ
    files = [] # VMのホスト名の後ろにLASTとついているファイル名のリスト
    alert_time = datetime.datetime.strptime(alert_time, "%Y-%m-%d %H:%M:%S") # アラート発生時刻を日付型に変換
    alert_time = alert_time + datetime.timedelta(hours=9) # alert_timeはUNIX時間なので9時間足して日本時間にする
    year = alert_time.year #アラート発生時刻の年
    use_end = "" # 日付型で，VMの使用を終了した時間
    used_time = "" # 障害発生時刻の直前に使われていた時間
    used_VM_datas = {} # 出力するVMごとのデータ
    vm_hostname = "" # VMのホスト名
    
    ## VMのホスト名の後ろにLASTとついているファイル名を取得
    for file in os.listdir(data_location):
        if file[-4:] == "LAST":
            files.append(file)
        
    ## filesの中のファイルを一つずつ読み込んで，障害発生時刻の直前の使用時間を取得する
    for file in files:
        vm_hostname = file[:-5] # このVMのホスト名を取得
        with open(f"{data_location}/{file}", encoding="ASCII", mode="r") as f:
            for line in f:
                used_VM_datas[vm_hostname] = 0 # そのVMの使用時間を0に設定する
                over_day = 0 # 使用開始時刻から24時間以上使用していた場合に用いる変数
                line_components = line.split(" ")
                line_components = list(filter(None, line_components))
                
                ## 改行があったらファイルの終わりなので手前のfor文を抜ける
                if line_components[0] == "\n":
                    break
                
                ## 「pts/.*」(.*は正規表現)という文字列がない行を除外
                if re.search("pts/.*", line_components[1]) == None:
                    continue
                
                ## 「logged」という文字列があった行を除外
                if line_components[8] == "logged":
                    continue
                                
                ## 使用終了時刻を計算する
                use_start = datetime.datetime.strptime(str(year) + "-" + line_components[4] + "-" + line_components[5] + " " + line_components[6], "%Y-%b-%d %H:%M") # 使用開始時刻
                use_time = re.sub("[()\n]", "", line_components[9]) # 使用時間の値を適切なフォーマットにする               
                ## 使用時間が24時間を超えていた時，超えていた日数を取得しておき，何時間：何分の形に変換する
                if "+" in use_time: # 使用時間が24時間を超えていたら(24時間を超えると1+（1日）のようになっている)
                    idx = use_time.find("+") # +があるindexを取得
                    over_day = int(use_time[:idx]) # +までの文字列を取得し，int型に変換
                    use_time = use_time.split("+")[1] # "+"で分割してリストにしたあと，分割した右側の要素をuse_timeとする         
                use_time = use_time.split(":") # use_timeは文字列なので，":"で分割してリストにする   
                use_end = use_start + datetime.timedelta(days=over_day) # use_start(日付型)に，timedeltaメソッドでover_dayを足す
                use_end = use_end + datetime.timedelta(hours=int(use_time[0])) # use_start(日付型)に，timedeltaメソッドでuse_time[0](使用時間)を足す
                use_end = use_end + datetime.timedelta(minutes=int(use_time[1])) # use_start(日付型)に，timedeltaメソッドでuse_time[1](使用分)を足す
                                                
                ## 障害発生時刻の直前かどうか判定
                before_alert_time_start = alert_time - datetime.timedelta(minutes=get_start_time) # 直前と定義された時間範囲の開始時刻
                before_alert_time_end = alert_time - datetime.timedelta(minutes=get_end_time) # 直前と定義された時間範囲の終了時刻
                
                # 直前と定義された時間範囲内でVMの使用があったら(以下の4パターンになっていたら)
                # 時間の流れ：   使用開始時刻 --- 直前の開始 --- 使用終了時刻 --- 直前の終了
                # 時間の流れ：   直前の開始 --- 使用開始時刻 --- 使用終了時刻 --- 直前の終了
                # 時間の流れ：   使用開始時刻 --- 直前の開始 --- 直前の終了 --- 使用終了時刻
                # 時間の流れ：   直前の開始 --- 使用開始時刻 --- 直前の終了 --- 使用終了時刻
                if ( (use_start < before_alert_time_start) & ((before_alert_time_start < use_end) & (use_end < before_alert_time_end)) ): # 時間の流れ：   使用開始時刻 --- 直前の開始 --- 使用終了時刻 --- 直前の終了
                    used_time = use_end - before_alert_time_start
                    used_time = int(used_time.seconds / 60) # 差分を秒数で出し，それを60で割ることで分単位に直す
                    used_VM_datas[vm_hostname] = used_time # そのVMの使用時間をused_timeに設定する
                    print(f"パターン1, 使用時間：{used_time}, 使用開始時刻：{use_start}, 使用終了時刻：{use_end}") # デバック用
                    break # 障害発生時刻の直前の使用時間を取得できたのでfor分を抜ける
                elif ( ((before_alert_time_start < use_start) & (use_start < before_alert_time_end)) & ((before_alert_time_start < use_end) & (use_end < before_alert_time_end)) ): # 時間の流れ：   直前の開始 --- 使用開始時刻 --- 使用終了時刻 --- 直前の終了
                    used_time = use_end - use_start
                    used_time = int(used_time.seconds / 60) # 差分を秒数で出し，それを60で割ることで分単位に直す
                    used_VM_datas[vm_hostname] = used_time # そのVMの使用時間をused_timeに設定する
                    print(f"パターン2, 使用時間：{used_time}, 使用開始時刻：{use_start}, 使用終了時刻：{use_end}") # デバック用
                    break # 障害発生時刻の直前の使用時間を取得できたのでfor分を抜ける
                elif ( (use_start < before_alert_time_start) & (before_alert_time_end < use_end) ): # 時間の流れ：   使用開始時刻 --- 直前の開始 --- 直前の終了 --- 使用終了時刻
                    used_time = before_alert_time_end - before_alert_time_start
                    used_time = int(used_time.seconds / 60) # 差分を秒数で出し，それを60で割ることで分単位に直す
                    used_VM_datas[vm_hostname] = used_time # そのVMの使用時間をused_timeに設定する
                    print(f"パターン3, 使用時間：{used_time}, 使用開始時刻：{use_start}, 使用終了時刻：{use_end}") # デバック用
                    break # 障害発生時刻の直前の使用時間を取得できたのでfor分を抜ける
                elif ( ((before_alert_time_start < use_start) & (use_start < before_alert_time_end)) & (before_alert_time_end < use_end) ): # 時間の流れ：   直前の開始 --- 使用開始時刻 --- 直前の終了 --- 使用終了時刻
                    used_time = before_alert_time_end - use_start
                    used_time = int(used_time.seconds / 60) # 差分を秒数で出し，それを60で割ることで分単位に直す
                    used_VM_datas[vm_hostname] = used_time # そのVMの使用時間をused_timeに設定する
                    print(f"パターン4, 使用時間：{used_time}, 使用開始時刻：{use_start}, 使用終了時刻：{use_end}") # デバック用
                    break # 障害発生時刻の直前の使用時間を取得できたのでfor分を抜ける
                #print(f"パターン5, 使用時間：{used_time}, 使用開始時刻：{use_start}, 使用終了時刻：{use_end}") # デバック用  
                    
    print(f"アラート発生時刻：{alert_time}")
    print(used_VM_datas)
                
                
    return (hostname, used_VM_datas, before_time) # この物理サーバのホスト名とVMの直前使用状況をタプルで返す
    
## デバッグ用
if __name__ == "__main__":
    get_PS_access("192.168.100.21", "2024-11-25 13:57:00")