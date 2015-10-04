import os

from bs4 import BeautifulSoup

def extract_from_imdb_file(filename, csvfile, index):
	print "Extracting ", filename
	file = open('data/imdb/' + filename, 'r')
	soup = BeautifulSoup(file, 'html.parser')
	
	title = soup.find("meta", attrs={"property" : "og:title"})
	title_year = title.get("content")
	print title_year

	#title_year = "Argo (2012)"
	mtitle = title_year.split("(")[0] #Stores the name
	
	'''
	string_after_title = title_year.split("(")[1].split(")")[0]
	myear = [int(s) for s in string_after_title.split() if s.isdigit()]
	print mtitle
	print myear[0]
	'''
	release_date = ""
	release_date_a_tag = soup.find("a", attrs={"title" : "See all release dates"})
	if(release_date_a_tag):
		release_date = release_date_a_tag.find("meta").get("content")

	csv_entry = str(index) + "^" + mtitle + "^" + release_date
	csv_entry = csv_entry + "\n"
	csvfile.write(csv_entry)

	file.close()	

def extract_imdb_data():
	print "Extracting IMDB Movies data..."
	csvfile = open('data/imdb.csv', 'w+')
	csvfile.write("0^Title^Year\n")

	index = 1
	for filename in os.listdir('data/imdb/'):
		if filename.endswith(".html"):
			extract_from_imdb_file(filename, csvfile, index)
			index = index + 1

	csvfile.close()
def extract_rottentomatoes_data():
	print "Extracting Rotten Tomatoes Movies data..."

def main():
	extract_imdb_data()
	extract_rottentomatoes_data()

if __name__ == '__main__':
	main()