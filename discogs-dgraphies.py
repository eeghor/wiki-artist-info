import discogs_client
import pprint

d = discogs_client.Client("DiscoCollector/0.1",  # required User-Agent string
								user_token="tLdkEpKbLCLugjcLZmTaQCwuaIgSFNTLqXhjeUNH")

res = d.search("flume", type="artist")  # iterator containing artist objects

a = res[0]  # top search result

for r in a.releases:
	try:
		print("{} - {}".format(r.title, r.year))
		print(tracklist)
	except:
		pass
