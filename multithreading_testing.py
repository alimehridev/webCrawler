import threading
import time
import math
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import glob
from helpers import *
import os

def full_depth(session, url, links, thread_number, verbose, onlydomain, output_file, continue_last_crawl=False):
    seen = []
    found_links = []
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc

    ## www_domain and domain to check better
    www_domain = ""
    if "www." in domain:
        www_domain = domain
        domain = domain.replace("www.", "")
    else:
        www_domain = domain = domain.replace("www.", "")
    # Create directory and files to store information
    directory_name = "." + parsed_url.netloc.replace(".", "-")
    file_name = directory_name + "/" + str(thread_number) + "_thread.tmp"
    seen_file_name = directory_name + "/" + str(thread_number) + "_thread_seen.tmp"

    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass

    #Make BackUp Files to restore if needed .
    if os.path.isfile(seen_file_name) == False:
        f = open(seen_file_name, "w")
        f.close()
        f = open(file_name, "w")
        f.close()
    else:
        f = open(seen_file_name, "r")
        seen = f.read().split("\n")
        f.close()
        f = open(file_name, "r")
        links = f.read().split("\n")
        f.close()


    counter = 0
    while len(seen) < len(links):
        link = links[counter]
        if continue_last_crawl:
            if link in seen and len(seen) != 0:
                print(f"[*] {link} Checked Before .")
                counter += 1
                continue
        if is_asset(link) == False and (domain.replace("https://", "") in link or www_domain.replace("https://", "") in link): #and (link not in seen):
            try:
                link = link[link.index("http"):]
                res = session.get(link, timeout=5)
                # soup = BeautifulSoup(res.html.html, "html.parser", features="xml")
            except:
                print("[-]", link, "Error happend so passed . ")
                counter += 1
                continue    
            # found_links += find_links(soup, parsed_url=parsed_url, domain=domain, verbose=verbose, onlydomain=onlydomain)
            found_links += list(res.html.absolute_links)
            found_links = unique(found_links)
            links += found_links
            links = correction(links, domain=domain)
            links = unique(links)
            output = open(file_name, "w")
            output.write("\n".join(links))
            output.write("\n")
            output.close()
            print("Thread Number [", thread_number, "] working on [" + str(len(seen)) + " /", len(links), "] links .")
        seen.append(link)
        f = open(seen_file_name, "w")
        f.write("\n".join(seen))
        f.write("\n")
        f.close()
        counter += 1


def multithreading(target, args, threads = 4):
    links = args['links']
    chunks = [links[x:x+math.ceil((len(links) / threads))] for x in range(0, len(links), math.ceil(len(links) / threads))]
    session = args["session"]
    url = args["url"]
    verbose = args["verbose"]
    onlydomain = args["onlydomain"]
    output_file = args["output_file"]
    continue_last_crawl = args['continue_last_crawl']


    # Checking Threads Number is equal files in site directory
    if continue_last_crawl == True:
        parsed_url = urlparse(url)
        directory_name = "." + parsed_url.netloc.replace(".", "-")
        threads = len(glob.glob('*_thread.tmp', root_dir=directory_name + "\\"))
    
    thread_list = []
    for thread in range(threads):
        try:

            th = threading.Thread(target=full_depth, kwargs={"session": session
                , "url": url
                , "verbose": verbose
                , "onlydomain": onlydomain
                , "output_file": output_file
                , "links": chunks[thread]
                , "thread_number": thread + 1,
                'continue_last_crawl': continue_last_crawl})
            th.start()
            thread_list.append(th)
        except IndexError:
            break

    for thread in thread_list:
        thread.join()

    
    t = time.time()
    print("Done in : ", time.time() - t)


args = ["https://flightio.com/", "https://flightio.com/blog/feed/", "https://flightio.com/blog/comments/feed/", "https://flightio.com/blog/wp-json/", "https://flightio.com/blog/travel-tips/", "https://flightio.com/blog/attractions/", "https://flightio.com/blog/tourism-news/intro-to-qatar-expo/", "https://flightio.com/blog/category/tourism-news/", "https://flightio.com/blog/attractions/turkey-islands/", "https://flightio.com/blog/category/attractions/", "https://flightio.com/blog/attractions/taksim-square-guide/", "https://flightio.com/blog/travel-tips/best-istanbul-restaurants/", "https://flightio.com/blog/category/travel-tips/", "https://flightio.com/blog/attractions/foods-in-qatar/", "https://flightio.com/blog/attractions/towns-and-villages-in-qatar/", "https://flightio.com/blog/travel-tips/qatar-travel-guide/", "https://flightio.com/blog/attractions/reasons-to-visit-qatar/", "https://flightio.com/blog/attractions/khalifa-international-stadium/", "https://flightio.com/blog/travel-tips/istanbul-amusement/", "https://flightio.com/blog/travel-tips/istanbuls-best-boutique-hotels/", "https://flightio.com/blog/travel-tips/best-luxury-hotels-in-istanbul/", "https://flightio.com/blog/travel-tips/pre-travel-anxiety-what-it-is-and-how-to-cope/", "https://flightio.com/blog/travel-tips/astara-baku/", "https://flightio.com/blog/travel-tips/types-of-flight-class/", "https://flightio.com/blog/author/zeinababedini/", "https://flightio.com/blog/attractions/qatar-education-city-stadium/", "https://flightio.com/../../../", "https://flightio.com/blog/encyclopedia/departure-toll/", "https://flightio.com/blog/travel-tips/foreign-exchange/", "https://flightio.com/blog/travel-tips/frequent-question-in-airport-list/", "https://flightio.com/blog/airport-information/ikia-airport/", "https://flightio.com/blog/flightio-events/abroad-travel-restrictions/", "https://flightio.com/blog/travel-tips/steps-to-board-the-plane/", "https://flightio.com/blog/travel-tricks/tax-free/", "https://flightio.com/blog/travel-tips/travel-check-list-flightio/", "https://flightio.com/blog/travel-tips/things-not-allowed-on-flights/feed/", "https://flightio.com/blog/author/h-sadeghi/", "https://flightio.com/blog/travel-tips/kish-travel-guide/feed/", "https://flightio.com/blog/attractions/attractions-in-kish/", "https://flightio.com/blog/hotel-information/kish-island/", "https://flightio.com/blog/travelling-in-iran/kish-malls/", "https://flightio.com/blog/travelling-in-iran/dont-miss-kish/", "https://flightio.com/blog/category/travel-tips/page/2/", "https://flightio.com/blog/category/travel-tips/feed/", "https://flightio.com/blog/travel-tips/page/2/", "https://flightio.com/blog/travel-tips/page/3/", "https://flightio.com/blog/travel-tips/page/147/", "https://flightio.com/blog/category/attractions/page/2/", "https://flightio.com/blog/category/attractions/feed/", "https://flightio.com/blog/attractions/istanbul-water-parks/", "https://flightio.com/blog/attractions/page/2/", "https://flightio.com/blog/attractions/page/3/", "https://flightio.com/blog/attractions/page/54/", "https://flightio.com/blog/tourism-news/intro-to-qatar-expo/feed/", "https://flightio.com/blog/tourism-news/qatar-events/", "https://flightio.com/blog/category/tourism-news/page/2/", "https://flightio.com/blog/category/tourism-news/feed/", "https://flightio.com/blog/tourism-news/formula-1-doha-travel/", "https://flightio.com/blog/tourism-news/suncity-routes/", "https://flightio.com/blog/tourism-news/abroad-travel-restrictions/", "https://flightio.com/blog/tourism-news/leap-year/", "https://flightio.com/blog/category/tourism-news/page/3/", "https://flightio.com/blog/category/tourism-news/page/12/", "https://flightio.com/blog/attractions/turkey-islands/feed/", "https://flightio.com/blog/attractions/foods-in-turkey/", "https://flightio.com/blog/author/e-azad/", "https://flightio.com/blog/category/attractions/page/3/", "https://flightio.com/blog/category/attractions/page/54/", "https://flightio.com/blog/attractions/taksim-square-guide/feed/", "https://flightio.com/blog/attractions/istanbul-card/", "https://flightio.com/blog/attractions/best-museums-in-istanbul/", "https://flightio.com/blog/globe-trotting/istanbul-traditions/", "https://flightio.com/blog/travel-tips/best-istanbul-restaurants/feed/", "https://flightio.com/blog/author/parnia/", "https://flightio.com/blog/category/travel-tips/page/3/", "https://flightio.com/blog/category/travel-tips/page/147/", "https://flightio.com/blog/attractions/foods-in-qatar/feed/", "https://flightio.com/blog/attractions/towns-and-villages-in-qatar/feed/", "https://flightio.com/blog/travel-tips/qatar-travel-guide/feed/", "https://flightio.com/blog/visa-information/qatar-visa/", "https://flightio.com/blog/hotel-information/best-hotel-in-qatar/", "https://flightio.com/blog/author/n-soltani/", "https://flightio.com/blog/attractions/reasons-to-visit-qatar/feed/", "https://flightio.com/blog/attractions/qatar-attractions/", "https://flightio.com/blog/author/salahshooratefe/", "https://flightio.com/blog/attractions/khalifa-international-stadium/feed/", "https://flightio.com/blog/travel-tips/istanbul-amusement/feed/", "https://flightio.com/blog/attractions/istanbul-attractions/", "https://flightio.com/blog/attractions/aqua-club-dolphin/", "https://flightio.com/blog/author/javidi/", "https://flightio.com/blog/travel-tips/istanbuls-best-boutique-hotels/feed/", "https://flightio.com/blog/travel-tips/best-luxury-hotels-in-istanbul/feed/", "https://flightio.com/blog/travel-tips/pre-travel-anxiety-what-it-is-and-how-to-cope/feed/", "https://flightio.com/blog/travel-tips/astara-baku/feed/", "https://flightio.com/blog/attractions/astara-attraction/", "https://flightio.com/blog/travel-tips/types-of-flight-class/feed/", "https://flightio.com/blog/travel-tips/types-of-travel/", "https://flightio.com/blog/author/zeinababedini/feed/", "https://flightio.com/blog/globe-trotting/best-luxury-hotels-in-dubai/", "https://flightio.com/blog/attractions/qatar-education-city-stadium/feed/", "https://flightio.com/blog/travel-tips/astara-baku/feed/", "https://flightio.com/blog/attractions/astara-attraction/", "https://flightio.com/blog/travel-tips/types-of-flight-class/feed/", "https://flightio.com/blog/travel-tips/types-of-travel/", "https://flightio.com/blog/author/zeinababedini/feed/", "https://flightio.com/blog/globe-trotting/best-luxury-hotels-in-dubai/", "https://flightio.com/blog/attractions/qatar-education-city-stadium/feed/", "https://flightio.com/blog/travel-tips/astara-baku/feed/", "https://flightio.com/blog/attractions/astara-attraction/", "https://flightio.com/blog/travel-tips/types-of-flight-class/feed/", "https://flightio.com/blog/travel-tips/types-of-travel/", "https://flightio.com/blog/author/zeinababedini/feed/", "https://flightio.com/blog/globe-trotting/best-luxury-hotels-in-dubai/", "https://flightio.com/blog/attractions/qatar-education-city-stadium/feed/"]

args += args
# t = time.time()
# target(args)
# print("Done in : ", time.time() - t)
