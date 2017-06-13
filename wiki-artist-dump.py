import xml.etree.ElementTree as et
from collections import defaultdict
import json

def __find(element, child_name):

    try:
        child = element.find(child_name).text.lower().strip()
    except:
        child = None
    return child

def __find_kids(element, child_name, grandchild_name):

    try:
        child = element.find(child_name)
    except:
        # if there's no child not much sense to proceed
        return None

    if not child:
        return None

    try:
        grandchildren = child.findall(grandchild_name)
    except:
        # what if grandchildren are missing
        return None

    if not grandchildren:
        return None

    return [v.text.lower().strip() for v in grandchildren if v.text]


artist_lst = []

c = 0

for ev, a in et.iterparse('data/discogs_20170601_artists.xml', events=("start", "end")):
    
    c += 1

    if (a.tag == "artist") and (ev == "end"):
        
        art_dict = defaultdict()
        
        art_dict["media"] = {}
    
        art_dict["name"] = __find(a, "name")
        art_dict["real_name"] = __find(a, "realname")
        
        art_dict["name_variations"] = __find_kids(a, "namevariations", "name")
        art_dict["aliases"] = __find_kids(a, "aliases", "name")
        
        artist_urls = __find_kids(a, "urls", "url")
        
        if artist_urls:
            
            urls_labl = "media"
            
            for u in artist_urls:
                if "facebook" in u:
                    art_dict[urls_labl].update({"facebook": u})
                elif "twitter" in u:
                    art_dict[urls_labl].update({"twitter": u})
                elif "youtube" in u:
                    art_dict[urls_labl].update({"youtube": u})
                elif "wikipedia" in u:
                    art_dict[urls_labl].update({"wikipedia": u})
                elif "soundcloud" in u:
                    art_dict[urls_labl].update({"soundcloud": u})
                elif "equipboard" in u:
                    art_dict[urls_labl].update({"equiboard": u})
                elif "instagram" in u:
                    art_dict[urls_labl].update({"instagram": u})
                else:
                    if "other" not in art_dict[urls_labl]:
                        art_dict[urls_labl].update({"other": [u]})
                    else:
                        art_dict[urls_labl]["other"].append(u)
        
        artist_lst.append(art_dict)
        a.clear()

        if c%100 == 0:
            print("artist so far: {}".format(len(artist_lst)))

        if len(artist_lst) == 5000:
            json.dump(artist_lst, open("data/AD{}.json".format(tp[0]), "w"), sort_keys=False, indent=4)
            artist_lst = []
