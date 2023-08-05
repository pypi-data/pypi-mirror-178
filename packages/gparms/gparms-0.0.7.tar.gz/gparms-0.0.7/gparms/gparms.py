import sys
from urllib.parse import urlparse
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="Takes a list of urls and returns the urls with parameters.",
    usage="cat allUrls.txt | gparms [options]")

    parser.add_argument('-t', action='store_true', help="If 1 URL has 3 parameters, then it will turn it into 3 URLs with 1 parameter each.")
    parser.add_argument('-s', metavar='scope.txt', help="Include a file with a list of inscope domains.")
    args = parser.parse_args()

    for line in sys.stdin:
        urlString = line.strip('\n')
        url = urlparse(urlString)
        if(url.query != ""):
            if(args.t == False):
                if(args.s is not None):
                    with open(args.s) as scope_file:
                        for scope in scope_file:
                            if(url.netloc == scope.strip('\n')):
                                print(line.strip('\n'))
                else:
                    print(line.strip('\n'))
            else:
                querys = url.query.split('&')
                if(len(querys) > 1):
                    for query in querys:
                        if(args.s is not None):
                            with open(args.s) as scope_file:
                                for scope in scope_file:
                                    if(url.netloc == scope.strip('\n')):
                                        print(url.scheme + '://' + url.netloc + url.path + '?' + query)
                        else:
                            print(url.scheme + '://' + url.netloc + url.path + '?' + query)
