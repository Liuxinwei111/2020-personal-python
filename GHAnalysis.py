import json
import os
import argparse

class Data:

    def __init__(self, path:str=None):  #对其进行初始化
        self.__dir_addr = path


        if path:
            print("init")
            if not os.path.exists(self.__dir_addr):
                raise RuntimeError("Path doesn't exist.")  #判断路径是否存在
            self.__read_1()
            self.__analysis()
            self.__save2json()
        else:
            self.__read_2()



    def __read_1(self):   #读取文件，将结果保存到json文件，并对json文件进行核对
        self.__dicts = []
        for root, dirs, files in os.walk(self.__dir_addr):
            for file in files:
                if file[-5:] == '.json' and file[-6:] != '1.json' and file[-6:] != '2.json' and file[-6:] != '3.json':
                    with open(file, 'r', encoding='utf-8') as f:
                        self.__jsons = [x for x in f.read().split('\n') if len(x)>0]
                        for self.__json in self.__jsons:
                            self.__dicts.append(json.loads(self.__json))

    def __analysis(self):
        self.__types = ['PushEvent', 'IssueCommentEvent', 'IssuesEvent', 'PullRequestEvent']
        self.__cnt_perP = {}  #个人的 4 种事件的数量。
        self.__cnt_perR = {}  #每一个项目的 4 种事件的数量。
        self.__cnt_perPperR = {}  #每一个人在每一个项目的 4 种事件的数量。

        for self.__dict in self.__dicts:
            # 如果属于四种事件之一 则增加相应值
            if self.__dict['type'] in self.__types:
                self.__event = self.__dict['type']
                self.__name = self.__dict['actor']['login']
                self.__repo = self.__dict['repo']['name']
                self.__cnt_perP[self.__name + self.__event] = self.__cnt_perP.get(self.__name + self.__event, 0) + 1
                self.__cnt_perR[self.__repo + self.__event] = self.__cnt_perR.get(self.__repo + self.__event, 0) + 1
                self.__cnt_perPperR[self.__name + self.__repo + self.__event] = \
                self.__cnt_perPperR.get(self.__name + self.__repo + self.__event, 0) + 1

    def __save2json(self):  #计算出来的字典保存到json文件
        with open("1.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perP, f)
        with open("2.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perR, f)
        with open("3.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perPperR, f)
        print("Save to json files successfully!")

    def __read_2(self):  #对三个json文件进行答案读取
        self.__cnt_perP = {}
        self.__cnt_perR = {}
        self.__cnt_perPperR = {}
        with open("1.json", encoding='utf-8') as f:
            self.__cnt_perP = json.load(f)
        with open("2.json", encoding='utf-8') as f:
            self.__cnt_perR = json.load(f)
        with open("3.json", encoding='utf-8') as f:
            self.__cnt_perPperR = json.load(f)

    # get value from dictionary

    def get_cnt_user(self, user:str, event:str) -> int:  #转换成int类型
        return self.__cnt_perP.get(user + event, 0)

    def get_cnt_repo(self, repo:str, event:str) -> int:  #同上
        return self.__cnt_perR.get(repo + event, 0)

    def get_cnt_user_and_repo(self, user, repo, event) -> int:  #同上
        return self.__cnt_perPperR.get(user + repo + event, 0)

def run():  #命令行参数的设置
    my_parser = argparse.ArgumentParser(description='analysis the json file')
    my_parser.add_argument('-i', '--init', help='json file path')   #添加参数
    my_parser.add_argument('-u', '--user', help='username')         #同上
    my_parser.add_argument('-r', '--repo', help='repository name')  #同上
    my_parser.add_argument('-e', '--event', help='type of event')   #同上
    args = my_parser.parse_args()   #解析命令行给出的参数

    if args.init:
        my_data = Data(path=args.init)
    else:
        my_data = Data()
        if args.event:
            if args.user:
                if args.repo:
                    print(my_data.get_cnt_user_and_repo(args.user, args.repo, args.event))
                else:
                    print(my_data.get_cnt_user(args.user, args.event))
            else:
                if args.repo:
                    print(my_data.get_cnt_repo(args.repo, args.event))
                else:
                    print("lock of parm")
        else:
            print("lack: event")

if __name__ == '__main__':
    run()