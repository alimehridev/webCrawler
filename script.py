from bs4 import BeautifulSoup
from urllib.parse import urlparse
from helpers import find_links
from functions import full_depth, not_full_depth
from multithreading_testing import multithreading
import sys
from requests_html import HTMLSession
import argparse


parser = argparse.ArgumentParser(description="webCrawl is a very simple url crawler .", epilog="example: python script.py -u https://google.com --cookies xwidth=1920;xheight=1032;sessionid=ed83623d96a51fb1bc --depth 3 --threads 8 -o result.txt")
parser.add_argument("-u", "--url", type=str, required=True, help="URL to crawl . [Required]")
parser.add_argument("-c", "--cookies", type=str, default="", help="Set cookies if authentication is required, sperate them with ';' . example: xwidth=1920;xheight=1032;sessionid=ed83623d96a51fb1bc")
parser.add_argument("-d", "--depth", type=str, default=2, help="Assign depth of crawl, default=2")
parser.add_argument("-v", "--verbose", action='store_true', help="Set verboseness to show more logs")
parser.add_argument("-ex", "--excludes", type=str, help='Set some filters that webCrawler should not crawl them, example "jpg,png,gif,css"')
parser.add_argument("-in", "--includes", type=str, help='Set some filters that webCrawler should only crawl them, example "php,aspx,py"')
parser.add_argument("-t", "--threads", type=int, default=3, help='Threads number, default=3 and max=16')
parser.add_argument("-a", "--assets", action="store_true", help='If crawling assets like js files is necessary .')
parser.add_argument("-o", "--output_file", default="[url].txt", help='output_file to save the output . [default=[url].txt]')
parser.add_argument("-f", "--format", default="plain_text", help='Format of output, default=plain_text [json is other option]')
parser.add_argument("-m", "--morelogs", action="store_true", help='Save more logs like Status Code of each links .')
parser.add_argument("-co", "--continue", action="store_true", help='Continue last crawl .')
parser.add_argument("--onlydomain", action="store_true", help='Just save links in this domain and ignore others .')

args = vars(parser.parse_args())
# {'url': 'https://google.com', 'cookies': '', 'depth': 2, 'verbose': True, 'exclude': None, 'threads': 3, 'assets': True, 'output_file': '[url].txt', 'format': 'plain_text', 'morelogs': True}
url = args['url'] 
cookies = args['cookies']
depth = args['depth']
verbose = args['verbose']
excludes = args['excludes']
includes = args['includes']
threads = args['threads']
assets = args['assets']
output_file = args['output_file']
format = args['format']
morelogs = args['morelogs']
onlydomain = args['onlydomain']
continue_last_crawl = args['continue']



if includes != None:
    includes = includes.split(",")
else:
    includes = []
if excludes != None:
    excludes = excludes.split(",")
else:
    excludes = []


parsed_url = urlparse(url)
domain = parsed_url.scheme + "://" + parsed_url.netloc
if output_file == "[url].txt":
    output_file = "temp/" + parsed_url.netloc + ".urls"
else:
    output_file = "temp/" + output_file
# cookies = """xwidth=1920; xheight=1032; was_visit=ed83623d96a51fb1bc746e277dcc5d5630bb1ad4919f3f18946b31ef96e2182aa%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22was_visit%22%3Bi%3A1%3Bs%3A1%3A%221%22%3B%7D; _ga=GA1.1.977938011.1699375141; _csrf=8d5bef65971b5dfa509e69573c8f156476e84069ff61e3107841fdfbf6677d85a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Q_jI463uSEyteiIcyd1Qh6untz7aqq7y%22%3B%7D; tlSID7=f215e36e493f6868cb3c517cf618b677; xwidth=1920; xheight=1032; _ga_RC2YBRG0B6=GS1.1.1699623402.8.1.1699624279.0.0.0"""
cookies = cookies.split(";")
cookies_dict = {}
for cookie in cookies:
    cookie = cookie.split("=")
    try:
        cookies_dict[cookie[0]] = cookie[1]
    except:
        pass

session = HTMLSession()
try:
    response = session.get(url)
    links_without_render = response.html.absolute_links
    response.html.render()
    links_with_render = response.html.absolute_links
    if len(links_with_render) > len(links_without_render):
        links = list(links_with_render)
    else:
        links = list(links_without_render)
    
    if len(links) == 0:
        print("[-] 0 links found and it means something is wrong . Status Code:", response.status_code)
        sys.exit()
except ConnectionAbortedError:
    print("[-] Connection Error Hanppend .")
    sys.exit()

# if depth == "full":
# full_depth(session=session, url=url, verbose=verbose, onlydomain=onlydomain, output_file=output_file, links=links)
multithreading(target=full_depth, args={"session": session
                                          , "url": url
                                          , "verbose": verbose
                                          , "onlydomain": onlydomain
                                          , "output_file": output_file
                                          , "links": links
                                          , "continue_last_crawl": continue_last_crawl}, threads=threads)
if depth != "full":
    depth = int(depth)
    not_full_depth(session=session, url=url, verbose=verbose, onlydomain=onlydomain, output_file=output_file, links=links, depth=depth)

