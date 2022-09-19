import subprocess
import requests
import json
import datetime


def calc_CPU(server):
    # CPU使用率
    result = subprocess.check_output(["ssh", server, "sar", "-u"], text=True)
    result = result.split()

    return "__**CPU**__\nCPU: " + result[5].replace("(", "") + "\tuser: " + result[-6] + "%\tsystem: " + result[-4] + "%\tidle: " + result[-1] + "%"


def calc_Mem(server):
    # メモリ使用率
    result = subprocess.check_output(["ssh", server, "sar", "-rh"], text=True)
    result = result.split()

    return "__**Memory**__\nfree: " + result[-11] + "\tavail: " + result[-10] + "\tused: " + result[-9] + "\t%memused: " + result[-8]


def calc_uptime(server):
    # メモリ使用率
    result = subprocess.check_output(["ssh", server, "uptime"], text=True)
    result = result.split()

    return "__**UpTime**__\n" + result[2] + result[3].replace(",", "\t") + result[4].replace(",", "")


def calc_loadaverage(server):
    # メモリ使用率
    result = subprocess.check_output(["ssh", server, "uptime"], text=True)
    result = result.split()

    return "__**Load Average**__\n1m: " + result[9].replace(",", "") + "\t5m: " + result[10].replace(",", "") + "\t15m: " + result[11]


def calc_Temp(server):
    # 温度
    if server == "server1" or server == "server4":
        result1 = int(subprocess.check_output(["ssh", server, "cat", "/sys/class/thermal/thermal_zone0/temp"], text=True))
        result1 = result1 / 1000

        return "__**Temp**__\nSocket0: " + str(result1) + "℃"
    else:
        result1 = int(subprocess.check_output(["ssh", server, "cat", "/sys/class/thermal/thermal_zone0/temp"], text=True))
        result1 = result1 / 1000
        result2 = int(subprocess.check_output(["ssh", server, "cat", "/sys/class/thermal/thermal_zone1/temp"], text=True))
        result2 = result2 / 1000

        return "__**Temp**__\nSocket0: " + str(result1) + "℃\tSocket1: " + str(result2) + "℃"


if __name__ == "__main__":
    # 日付取得
    dt_now = datetime.datetime.now()
    date = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    # 送信用
    webhook_url = "https://discord.com/api/webhooks/1021321753554862081/r8WuKyNf6hXW8NkFhIxjZC0H1KMQlj8oEldmOoZEKX5xDmkczX-tR2PptAHgxMoRqsvM"
    headers = {"Content-Type": "application/json"}

    # 日付
    text = date

    # サーバの種類
    server = ["server1", "server2", "server3", "server4"]

    for name in server:
        # 送信用メッセージ
        text = text + "\n---------- " + name + " ----------\n" + calc_uptime(name) + "\n" + calc_CPU(name) + "\n" + calc_Mem(name) + "\n" + calc_Temp(name)

    # 送信
    main_content = {"content": text}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, json.dumps(main_content), headers=headers)
