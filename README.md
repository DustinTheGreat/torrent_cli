# Torrent_Cli
A torrent search and downloader from the command line. Can been used to automatically download torrents.
I plan on serving this on AWS and use SMS to interface with it.
# Example:
  ## list torrent:
  <code> ./torrent.py shrek2 </code>
  ## download specific torrent:
   <code>./torrent.py shrek2 -d 0 </code>.
# usage:
<code> 
 torrent.py [-h] [-n NUM] [-s SORT_BY] [-o OUTPUT] [-p] [-v]
         [KEYWORD [KEYWORD ...]]
</code>

# positional arguments:
  KEYWORD               magnet keyword.

optional arguments:
       
     
    -h, --help            show this help message and exit
      
    -n NUM, --num NUM     magnet number.(default 10)
       
    -s SORT_BY, --sort-by SORT_BY
                      
    -o, OUTPUT, --output OUTPUT
                            
    -p, --pretty-oneline  show magnets info with one line.
    -v, --version         version information
  
# Help
  Want to implement threading into the torrent download.
