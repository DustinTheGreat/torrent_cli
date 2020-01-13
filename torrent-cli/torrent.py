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
from subprocess import call
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
            
            resp = requests.get(url, headers=HEADERS).text.encode("utf-8")
            
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
                    parse_results(resp2) 

                except:
                    print("error parsing results")

        except Exception as e:
            print(e)
            url2 = ARCHIVE + "/search/{kw}/{p}".format(kw=_kw, p=num)
            resp2 = requests.get(url2, headers=HEADERS).text.encode("utf-8")
            try:
                parse_results(resp2)
                print('here')
                download  = input("What one do you want to download?") 
                print(download)
                print(links[int(download)])
                download_torrnet(links[int(download)])
            except:
                print("error parsing results")
def parse_results(response):
    global links
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
            print(index)
            parse_name(torrent_list[index])

            print(links[index])
        print(links[0])
    f = links[0]
    save_link(f)


def save_link(magnet):
    with open("links.txt", "w+") as file:
        file.write(magnet)

def parse_name(name):
    for items in range(len(name)):
        name[items] = name[items].decode("utf-8" ,"replace")

    info = name[1].split(',')
    print()
    print("Name: {}".format(info[0]))
    print("Uploaded: {}".format(info[1]))
    print("Size: {}".format(info[2]))
    print("Type:{}".format(name[0]))
    print("S/L Ratio:{}{}{}".format(name[2], "/", name[3]))

    print("\n")


def download_torrnet(torrnet):
    #start multiprocessing
   # call(["transmission-cli", "-p", "57558", torrnet])
    



def sort_by():
    pass


def main():
    pass

if __name__ == "__main__":
    command_line_runner()
