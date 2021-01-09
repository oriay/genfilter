import os
import shutil

from rich.progress import Progress

from .extractor import DataExtrator


def creat_dirs(target):
    if target == "all":
        if os.path.exists("public"):
            shutil.rmtree("public")
        os.mkdir("public")
        os.chdir("public")
        for dir in ["clash", "quantumult-x"]:
            os.mkdir(dir)
    else:
        if os.path.exists("public"):
            shutil.rmtree("public")
        os.mkdir("public")
        os.chdir("public")
        if os.path.exists(target):
            shutil.rmtree(target)
        os.mkdir(target)
    os.chdir("../")


def convert_qx(domain_list, file_name):
    print(file_name)
    domain_list = [x for x in domain_list if x[0:7] != "regexp:"]
    filter_list = []
    for item in domain_list:
        if item[0:5] == "full:":
            filter_list.append("host, " + item[5:] + ", " + file_name)
        elif item[0:] == "keyword:":
            filter_list.append("host-keyword, " + item[8:] + ", " + file_name)
        else:
            filter_list.append("host-suffix, " + item + ", " + file_name)
    with open(file_name, "w", encoding="utf-8") as e:
        for item in filter_list:
            print(item)
            e.write(item+"\n")


def convert_clash(domain_list, file_name):
    print(file_name)
    domain_list = [x for x in domain_list if x[0:7] != "regexp:"]
    filter_list = []
    for item in domain_list:
        if item[0:5] == "full:":
            filter_list.append("DOMAIN," + item[5:])
        elif item[0:] == "keyword:":
            filter_list.append("DOMAIN-KEYWORD," + item[8:])
        else:
            filter_list.append("DOMAIN-SUFFIX," + item)
    with open(file_name, "w", encoding="utf-8") as e:
        for item in filter_list:
            print(item)
            e.write(item+"\n")


def convert(target):
    creat_dirs(target)
    data = DataExtrator("latest")
    file_list = data.get_file_list()
    with Progress() as progress:
        if target != "all":
            task = progress.add_task(
                "[red]Downloading...", total=len(file_list))
            os.chdir("public/"+target)
            for file_name in file_list:
                domain_list = data.data_parser(file_name)
                if target == "quantumult-x":
                    convert_qx(domain_list, file_name)
                elif target == "clash":
                    convert_clash(domain_list, file_name)
                progress.update(task, advance=1,
                                description=f'{target} ==> {file_name:50}')
            os.chdir('../../')
        elif target == "all":
            task_qx = progress.add_task(
                'quantumult-x ==> watting', total=len(file_list))
            task_clash = progress.add_task(
                'clash ==> watting', total=len(file_list))
            os.chdir("public")
            for _target in ["quantumult-x", "clash"]:
                os.chdir(_target)
                for file_name in file_list:
                    domain_list = data.data_parser(file_name)
                    if _target == "quantumult-x":
                        convert_qx(domain_list, file_name)
                        progress.update(
                            task_qx, advance=1, description=f'{_target} ==> {file_name:50}')
                    elif _target == "clash":
                        convert_clash(domain_list, file_name)
                        progress.update(
                            task_clash, advance=1, description=f'{_target} ==> {file_name:50}')
                os.chdir("../")
            os.chdir("../")
        print(data.release_tag)
