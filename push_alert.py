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

    webhook_url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
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
    alert_datas = {
    "receiver": "webhook-trouble-handler",
    "status": "firing",
    "alerts": [
        {
            "status": "firing",
            "labels": {
                "alertname": "icmp-check",
                "instance": "192.168.100.23",
                "job": "my_blackbox_icmp",
                "prometheus": "monitoring/prometheus-kube-prometheus-prometheus",
                "severity": "critical"
            },
            "annotations": {
                "description": "Instance icmp not connection",
                "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedreload",
                "summary": "icmp error"
            },
            "startsAt": "2024-10-09T07:50:19.912Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=probe_success+%3D%3D+0&g0.tab=1",
            "fingerprint": "cd17d346be9700c3"
        },
        {
            "status": "firing",
            "labels": {
                "alertname": "icmp-check",
                "instance": "192.168.100.21",
                "job": "my_node-exporter",
                "prometheus": "monitoring/prometheus-kube-prometheus-prometheus",
                "severity": "critical"
            },
            "annotations": {
                "description": "Instance icmp not connection",
                "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedreload",
                "summary": "node up not connection"
            },
            "startsAt": "2024-10-09T07:42:07.171Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1",
            "fingerprint": "3d9203a36337f368"
        },
        {
            "status": "firing",
            "labels": {
                "alertname": "icmp-check",
                "instance": "192.168.100.24",
                "job": "my_node-exporter",
                "prometheus": "monitoring/prometheus-kube-prometheus-prometheus",
                "severity": "critical"
            },
            "annotations": {
                "description": "Instance icmp not connection",
                "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedreload",
                "summary": "node up not connection"
            },
            "startsAt": "2024-10-09T07:42:07.171Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1",
            "fingerprint": "3d9203a36337f368"
        }
    ],
    "groupLabels": {
        "severity": "critical"
    },
    "commonLabels": {
        "prometheus": "monitoring/prometheus-kube-prometheus-prometheus",
        "severity": "critical"
    },
    "commonAnnotations": {
        "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedreload"
    },
    "externalURL": "http://prometheus-kube-prometheus-alertmanager.monitoring:9093",
    "version": "4",
    "groupKey": "{}/{}:{severity=\"critical\"}",
    "truncatedAlerts": 0
}
    alert_time = "2024-10-25 16:30:00"
    priority_datas = {'plum': 1, 'rose': 2, 'lotus': 3}
    
    push_alert(alert_time, alert_datas, priority_datas)