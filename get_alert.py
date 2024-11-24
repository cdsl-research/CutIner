import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import calc_before_usage
import set_priority
import push_alert
import get_PS_access

class SimpleAlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 200 OKを返す
        self.send_response(200)
        self.end_headers()
        
        # リクエストボディのJSONデータを読み取る
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        alert_data = json.loads(post_data)

        # 日時を含めてデータをコンソールに出力
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} Received data:")
        print(json.dumps(alert_data, indent=4))
        groups = [] # アラートグループが何のアラートで構成されているかを取得するときのリスト．要素は[アラート名，障害箇所]
        severity = ( alert_data["groupKey"].split('\"') )[1] # そのアラートグループが何のseverityであるかを取り出す
        print("=================================")
        # severityがcriticalのアラートグループであれば
        if (severity == "critical"):
            print()
            for alert in alert_data["alerts"]:
                print(f"alert:{alert['labels']['alertname']}")
                print(f"instance:{alert['labels']['instance']}")
                print(f"severity:{alert['labels']['severity']}")
                groups.append( [alert['labels']['alertname'], alert['labels']['instance']] ) # groupsリストに追加
                
            used_VM_datas_every_PM = {} # key：物理サーバのホスト名(str)，Value：その物理サーバ内のVMごとの直前使用状況(dict)
            before_time = 0 # 直前の時間範囲
            
            # 1. 障害発生時刻の直前の内容を取得する．
            for alert in groups: # groupから一つずつアラートを取り出す
                hostname, used_VM_datas, before_time = get_PS_access.get_PS_access(alert[1], current_time) # get_PS_accessは戻り値の型が2要素のタプルであるため，それぞれ別々の変数で受け取る
                used_VM_datas_every_PM[hostname] = used_VM_datas
                
            # 直前使用度の算出
            before_useges = calc_before_usage.calc_before_usage(used_VM_datas_every_PM, before_time)
                
            # 優先度の決定
            priority_datas = set_priority.set_priority(before_useges)
            
            #優先度を付与したアラートをSlackへ送信
            push_alert.push_alert(current_time, alert_data, priority_datas)
            
            
        # severityがcriticalのアラートグループでなければ
        else:
            print("これはcriticalのアラートグループではない")
        print("=================================")
        
        groups = [] # リスト内容のリセット

if __name__ == "__main__":
    # サーバーのポートとハンドラを設定して起動
    server_address = ('', 9083)
    httpd = HTTPServer(server_address, SimpleAlertHandler)
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Starting server on port 9083")
    httpd.serve_forever()
    

    