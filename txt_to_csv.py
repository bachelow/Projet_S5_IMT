

def txt_to_csv_fn(input,output):

	# Open the txt file
	file = open(input, 'r', encoding = "utf-8")

	# Read the file
	new_text = file.readlines()

	# Create a list to keep all the words in file
	words = []
	line_break = 0

	# Add all the words in file to list
	for x in range(0, len(new_text)):
		for word in new_text[x].split():
			words.append(word + ',')

	# Write words into csv file
	f = open(output,'w')
	for x in range(0, len(words)):
		if (line_break == 37):
			f.write('\n')
			f.write(words[x])
			line_break = 1
		else:
			f.write(words[x])
			line_break += 1
	f.close()