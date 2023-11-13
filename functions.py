from bs4 import BeautifulSoup
from helpers import *


def full_depth(session, url, verbose, onlydomain, output_file, links):
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc
    seen = []
    counter = 0
    while len(seen) != len(links):
        l = links[counter]
        counter += 1
        if l not in seen:
            if is_asset(l) == False and domain in l:
                try:
                    res = session.get(l)

                    soup = BeautifulSoup(res.html.html, "html.parser")
                    links += find_links(soup, parsed_url=parsed_url, domain=domain, verbose=verbose, onlydomain=onlydomain)
                except:
                    print("[-]", l, "is passed .")
                links = correction(links, domain=domain)
                links = unique(links)
                remains = len(links) - len(seen)
                if remains != 1:
                    print(str(len(seen)) + "/" + str(len(links)), "links have been check -", remains, "remain .")
                else:
                    print(str(len(seen)) + "/" + str(len(links)), "links have been check -", remains, "remains .")
                output = open(output_file, "w")
                output.write("\n".join(links))
                output.write("\n")
                output.close()
            seen.append(l)

    

def not_full_depth(session, url, verbose, onlydomain, output_file, links, depth):
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc
    counter = 0
    result = [links]
    while depth != 0:
        print("[+] Depth", counter + 1, "started .")
        links = result[counter]
        if len(result) > 1:
            links = list(set(result[counter]) - set(result[counter - 1]))
        links_items = fetch_links(session=session, url=url, verbose=verbose, onlydomain=onlydomain, links=links, depth=counter + 1)
        links_items = correction(links_items, domain=domain)
        result.append(links_items)
        counter += 1
        depth -= 1
    empty_list = []
    for item in result:
        if len(item) != 0:
            empty_list += item
    result = correction(empty_list, domain=domain)
    result = unique(empty_list)
    output = open(output_file, "w")
    output.write("\n".join(result))
    output.write("\n")
    output.close()
    
def fetch_links(session, url, verbose, onlydomain, links, depth):
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc
    links_items = []
    counter = 0
    for link in links:
        counter += 1
        list_of_links = []
        try:
            if is_asset(link):
                print("[Depth:", depth, "]", str(counter) + "/" + str(len(links)), " is an asset an not checked .")
                continue
            res = session.get(link, timeout=3)
            soup = BeautifulSoup(res.html.html, "html.parser")
            list_of_links = find_links(soup, parsed_url=parsed_url, domain=domain, verbose=verbose, onlydomain=onlydomain)
            links_items += list_of_links
        except:
            print("[-]", link, "is passed .")
        remains = len(links) - counter
        if remains != 1:
            print("[Depth:", depth, "]", str(counter) + "/" + str(len(links)), "links have been check [", len(list_of_links) ,"New links] -", remains, "remain .")
        else:
            print("[Depth:", depth, "]", str(counter) + "/" + str(len(links)), "links have been check [", len(list_of_links) ,"New links] -", remains, "remains .")

    links_items = correction(links_items, domain=domain)
    links_items = unique(links_items)
    return links_items