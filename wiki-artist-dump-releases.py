import xml.etree.ElementTree as et
from collections import defaultdict
import json
import sys

required_artists = ["aerosmith", "alicia keys"]

def __get_artist_info(artist_elem):

	artist_rec = {}

	try:
		artist_id = artist_elem.find("id").text.lower().strip()
	except:
		# if no id, we don't care
		return None
	try:
		artist_name = artist_elem.find("name").text.lower().strip()
	except:
    	# we don't care about nameless artists
		return None
	try:
		artist_role = artist_elem.find("role").text.lower().strip()
	except:
		artist_role = None

	artist_rec.update({"id": artist_id, "name": artist_name, "role": artist_role})

	if artist_rec:
		return artist_rec
	else:
		return None

def __get_release_artists(rel_elem, artist_or_extra="artist"):

	found_artists = []

	if artist_or_extra == "artist":
		group_name = "artists"
		artist_type = "artist"
	elif artist_or_extra == "extra_artist":
		group_name = "extraartists"
		artist_type = "extraatrist"

	try:
		artists_field = rel_elem.find(group_name)  #  exception if there's no artists field
	except:
		return None

	if not artists_field:
		return None

	try:
		artist_list = artists_field.findall(artist_type)
	except:
		# if no <artist></artist>
		return None

	if not artist_list:
		return None

	for artist in artist_list:

		artist_rec = __get_artist_info(artist)

		if artist_rec:
			found_artists.append(artist_rec)

	if found_artists:
		return found_artists
	else:
		return None

def __get_record_labels(rel_elem):

	found_labels = []

	try:
		labels = rel_elem.find("labels")
	except:
		return None
	try:
		for lb in labels.findall("label"):
			found_labels.append({"name": lb.get("name").lower().strip(), "cat_no": lb.get("catno").lower().strip()})
		return found_labels
	except:
		return None

def __get_formats(rel_elem):

	found_formats = []

	try:
		formats = rel_elem.find("formats")
	except:
		return None
	try:
		for f in formats.findall("format"):
			found_formats.append(f.get("name").lower().strip())
		return found_formats
	except:
		return None

def __get_single_field(rel_elem, field_name):

	try:
		return rel_elem.find(field_name).text.lower().strip()
	except:
		return None

def __get_track_list(rel_elem):

	found_tracks = []

	try:
		tracklist = rel_elem.find("tracklist")
	except:
		return None
	try:
		for track in tracklist.findall("track"):
			found_tracks.append({"position": track.find("position").text.lower().strip(),
									"title": track.find("title").text.lower().strip(),
									"duration": track.find("duration").text.lower().strip()})
		return found_tracks
	except:
		return None

for ev, elem in et.iterparse('data/discogs_20170601_releases.xml', events=("start", "end")):

	"""
	this dump contains releases. artist is included in each release along with other information
	"""

	if (elem.tag == "release") and (ev == "end"):  # effectively this means that info on some release has been fully read

		release_info = defaultdict()
		release_info["artists"] = __get_release_artists(elem, artist_or_extra="artist")
		release_info["extra_artists"] = __get_release_artists(elem, artist_or_extra="extra_artist")
		release_info["labels"] = __get_record_labels(elem)
		release_info["formats"] = __get_formats(elem)
		release_info["country"] = __get_single_field(elem, "country")
		release_info["date"] = __get_single_field(elem, "released")
		release_info["tracklist"] = __get_track_list(elem)


		print(release_info)

		#sys.exit(0)
