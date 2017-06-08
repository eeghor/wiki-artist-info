import discogs_client
from discogs_client.exceptions import HTTPError
import pprint
import json
import time
import sys
from collections import defaultdict

 # 60 requests per minute if auntheticated
SLEEPSEC = 0.5
SAVE_EVERY = 500

def _get_time():
	"""
	return elapsed time as hours, minutes and seconds
	"""

	ttup = divmod(time.time() - t0, 3600)
	mins, secs = divmod(ttup[1], 60)

	return (ttup[0], mins, secs)

def _do_search(artist_name, rtry=0):
	"""
	submit artist search request
	"""

	try:
		res = d.search(artist_name, type="artist") 
		# res is discogs_client.models.MixedPaginatedList
	except HTTPError as e:
		if (e.status_code == 429) and (rtry < 6):   # sending requests too quickly
			time.sleep(10)
			rtry += 1
			_do_search(artist_name, rtry + 1)
		else:
			return None
	except:
		return None
	return res

def _request_data(release, rtry=0):
	"""
	submit release data request
	"""
	try:
		res = release.data
		# res is discogs_client.models.MixedPaginatedList
	except HTTPError as e:
		if (e.status_code == 429) and (rtry < 6):   # sending requests too quickly
			time.sleep(60)
			rtry += 1
			_request_data(release, rtry + 1)
		else:
			return None
	except:
		return None
	return res



artists = json.load(open("data/artists.json","r"))
total_artists = len(artists)

fl = "artist_data_discogs.json"

# initialize Discogs client
d = discogs_client.Client("DiscoCollector/0.1",  # required User-Agent string
								user_token="tLdkEpKbLCLugjcLZmTaQCwuaIgSFNTLqXhjeUNH")

collected_data = []

t0 = time.time()

artist_list = [a for a in list(artists.keys()) if not (set(a.split()) & {"hits", "greatest", "choir", "collection"})]

for j, artist_name in enumerate(artist_list):

	print("artist {}/{}: {}...".format(j+1, total_artists, artist_name), end="")

	res = _do_search(artist_name)

	if not res:
		print("failed")
		continue

	if res.count == 0:
		print("failed")
		continue

	for artist in res.page(1):
		try:
			artist.releases
			a = artist
			break
		except:
			continue

	time.sleep(SLEEPSEC)

	art_dict = defaultdict()
	art_dict["name_variations"] = []
	art_dict["social"] = {}
	art_dict["albums"] = []

	try:
		art_dict["name"] = a.name.lower()
	except:
		continue

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
		pass
	except:
		pass

	# now browse releases
	for r in a.releases:

		count_nodata = 0

		time.sleep(SLEEPSEC)

		release_data = _request_data(r)

		# if there is some data..
		try:
			if ((release_data["type"] in {"release", "master"}) and
						(release_data["role"] == "Main") and
							(len(r.tracklist) > 6)):   # then we assume it's an album
				art_dict["albums"].append(
					{
					"title": release_data["title"].lower(),
					"year": release_data["year"],
					"tracklist": [{"#": track.data["position"],
									"title": track.data["title"].lower(),
									"duration": track.data["duration"]} for track in r.tracklist]
					})
		except:
			continue

	# add this artist's info to the list
	collected_data.append(art_dict)

	print("ok. elapsed time: {:.0f}h {:.0f}m {:.0f}s".format(*_get_time()))
	# wait to avoid the 'You are making requests too quickly' error

	tp = divmod(j, SAVE_EVERY)

	if (j > 0) and (tp[1] == 0):
		json.dump(collected_data[SAVE_EVERY*(tp[0]-1):SAVE_EVERY*tp[0]], open("data/AD{}.json".format(tp[0]), "w"), 
			sort_keys=False, indent=4)

