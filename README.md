# CutIner

## get_alert.py
### 説明
このプログラムは，実行すると無限ループでAlertmanagerからのアラートを受け付け，取得します．
取得した後，severityがcriticalのアラートのみ，alertname，instance，severityの項目を抜き出して表示させることも行います．

### 使用方法

```
python3 get_alert.py
```

このコマンドでプログラムを実行できます．

アラートを取得するためには，Alertmanager側で以下のように設定を行う必要があります．

```
receivers:
- name: 'webhook-trouble-handler'
  webhook_configs:
    - url: 'http://<IPアドレスまたはhostname>:9083'
      send_resolved: true

route:
  group_by:
  - severity
  group_interval: 1m
  group_wait: 30s
  receiver: "webhook-trouble-handler"
  repeat_interval: 1m
  routes:
  - match:
      alertname: DeadMansSwitch
    receiver: webhook-trouble-handler
  - continue: true
    match: null
    receiver: webhook-trouble-handler
```

このように，receiverとしてwebhook-trouble-handlerを指定してください．
また，このプログラムを実行中のIPアドレスまたはhostnameを指定してください．
### バージョン
このプログラムはPython3.10.12のバージョンで作成しました．うまく動作しない場合はこのバージョンに合わせてみてください
