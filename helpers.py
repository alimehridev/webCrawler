from urllib.parse import urlparse

def find_links(soup, parsed_url, domain, verbose, onlydomain, includes = [], excludes = []):
    links = []
    for a in soup.find_all(attrs={"href": True}):
        lnk = a['href']
        parsed_lnk = urlparse(lnk)
        if parsed_url.netloc not in lnk and (parsed_lnk.netloc == ""):
            if lnk.startswith("/"):
                lnk = domain + lnk
            else:
                lnk = domain + "/" + lnk
        
        if(verbose):
            print(lnk)
        if(onlydomain):
            if domain in lnk:
                links.append(lnk)
        else:
            links.append(lnk)

    for s in soup.find_all(attrs={"src": True}):
        lnk = s['src']
        parsed_lnk = urlparse(lnk)
        if parsed_url.netloc not in lnk and (parsed_lnk.netloc == ""):
            if lnk.startswith("/"):
                lnk = domain + lnk
            else:
                lnk = domain + "/" + lnk
        if(verbose):
            print(lnk)
        if(onlydomain):
            if domain in lnk:
                links.append(lnk)
        else:
            links.append(lnk)

    for e in soup.find_all(attrs={"action": True}):
        lnk = e['action']
        parsed_lnk = urlparse(lnk)
        if parsed_url.netloc not in lnk and (parsed_lnk.netloc == ""):
            if lnk.startswith("/"):
                lnk = domain + lnk
            else:
                lnk = domain + "/" + lnk
        if(verbose):
            print(lnk)
        if(onlydomain):
            if domain in lnk:
                links.append(lnk)
        else:
            links.append(lnk)
            
    uniqs = []
    for l in links:
        if l not in uniqs and (l[0:-1] not in uniqs):
            uniqs.append(l)
    return uniqs

def is_asset(link):
    parsed_link = urlparse(link)
    asset_extensions = [
        '.jpg', '.png', '.webp', '.gif', '.pdf', '.jpeg', '.epub', '.mp3', '.mp4', '.js', '.css', '.scss', '.less', '.ico' 
    ]
    for ext in asset_extensions:
        if ext in parsed_link.path:
            return True
    return False

def unique(lst):
    uniqs = []
    for l in lst:
        if l not in uniqs and (l[0:-1] not in uniqs):
            uniqs.append(l)
    return uniqs

def correction(links_list, domain):
    domain = urlparse(domain)
    links = []
    for l in links_list:
        if is_asset(l):
            parsed = urlparse(l)
            if(parsed.netloc == ""):
                l = domain.scheme + "://" + domain.netloc + parsed.path
        if l.startswith("//"):
            l = l[2:]
        if l.endswith("/"):
            l = l[:-1]
        links.append(l)
    return links