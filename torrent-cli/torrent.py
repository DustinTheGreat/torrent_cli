#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import os
import re
import csv
import math
import argparse
import json
import codecs

import requests
from bs4 import BeautifulSoup, Comment


HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

VERSION = "VERSION 0.0.9"
DOMAIN = "https://www.thepiratebay.org"
ARCHIVE = "https://tpb.party"

PROXIES = {
    "http": 'http://59.127.55.215:36733', 
    "https": 'http://59.127.55.215:36733'
}
def get_parser():
  
    parser = argparse.ArgumentParser(description='Magnets-Getter CLI Tools.')
    parser.add_argument('keyword', metavar="KEYWORD", type=str, nargs="*",
                        help='magnet keyword.')
    parser.add_argument('-n', '--num', type=int, default=0,
                        help='magnet number.(default 10)')
    parser.add_argument('-s', '--sort-by', type=int, default=0,
                        help='0: Sort by date，1: Sort by size. 2: Sort by hot-rank.(default 0)')
    parser.add_argument('-o', '--output', type=str,
                        help='output file path, supports csv and json format.')
    parser.add_argument('-p', '--pretty-oneline', action='store_true',
                        help='show magnets info with one line.' , default= 0)
    parser.add_argument('-v', '--version', action='store_true',
                        help='version information.')
    return parser


def command_line_runner():
   
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)
        return

    if not args["keyword"]:
        parser.print_help()
    else:
        magnets = run(kw=args["keyword"],
                      num=args["num"], sort_by=args["sort_by"])

def run(kw, num, sort_by):

    print("Crawling data for you.....")
    _kw = "%20".join(kw)
    # 排序类型选择
    if sort_by == 0:
        sort_str = "ctime"
    elif sort_by == 1:
        sort_str = "length"
    elif sort_by == 2:
        sort_str = "click"
    else:
        raise ValueError("Unknown Sort Method")

    
    

    #if user didnt declare pages get first page only
    if num > 0:
        for p in range(0, num + 1):
            url = DOMAIN + "/search/{kw}/{p}".format(kw=_kw, p=p)
    else:
        url = DOMAIN + "/search/{kw}/{p}".format(kw=_kw, p=num)

        try:
            resp = requests.get(url, headers=HEADERS, proxies = PROXIES).text.encode("utf-8")
            try:
                print(url)
                parse_results(resp)      
            except:
                print("Error when parsing")
                #search archive 
                url2 = ARCHIVE + "/search/{kw}/{p}".format(kw=_kw, p=num)
                print(url2)
                resp2 = requests.get(url2, headers=HEADERS).text.encode("utf-8")
                try:
                    print(resp2)
                    parse_results(resp2) 

                except:
                    print("error parsing results")

        except Exception as e:
            print(e)
def parse_results(response):
    links = []
    torrents = []
    torrent_list = [] 
    soup2 = BeautifulSoup(response, "lxml")
    for link in soup2.findAll('a', attrs={'href': re.compile("^magnet")}):
        links.append((link.get('href')))
    
    table = soup2.find("table", id="searchResult")

    if not table:
        print('no table')
        print(url)
        #table = soup.find_all('table')
        #print('count:', len(table))
        #print(response.text)
    else:
        for row in table.find_all('tr'):
            
            for column in row.find_all('td'):
                text = ', '.join(x.strip() for x in column.text.split('\n') if x.strip()).strip()
                torrents.append(text.encode("ascii", "replace"))
        holder = int(0)
        for x in range(len(links)):
            torrent_list.append(torrents[holder:holder+4:1])
            holder +=4
        for index in range(len(links)):
            print(torrent_list[index])
            print(links[index])


def parse_name(name):







    return(name)



def download_torrnet(torrnet):
    pass
















'''    return sort_magnets(magnets, sort_by, num)

def sort_magnets(magnets, sort_by, num):
    
    if sort_by == 0:
        _magnets = sorted(magnets,
                          key=lambda x: x["magnet_date"],
                          reverse=True)
    # 按大小排序，统一单位为 kb
    elif sort_by == 1:
        for m in magnets:
            unit = m["magnet_size"].split()
            if unit[1] == "GB":
                _size = float(unit[0]) * 1024 * 1024
            elif unit[1] == "MB":
                _size = float(unit[0]) * 1024
            else:
                _size = float(unit[0])
            m["magnet_size_kb"] = _size
        _magnets = sorted(magnets,
                          key=lambda x: x["magnet_size_kb"],
                          reverse=True)
    else:
        _magnets = sorted(magnets,
                          key=lambda x: x["magnet_rank"],
                          reverse=True)
    return _magnets[:num]


def _print(magnets, is_show_magnet_only):
    """

    :param magnets: 磁力列表
    :param is_show_magnet_only: 单行输出
    """
    if not magnets:
        return
    if is_show_magnet_only:
        for row in magnets:
            print(row["magnet"], row["magnet_size"], row["magnet_date"])
    else:
        for row in magnets:
            try:
                print("磁链:", row["magnet"])
                print("名称:", row["magnet_name"])
                print("大小:", row["magnet_size"])
                print("日期:", row["magnet_date"])
                print("热度:", row["magnet_rank"], "\n")
            except:
                print("磁链:", row["magnet"])
                print("名称:", row["magnet_name"].encode('utf-8'))
                print("大小:", row["magnet_size"])
                print("日期:", row["magnet_date"])
                print("热度:", row["magnet_rank"], "\n")


def _output(magnets, path):
    """

    :param magnets: 磁力列表
    :param path: 文件路径，支持 csv 和 json 两种文件格式
    """
    if path:
        _, extension = os.path.splitext(path)
        if extension == ".csv":
            with open(path, mode="w+", encoding="utf-8-sig", newline="") as fout:
                fieldnames = (
                    "magnet",
                    "magnet_name",
                    "magnet_size",
                    "magnet_date",
                    "magnet_rank"
                )
                f_csv = csv.DictWriter(fout, fieldnames, extrasaction="ignore")
                f_csv.writeheader()
                f_csv.writerows(magnets)
            print("Save successfully!")
        elif extension == ".json":
            with codecs.open(path, mode="w+", encoding="utf-8") as f:
                json.dump(magnets, f, indent=2)
            print("Save successfully!")
        else:
            print("Failed to save the file!")

'''
if __name__ == "__main__":
    command_line_runner()
