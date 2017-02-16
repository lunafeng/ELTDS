import ast
import sys
import csv
import isAmbig

with open("original_tweets_spots.csv", "r") as fd:
	contents = csv.reader(fd)
	count = 0
	spots_raw_all = []
	for c in contents:
		if count == 0:
			pass
		else:
			spots_raw = ast.literal_eval(c[2])
			spots_raw_all.append(spots_raw)
		count += 1
	spots_all = sum(spots_raw_all, [])
	spots_all = list(set(spots_all))

	fdspot = open("spots_ambig", "w+")
	for spot in spots_all:
		spot = spot.replace(" ", "_")
		print spot
		sys.stdout.flush()
		if isAmbig.main(spot.title()) is True or isAmbig.main(spot.capitalize()) is True or isAmbig.main(spot.lower()) is True:
			fdspot.write(spot.lower() + ",1\n")
		else:
			fdspot.write(spot.lower() + ",0\n")
		fdspot.flush()
		
