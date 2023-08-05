import sys
from urllib.parse import urlparse
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="Takes a list of urls and returns the urls with parameters.",
    usage="cat allUrls.txt | gparms [options]")

    parser.add_argument('-s', action='store_true', help="If 1 URL has 3 parameters, then it will turn it into 3 URLs with 1 parameter each.")
    args = parser.parse_args()

    for line in sys.stdin:
        urlString = line.strip('\n')
        url = urlparse(urlString)
        if(url.query != ""):
            if(args.s == False):
                print(line.strip('\n'))
            else:
                querys = url.query.split('&')
                if(len(querys) > 1):
                    for query in querys:
                        print(url.scheme + '://' + url.netloc + url.path + '?' + query)
