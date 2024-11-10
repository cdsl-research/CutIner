import subprocess
import json
import csv

def get_user_num():
    script_path = "/home/c0a21030/develop2/get_user_num.sh"
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    result = json.loads(result.stdout)["data"]["result"]
    # print(result[0])
    with open("ESXi_users.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["hostname", "userID"])
        for i,vm in enumerate(result):
            if not (result[i]["value"][1]):
                continue
            host_name = result[i]["metric"]["host_name"]
            userID = result[i]["metric"]["vm_name"].split('-')[0] 
            writer.writerow([host_name, userID])
            
    
if __name__ == "__main__":
    get_user_num()