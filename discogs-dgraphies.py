import discogs_client
from discogs_client.exceptions import HTTPError
import pprint
import json
import time
import sys
from collections import defaultdict

 # 60 requests per minute if auntheticated

def _get_time():

	ttup = divmod(time.time() - t0, 3600)
	hrs = ttup[0]
	mins, secs = divmod(ttup[1], 60)

	return (hrs, mins, secs)

artists = json.load(open("data/artists.json","r"))
total_artists = len(artists)

fl = "artist_data_discogs.json"

# initialize Discogs client
d = discogs_client.Client("DiscoCollector/0.1",  # required User-Agent string
								user_token="tLdkEpKbLCLugjcLZmTaQCwuaIgSFNTLqXhjeUNH")

collected_data = []

t0 = time.time()

artist_list = [a for a in list(artists.keys()) if not (set(a.split()) & {"hits", "greatest", "choir", "collection"})]

for j, artist_name in enumerate(artist_list[57: 60]):

	print("artist {}: {}...".format(j+1, artist_name), end="")

	try:
		res = d.search(artist_name, type="artist") 
		# discogs_client.models.MixedPaginatedList
	except HTTPError:
		print("some http error!!")
		time.sleep(1)
		res = d.search(artist_name, type="artist")
	except:
		print("some non-http exception")
		time.sleep(1)
		continue
	if res.count == 0:
		print("can\'t find")
		continue

	for artist in res.page(1):
		try:
			artist.releases
			a = artist
			break
		except:
			continue

	#a = res.page(1)[0]

	print("artist:", a)
	print(dir(a))
	print("refresh=", a.images)
	print("url", a.url)
	
	time.sleep(1)

	art_dict = defaultdict()
	art_dict["name_variations"] = []

	try:
		art_dict["name"] = a.name.lower()
	except:
		art_dict["name"] = None

	try:
		art_dict["real_name"] = a.real_name.lower()
	except:
		art_dict["real_name"] = None

	try:
		art_dict["name_variations"] = [v.lower() for v in a.name_variations]
	except:
		art_dict["name_variations"] = [None]


	try:
		art_dict["aliases"] = [al.name.lower() for al in a.aliases]
	except:
		art_dict["aliases"] = [None]

	art_dict["social"] = {}
	art_dict["albums"] = []

	try:
		for u in a.urls:
			if "facebook" in u:
				art_dict["social"].update({"facebook": u})
			elif "twitter" in u:
				art_dict["social"].update({"twitter": u})
			elif "youtube" in u:
				art_dict["social"].update({"youtube": u})
			elif "wikipedia" in u:
				art_dict["social"].update({"wikipedia": u})
			elif "soundcloud" in u:
				art_dict["social"].update({"soundcloud": u})
			elif "equipboard" in u:
				art_dict["social"].update({"equiboard": u})
			elif "instagram" in u:
				art_dict["social"].update({"instagram": u})
			else:
				if "other" not in art_dict["social"]:
					art_dict["social"].update({"other": [u]})
				else:
						art_dict["social"]["other"].append(u)
	except HTTPError:
			print("http error - NO URLS!")
	except:
		print("some non-http problem with urls!")


	print("checking releases")

	try:
		a.releases
	except:
		print("NO RELEASES!")
		print("failed")
		time.sleep(1)
		continue

	# now browse releases
	for r in a.releases:

		count_nodata = 0
		try:
			release_data = r.data
			time.sleep(1)
		except AttributeError:
			count_nodata += 1
			print("note: {} releases without data so far!", count_nodata)
			continue
		# if there is some data..
		if ((release_data["type"] in {"release", "master"}) and
					(release_data["role"] == "Main") and
						(len(r.tracklist) > 6)):   # then we assume it's an album
			print("extracting another album")
			art_dict["albums"].append(
				{
				"title": release_data["title"].lower(),
				"year": release_data["year"],
				"tracklist": [{"#": track.data["position"], 
								"title": track.data["title"].lower(),
								"duration": track.data["duration"]} for track in r.tracklist]
				})

	collected_data.append(art_dict)
	print("done with this artist")

	print("ok. elapsed time: {:.0f}h {:.0f}m {:.0f}s".format(*_get_time()))
	# wait to avoid the 'You are making requests too quickly' error

json.dump(collected_data, open(fl, "w"), sort_keys=False, indent=4)

