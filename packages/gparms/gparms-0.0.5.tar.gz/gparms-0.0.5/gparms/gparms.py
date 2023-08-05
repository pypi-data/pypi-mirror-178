import sys
from urllib.parse import urlparse

def main():
    for line in sys.stdin:
        urlString = line.strip('\n')
        url = urlparse(urlString)
        if(url.query != ""):
            print(line.strip('\n'))

