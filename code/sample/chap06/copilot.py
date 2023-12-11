# 读取csv文件，并返回一个数组对象
def read_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        return list(reader)


# 将数组对象转换为json字符串
def to_json(data):
    return json.dumps(data)


# 将json发送到github
def send_json(json_data):
    url = "https://api.github.com/repos/udacity/ud120-projects/issues"
    headers = {"Authorization": "mytoken"}  # 请填写你的token
    r = requests.post(url, json_data, headers=headers)


def main():
    data = read_csv("foo.csv")
    json_data = to_json(data)
    send_json(json_data)


# get price for crytocurrency
def get_price(coin):
    url = "https://api.coinmarketcap.com/v1/ticker/{}/".format(coin)
    r = requests.get(url)
    return r.json()[0]["price_usd"]
