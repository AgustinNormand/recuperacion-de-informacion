import sys
from links_collector import *

try:
    url = sys.argv[1]
except:
    print("Ingrese una URL por parámetro")

lc = Links_Collector()
links = lc.collect_links(url)
for link in links:
    print(link)