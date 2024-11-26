# CutIner
このソフトウェアは，私の所属する研究室の物理サーバにおいて，severityがcriticalのアラートが発生した時，そのアラートを取得して，アラート発生時刻の直前のVM使用時間をもとに優先度を設定します．そして，設定した優先度順にアラートを並び替え，アラートを送信します．

## get_alert.py
### 説明
このプログラムは，実行すると無限ループでAlertmanagerからのアラートを受け付け，取得します．
取得した後，severityがcriticalのアラートのみ，alertname，instance，severityの項目を抜き出して表示させることも行います．

### 使用方法

```
python3 get_alert.py
```

このコマンドでプログラムを実行できます．

アラートを取得するためには，Alertmanager側で以下のようにwebhook-trouble-handlerをreceiverに指定する必要があります．

```Alertmanager_config.yaml
global:
  resolve_timeout: 1m

inhibit_rules:
  - equal:
      - namespace
      - alertname
    source_matchers:
      - severity = critical
    target_matchers:
      - severity =~ warning|info|attention  # 新しい優先度 'attention' を追加
  - equal:
      - namespace
      - alertname
    source_matchers:
      - severity = warning
    target_matchers:
      - severity =~ info|attention
  - equal:
      - namespace
    source_matchers:
      - alertname = InfoInhibitor
    target_matchers:
      - severity = info
  - target_matchers:
      - alertname = InfoInhibitor

### レシーバーにwebhook-trouble-handlerを定義
receivers:
  - name: 'webhook-trouble-handler'
    webhook_configs:
      - url: 'http://<アラートを受け取るノードのホスト名またはIPアドレス>:9083'
        send_resolved: true
  
route:
  group_by:
    - severity
  group_interval: 10m
  group_wait: 1m
  repeat_interval: 5m
  receiver: webhook-trouble-handler # レシーバーにwebhook-trouble-handlerを指定

templates:
  - /etc/alertmanager/config/*.tmpl
```

### 実行結果
```アラート取得待機中
c0a21030@c0a21030-implement:~/develop2$ python3 get_alert.py 
2024-11-24 14:10:41 Starting server on port 9083
```

このように，receiverとしてwebhook-trouble-handlerを指定してください．
また，このプログラムを実行中のIPアドレスまたはhostnameを指定してください．
### バージョン
このプログラムはPython3.10.12のバージョンで作成しました．うまく動作しない場合はこのバージョンに合わせてみてください

## get_PS_access.py
このプログラムは，物理サーバごとに，物理サーバ内のVMが，アラート発生時刻の直前にどのくらいの時間使用されていたのかを取得します．

### 使用方法
get_alert.pyによって呼び出されます．
get_PS_acccess.py単体で実行したい場合は,以下のように実行出来ます
```
python3 get_PS_access.py
```

### 実行結果
```テスト実行の結果
c0a21030@c0a21030-implement:~/develop2$ python3 get_PS_access.py 
パターン1, 使用時間：10, 使用開始時刻：2024-11-25 21:18:00, 使用終了時刻：2024-11-25 22:49:00
パターン4, 使用時間：2, 使用開始時刻：2024-11-25 22:52:00, 使用終了時刻：2024-11-25 22:55:00
アラート発生時刻：2024-11-25 22:57:00
{'c0a21030-outside-site-test-worker2': 0, 'c0a21030-outside-site-test-worker1': 0, 'c0a21030-monitoring-mp': 10, 'c0a21030-outside-site-test-master': 0, 'c0a21030-outside-site-test-nfs': 2}
```

## calc_before_usage.py
このプログラムは，引数として受け取った物理サーバごとのVM使用時間のデータから，物理サーバごとの直前使用度を算出します．

### 使用方法
get_alert.pyによって呼び出されます．
calc_before_usage.py単体で実行したい場合は,以下のように実行出来ます
```
python3 calc_before_usage.py
```

### 実行結果
```テスト実行の結果
c0a21030@c0a21030-implement:~/develop2$ python3 calc_before_usage.py 
{'plum': Decimal('0.13'), 'rose': Decimal('0.08')}
```

## set_priority.py
このプログラムは，引数として受け取った物理サーバごとの直前使用度をもとに，優先度を割り当てます．

### 使用方法
get_alert.pyによって呼び出されます．
set_priority.py単体で実行したい場合は,以下のように実行出来ます
```
python3 set_priority.py
```

### 実行結果
```テスト実行の結果
c0a21030@c0a21030-implement:~/develop2$ python3 set_priority.py 
{'plum': 1, 'rose': 2, 'lotus': 3}
```

## push_alert.py
このプログラムは，引数として受け取った，Alertmanagerから取得したアラートの情報，物理サーバごとの優先度を使用して，優先度ごとに並び変えられたアラートを送信します．

### 使用方法
get_alert.pyによって呼び出されます．
push_alert.py単体で実行したい場合は,以下のように実行出来ます
```
python3 push_alert.py
```

### 実行結果
テスト実行の結果
![alt text](image.png)