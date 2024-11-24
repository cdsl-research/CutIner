import requests
import json

def push_alert(alert_time, alert_datas, priority_datas):
    """優先度順に並び変えられたアラートを送信する

    Args:
        alert_time (str): アラート発生時刻
        alert_datas (dict): アラートのデータ．構造が複雑で書くのめんどいから詳しくは書かないよ
        priority_datas (dict): 物理サーバごとの優先度
            key:
                - hostname (str): 物理サーバのホスト名
            value:
                - priority (int): 優先度
    """

    webhook_url = "https://hooks.slack.com/services/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"
    
    ## ホスト名とIPアドレスの対応を保持した辞書
    hostnames = {"192.168.100.21":"plum",
                 "192.168.100.22":"jasmine",
                 "192.168.100.23":"rose",
                 "192.168.100.24":"lotus",
                 "192.168.100.25":"violet",
                 "192.168.100.26":"mint",
                 "192.168.100.27":"lily",
                 }
    
    pushing_alerts = "" # 送信するアラート達
    pushing_alerts += f"========================{alert_time}========================\n"
    for hostname, priority in priority_datas.items():
        for alert in alert_datas["alerts"]: # alert_datas["alerts"]：リスト，alert：辞書
            alert_name = "" # アラート名
            instance = "" # アラート発生箇所のホスト名
            severity = "" # アラートの重大度
            description = "" # アラートの詳細
            runbook_url = "" # runbookのURL          
            
            if hostnames[alert["labels"]["instance"]] == hostname: # アラートinstance(IPaddress)がpriorityのhostnameと同じ時
                alertname = alert["labels"]["alertname"]
                instance = hostname
                severity = alert["labels"]["severity"]
                description = alert["annotations"]["description"]
                runbook_url = alert["annotations"]["runbook_url"]
                
                pushing_alerts += "##########################################\n"
                pushing_alerts += f"alert_name:`{alertname}`\n"
                pushing_alerts += f"description:`{description}`\n"
                pushing_alerts += f"instance:`{instance}`\n"
                pushing_alerts += f"severity:`{severity}`\n"
                pushing_alerts += f"runbook_url:`{runbook_url}`\n"
                pushing_alerts += "\n"
                pushing_alerts += f"優先度:`{priority}`\n"
                pushing_alerts += "##########################################\n"
                pushing_alerts += "\n"
                
    pushing_alerts += "=================================================\n"

    requests.post(webhook_url, data = json.dumps({
        "text" : pushing_alerts,
    }))

if __name__ == "__main__":
    push_alert()