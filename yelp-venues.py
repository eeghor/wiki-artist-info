from yelpapi import YelpAPI
import json
import time

search_term = "live music"
loc = "Sydney"
fl = "data/live_venues_syd.json"

yelp_api = YelpAPI(client_id="UPGF-lyvi9RNGRVYPrD4UQ", client_secret="L3DvMeZEyH4gEiLGioSnlkk0pflOr2Y0ZB4g7x379PGHZma5KVBuuX0h6eZTJODj")

dk = {'businesses': []}

i = 0
t0 = time.time()

print("collecting data...")

while True:
	try:
		res = yelp_api.search_query(term=search_term, location=loc, limit=50, offset=50*i)["businesses"]
		i += 1
		if res:
			dk["businesses"].extend(res)
	except:
		break

json.dump(dk, open(fl, "w"), sort_keys=True, indent=4)
print("done. collected {} items. elapsed time: {:02.0f} min {:02.0f} sec\nsaved data to {}".format(len(dk["businesses"]), *divmod(time.time() - t0, 60), fl))