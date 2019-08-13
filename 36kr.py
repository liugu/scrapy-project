# -*- coding: utf-8 -*-

import re
import json
import requests
import os
from pprint import pprint


class NewsFlashesSplider:
    def __init__(self):
        # "https://36kr.com/newsflashes?b_id={}&per_page=20"
        self.url = "https://36kr.com/newsflashes"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.file_dir = "./newsflashes.txt"

    def parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        ret = json.loads(response.content.decode())["data"]["items"]
        size = len(ret)
        last_id = int(ret[size - 1]["id"])
        with open(self.file_dir, "a", encoding="utf-8") as file:
            file.write(json.dumps(ret, ensure_ascii=False))
            file.write("\r\n")
        return size, last_id

    def run(self):
        if os.path.exists(self.file_dir):
            os.remove(self.file_dir)
            print("文件已清空")

        # 第一次请求获得当前最新的新闻
        response = requests.get(self.url, headers=self.headers)
        
        test = response.content.decode()
        # print('response:')
        # print(test)

        result = re.compile("<script>window.initialState=(.*)</script>").findall(
            response.content.decode())
        # print(result[0])

        # 打开文件进行 'w'riting 写操作
        # f = open('test.txt', 'w', encoding="utf-8")
        # # 将文本写入到文件
        # f.write(result[0])
        # # 关闭文件
        # f.close()
        
        ret = json.loads(result[0])
        
        lists = ret['newsflashCatalogData']['data']['newsflashList']['data']

        # 新闻个数,最后一个id
        tuple_result = len(lists), int(lists[len(lists) - 1]["id"])

        while True:
            self.url = "https://36kr.com/api/newsflash?b_id={}&per_page=20".format(tuple_result[1])
            tuple_result = self.parse_url()
            if tuple_result[0] < 20:
                break

def main():
    splider = NewsFlashesSplider()
    splider.run()


if __name__ == '__main__':
    main()
