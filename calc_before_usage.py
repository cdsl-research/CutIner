import math
from decimal import Decimal, ROUND_HALF_UP

def rounding_off(num):
    """引数を四捨五入する

    Args:
        num (float): 四捨五入する対象の数値
    Returns:
        rounded_num (float): 小数第2位
    """
    decimal_num = Decimal(str(num))

    # ROUND_HALF_UPで四捨五入
    rounded_num = decimal_num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
    
    return rounded_num


def calc_before_usage(used_VM_datas_every_PM, before_time): 
    """物理サーバごとの直前使用度の算出を行う
    Args:
        used_VM_datas_every_PM (dict): 物理サーバごとのVMの直前使用状況のデータ
            key:
                - hostname (str): 物理サーバのホスト名
            value:
                - used_VM_datas (dict): VMごとの直前使用状況のデータ
                    key:
                        - vm_hostname (str): VMのホスト名
                    value:
                        - used_time (int): 直前と定義された時間範囲内で使用されたいた時間
        before_time (int): 直前の時間範囲
    Returns:
        before_usage_every_PM (dict): 物理サーバごとの直前使用度
            key:
                - hostname (str): 物理サーバのホスト名
            value:
                - before_usage (float): 直前使用度
    """
    
    before_usage_every_PM = {} # 戻り値として使う変数
        
    ## 直前使用度の算出
    for hostname, used_VM_datas in used_VM_datas_every_PM.items(): # 物理サーバのホスト名とそのホスト名の持つVMごとの直前使用状況のデータをそれぞれ取得
        used_time_list = [] # 平均を出すために使うリスト
        for used_time in used_VM_datas.values(): # VMごとにused_timeを取り出す
            vm_before_usage = used_time / before_time # そのVMの直前使用度を計算    
            used_time_list.append(vm_before_usage) # リストに追加
        before_usage = rounding_off(sum(used_time_list) / len(used_time_list)) # 物理サーバの直前使用度の算出
        before_usage_every_PM[hostname] = before_usage # 出力結果に追加
        
    print(before_usage_every_PM)
    return before_usage_every_PM

            
if __name__ == "__main__":
    input = {"plum" : {"vm1":2, "vm2":0, "vm3":5, "vm4":1}, "rose" : {"vm1":4, "vm2":1, "vm3":0, "vm4":0}}
    before_time = 15
    calc_before_usage(input, before_time)
