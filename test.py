import argparse

parser = argparse.ArgumentParser(description="webCrawl is a very simple url crawler .", epilog="example: python script.py -u https://google.com --cookies xwidth=1920;xheight=1032;sessionid=ed83623d96a51fb1bc --depth 3 --threads 8 -o result.txt")
parser.add_argument("-u", "--url", type=str, required=True, help="URL to crawl . [Required]")
parser.add_argument("-c", "--cookies", type=str, default="", help="Set cookies if authentication is required, sperate them with ';' . example: xwidth=1920;xheight=1032;sessionid=ed83623d96a51fb1bc")
parser.add_argument("-d", "--depth", type=str, default=2, help="Assign depth of crawl, default=2")
parser.add_argument("-v", "--verbose", action='store_true', help="Set verboseness to show more logs")
parser.add_argument("-ex", "--exclude", type=str, help='Set some endpoints that webCrawler should not crawl them, example "jpg,png,gif,css"')
parser.add_argument("-t", "--threads", type=int, default=3, help='Threads number, default=3 and max=16')
parser.add_argument("-a", "--assets", action="store_true", help='If crawling assets like js files is necessary .')
parser.add_argument("-o", "--output_file", default="[url].txt", help='output_file to save the output . [default=[url].txt]')
parser.add_argument("-f", "--format", default="plain_text", help='Format of output, default=plain_text [json is other option]')
parser.add_argument("-m", "--morelogs", action="store_true", help='Save more logs like Status Code of each links .')
parser.add_argument("--onlydomain", action="store_true", help='Just save links in this domain and ignore others .')
args = vars(parser.parse_args())
# {'url': 'https://google.com', 'cookies': '', 'depth': 2, 'verbose': True, 'exclude': None, 'threads': 3, 'assets': True, 'output_file': '[url].txt', 'format': 'plain_text', 'morelogs': True}
url = args['url']
cookies = args['cookies']
depth = args['depth']
verbose = args['verbose']
exclude = args['exclude']
threads = args['threads']
assets = args['assets']
output_file = args['output_file']
format = args['format']
morelogs = args['morelogs']
onlydomain = args['onlydomain']

