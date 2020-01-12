# Torrent_Cli
A torrent search and downloader from the command line. Can been used to automatically 
# Example:
  <code> torrent.py -shrek2 </code>
# usage:
 
 torrent.py [-h] [-n NUM] [-s SORT_BY] [-o OUTPUT] [-p] [-v]
         [KEYWORD [KEYWORD ...]]

Magnets-Getter CLI Tools.

positional arguments:
  KEYWORD               magnet keyword.

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     magnet number.(default 10)
  -s SORT_BY, --sort-by SORT_BY
                        0: Sort by date，1: Sort by size. 2: Sort by hot-
                        rank.(default 0)
  -o OUTPUT, --output OUTPUT
                        output file path, supports csv and json format.
  -p, --pretty-oneline  show magnets info with one line.
  -v, --version         version information
# Help
  Want to implement threading into the torrent download.
