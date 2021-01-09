import json

import requests


class DataExtrator():
    def __init__(self, release_tag="latest"):
        if release_tag == "latest":
            self.release_tag = json.loads(requests.get(
                "https://api.github.com/repos/v2fly/domain-list-community/releases/latest").content.decode('utf-8'))["tag_name"]
        else:
            self.release_tag = release_tag

    def get_file_list(self):
        api_url = "https://api.github.com/repos/v2fly/domain-list-community/"
        latest_release_sha = json.loads(requests.get(
            api_url+"releases/tags/"+self.release_tag).content.decode("utf-8"))["target_commitish"]
        latest_tree = json.loads(requests.get(
            api_url+"git/trees/"+latest_release_sha).content.decode("utf-8"))
        data_tree_url = [x["url"]
                         for x in latest_tree["tree"] if x["path"] == "data"][0]
        domain_file_list = [domain_file["path"]
                            for domain_file in json.loads(requests.get(data_tree_url).content.decode("utf-8"))["tree"]]
        return domain_file_list

    def data_parser(self, file_name):
        resp = requests.get(
            "https://cdn.jsdelivr.net/gh/v2fly/domain-list-community@"+self.release_tag+"/data/"+file_name).content.decode('utf-8')
        domain_list = resp.split("\n")

        # 删除空白行
        domain_list = [x for x in domain_list if x != '']
        # 删除注释行
        domain_list = [x for x in domain_list if x[0] != '#']
        # 忽略空格后的内容
        domain_list = [x.split(" ")[0] for x in domain_list]
        # 递归读取 include 指向的文件
        for item in domain_list:
            if item[0:8] == "include:":
                domain_list = domain_list + self.data_parser(item[8:])
        # 删除 include 行
        domain_list = [x for x in domain_list if x[0:8] != "include:"]

        return domain_list
