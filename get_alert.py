import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import set_severity

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
        groups = [] # アラートグループが何のアラートで構成されているかを取得するときのリスト
        severity = ( alert_data["groupKey"].split('\"') )[1] # そのアラートグループが何のseverityであるかを取り出す
        print("=================================")
        # severityがcriticalのアラートグループであれば
        if (severity == "critical"):
            print()
            for alert in alert_data["alerts"]:
                print(f"alert:{alert['labels']['alertname']}")
                print(f"instance:{alert['labels']['instance']}")
                print(f"severity:{alert['labels']['severity']}")
                groups.append( [alert['labels']['alertname'], alert['labels']['instance']] )
        # severityがcriticalのアラートグループでなければ
        else:
            print("これはcriticalのアラートグループではない")
        print("=================================")
        #set_severity.pyを実行
        set_severity.to_evaluate_alert(groups)
        
        groups = [] # リスト内容のリセット

if __name__ == "__main__":
    # サーバーのポートとハンドラを設定して起動
    server_address = ('', 9083)
    httpd = HTTPServer(server_address, SimpleAlertHandler)
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Starting server on port 9083")
    httpd.serve_forever()
    

    