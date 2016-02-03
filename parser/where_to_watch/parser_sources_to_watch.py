import sys
import re
import json

# got input_shows.csv from sources parser output (output_sources.csv)
# bcmoe.json is from https://github.com/mczub/because-moe

filename = sys.argv[1]
tracefile = open(filename, "r")
newfile = open("output_sources_to_watch.csv", "w")

json_data = open("bcmoe.json")
watch_obj = json.load(json_data)

while True:
	line = tracefile.readline()

	if line == "":
		break

 	line = line.replace('\n', '')
	found = False

	for show in watch_obj:
		if show['name'] == line:
			newfile.write(line + "," + str(show['sites']) + "\n")
			found = True

	if not found:
		# not found
		print "Not found ", line


json_data.close()
