import decimal

def set_priority(before_usages):
    """優先度の設定と優先度順への並び変え

    Args:
        before_usages (dict): 物理サーバごとの直前使用度
            key:
                - hostname (str): 物理サーバのホスト名
            value:
                - before_usage (decimal): 直前使用度

    Returns:
        priorities (dict): 物理サーバごとの優先度
            key:
                - hostname (str): 物理サーバのホスト名
            value:
                - priority (int): 優先度
    """
    
    priorities = {} # キー：物理サーバのホスト名，Value：優先度(1~)
    
    # 影響度の降順に並び替える
    sorted_impact_degrees = sorted(before_usages.items(), key=lambda x:x[1], reverse=True)
    # 優先度の決定
    for i,impact_degree in enumerate(sorted_impact_degrees):
        priorities[impact_degree[0]] = i + 1
        
    print(priorities)
    return priorities

if __name__ == "__main__":
    before_usages = {"rose":0.11, "plum":0.14, "lotus":0.04}
    set_priority(before_usages)